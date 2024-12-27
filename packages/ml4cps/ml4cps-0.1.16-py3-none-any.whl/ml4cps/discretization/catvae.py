import pytorch_lightning as pl
import torch
import numpy as np
from torch import nn
from torch.nn import functional as F
from pytorch_lightning.loggers import TensorBoardLogger
from pytorch_lightning.callbacks import EarlyStopping
import os
import yaml
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import pandas as pd
from torch.utils.data import DataLoader, TensorDataset
import pytorch_lightning as pl
import torch
import os
import torch
import random
import _pickle as pkl
from tqdm import tqdm
from pathlib import Path
from sklearn.preprocessing import StandardScaler
from mlxtend.frequent_patterns import association_rules
from mlxtend.frequent_patterns.fpgrowth import fpgrowth
from sklearn.metrics import precision_score
from ml4cps.discretization import  TimeSeriesDiscretizer


class DataModule(pl.LightningDataModule):
    # Decide on the different datasets by entering either 'SmA_normal',
    # 'SmA_anomalyID2', BeRfiPl_ds1n', BeRfiPl_ds1c', 'SWaT_norm', 'SWaT_anom, 'Tank_normal' or 'Tank_anomaly'
    def __init__(self, hparam_batch, time, train, states, train_names, state_names, num_workers: int = 20,
                 train_part=0.75):
        super().__init__()
        self.batch_size = hparam_batch
        self.num_workers = num_workers

        train_data = train[:int(train_part * len(train))]
        valid_data = train[int(train_part * len(train)):]
        self.ds_train = TensorDataset(torch.cat(train_data))
        self.ds_val = TensorDataset(torch.cat(valid_data))

    def train_dataloader(self):
        return DataLoader(self.ds_train, batch_size=self.batch_size, shuffle=False, num_workers=self.num_workers)

    def val_dataloader(self):
        return DataLoader(self.ds_val, batch_size=self.batch_size, shuffle=False, num_workers=self.num_workers)


class DiscretizationCatVAE(pl.LightningModule, TimeSeriesDiscretizer):
    def __init__(self, in_dim, enc_out_dim, dec_out_dim, categorical_dim, temp, beta, batch_size=256,
                  mid_layer_sizes=256, device="cpu"):
        # parameters from hparams dictionary
        self.in_dim = in_dim
        self.enc_out_dim = enc_out_dim
        self.dec_out_dim = dec_out_dim
        self.categorical_dim = categorical_dim
        self.temp = temp
        self.beta = beta
        super(DiscretizationCatVAE, self).__init__()
        self.save_hyperparameters()

        # Build Encoder
        self.encoder = nn.Sequential(
            nn.Linear(self.in_dim, mid_layer_sizes),
            nn.ReLU(),
            nn.Linear(mid_layer_sizes, mid_layer_sizes),
            nn.ReLU(),
            nn.Linear(mid_layer_sizes, self.enc_out_dim))
        self.fc_z_cat = nn.Linear(self.enc_out_dim, self.categorical_dim)

        # Build Decoder
        self.decoder = nn.Sequential(
            nn.Linear(self.categorical_dim, 256),
            nn.ReLU(),
            nn.Linear(256, 256),
            nn.ReLU(),
            nn.Linear(256, self.dec_out_dim))
        self.fc_mu_x = nn.Linear(self.dec_out_dim, self.in_dim)
        self.fc_logvar_x = nn.Linear(self.dec_out_dim, self.in_dim)

        # Categorical prior
        self.pz = torch.distributions.OneHotCategorical(
            1. / self.categorical_dim * torch.ones(1, self.categorical_dim, device='cuda'))

        self.log_sigma = torch.nn.Parameter(torch.full((1,), 0.)[0], requires_grad=True)

    def encode(self, input: torch.Tensor) -> torch.Tensor:
        """
        Encodes the input by passing through the encoder network
        and returns the latent codes.
        :param input: (Tensor) Input tensor to encoder
        :return z_out: (Tensor) Latent code
        """
        result = self.encoder(input)
        z = self.fc_z_cat(torch.flatten(result, start_dim=1))
        z_out = z.view(-1, self.categorical_dim)
        return z_out

    def decode(self, z: torch.Tensor) -> torch.Tensor:
        """
        Computes parameters for pxz from sampels of pzx
        :param z: (Tensor)
        :return: mu (Tensor)
        :return: sigma (Tensor)
        """
        result = self.decoder(z)
        mu = self.fc_mu_x(result)
        logvar = self.fc_logvar_x(result)
        sigma = torch.cat(
            [torch.diag(torch.exp(logvar[i, :])) for i in range(z.shape[0])]
        ).view(-1, self.in_dim, self.in_dim)
        return mu, sigma

    def sample_gumble(self, logits: torch.Tensor, eps: float = 1e-7) -> torch.Tensor:
        """
        Gumbel-softmax trick to sample from Categorical Distribution
        :param logits: (Tensor) Latent Codes
        :return: (Tensor)
        """
        # Sample from Gumbel
        u = torch.rand_like(logits)
        g = - torch.log(- torch.log(u + eps) + eps)
        s = F.softmax((logits + g) / self.temp, dim=-1)
        return s

    def shared_eval(self, x: torch.Tensor):
        """
        shared computation of all steps/methods in CatVAE
        """
        # first compute parameters of categorical dist. pzx
        pzx_logits = self.encode(x[0])
        # create one hot categorical dist. object for use in loss func
        pzx = torch.distributions.OneHotCategorical(logits=pzx_logits)
        # sample from pzx
        z = self.sample_gumble(logits=pzx_logits)
        # decode into mu and sigma
        mu, sigma = self.decode(z)
        # construct multivariate distribution object for pxz
        pxz = torch.distributions.MultivariateNormal(
            loc=mu, covariance_matrix=sigma)
        return pzx_logits, pzx, mu, sigma, pxz, z

    def shared_testing(self, x: torch.Tensor):
        """
        shared computation of all steps/methods in CatVAE
        """
        # first compute parameters of categorical dist. pzx
        pzx_logits = self.encode(x)
        # create one hot categorical dist. object for use in loss func
        pzx = torch.distributions.OneHotCategorical(logits=pzx_logits)
        # sample from pzx
        z = self.sample_gumble(logits=pzx_logits)
        # decode into mu and sigma
        mu, sigma = self.decode(z)
        # construct multivariate distribution object for pxz
        pxz = torch.distributions.MultivariateNormal(
            loc=mu, covariance_matrix=sigma)
        return pzx_logits, pzx, mu, sigma, pxz, z

    def get_states(self, x: torch.Tensor):
        """
        computation of discretized states
        :param x: (Tensor)
        :return:
        """
        # first compute parameters of categorical dist. pzx
        pzx_logits = self.encode(x)
        # create one hot categorical dist. object for later use in loss func
        pzx = torch.distributions.OneHotCategorical(logits=pzx_logits)
        # sample from pzx (one hot categorical)
        z = self.sample_gumble(logits=pzx_logits)
        # compute states by using the argmax of logits
        z_states = torch.zeros(z.shape).to(device='cuda').scatter(1, torch.argmax(pzx_logits, dim=1).unsqueeze(1), 1)
        # decode into mu and sigma
        mu, sigma = self.decode(z_states)
        # construct multivariate distribution object for pxz
        pxz = torch.distributions.MultivariateNormal(
            loc=mu, covariance_matrix=sigma)
        return pzx_logits, pzx, mu, sigma, pxz, z

    def training_step(self, x, batch_idx):
        pzx_logits, pzx, mu, sigma, pxz, z = self.shared_eval(x)
        loss_dct = self.loss_function(x=x, pzx=pzx, pxz=pxz)
        self.log('Loss', loss_dct['Loss'])
        self.log('recon_loss', loss_dct['recon_loss'])
        self.log('KLD_cat', loss_dct['KLD_cat'])
        self.log('train_loss', loss_dct['Loss'])
        return loss_dct['Loss']

    def validation_step(self, x, batch_idx):
        pzx_logits, pzx, mu, sigma, pxz, z = self.shared_eval(x)
        loss_dct_val = self.loss_function(x=x, pzx=pzx, pxz=pxz)
        self.log('Loss', loss_dct_val['Loss'])
        self.log('recon_loss', loss_dct_val['recon_loss'])
        self.log('KLD_cat', loss_dct_val['KLD_cat'])
        self.log('val_loss', loss_dct_val['Loss'])
        return loss_dct_val['Loss']

    def test_step(self, x, batch_idx):
        pzx_logits, pzx, mu, sigma, pxz, z = self.shared_eval(x)
        loss_dct_test = self.loss_function(x=x, pzx=pzx, pxz=pxz)
        self.log('Loss', loss_dct_test['Loss_test'])
        self.log('recon_loss', loss_dct_test['recon_loss'])
        self.log('KLD_cat', loss_dct_test['KLD_cat'])
        return loss_dct_test['Loss']

    def anom_detect(self, x, **kwargs):
        pzx_logits, pzx, mu, sigma, pxz, z = self.shared_testing(x)
        likelihood = pxz.log_prob(x[0]).detach().cpu().numpy()
        # anom_labels_likelihood = np.where(likelihood<anom_threshold_likelihood, 1, 0)

        mse_error = ((x - mu) ** 2).mean(dim=1).detach().cpu().numpy()
        # anom_labels_mse = np.where(anom_label_mse<anom_threshold_mse, 1, 0)
        return likelihood, mse_error

    def forward(self, x: torch.Tensor, **kwargs):
        return self.shared_eval(x)

    def loss_function(self, x: torch.Tensor,
                      pzx: torch.distributions.OneHotCategorical,
                      pxz: torch.Tensor) -> dict:
        likelihood = pxz.log_prob(x[0])
        recon_loss = torch.mean(likelihood)
        # compute kl divergence for categorical dist
        kl_categorical = torch.distributions.kl.kl_divergence(pzx, self.pz)
        kl_categorical_batch = torch.mean(kl_categorical)
        loss = -recon_loss + self.beta * kl_categorical_batch
        return {'Loss': loss, 'recon_loss': recon_loss, 'KLD_cat': kl_categorical_batch}

    def configure_optimizers(self):
        optimizer = torch.optim.Adam(self.parameters(), lr=1e-4)
        return optimizer

    def function_likelihood(self, x: torch.Tensor):
        pzx_logits, pzx, mu, sigma, pxz, z = self.shared_eval(x)
        likelihood = pxz.log_prob(x)
        return likelihood

    def discret_comp(self, train, val):
        vae_data = []
        total = []
        unique_list = []

        pzx_logits, _, _, _, _, z = self.shared_testing(train)
        vae_data = torch.zeros(z.shape).to(device='cuda').scatter(1, torch.argmax(pzx_logits, dim=1).unsqueeze(1),
                                                                  1).cpu().detach().numpy()
        cats = torch.tensor(pd.DataFrame(vae_data).idxmax(axis=1))

        flattened_tensors = [tuple(tensor.tolist()) for tensor in vae_data]
        unique_tensors = list(set(flattened_tensors))
        for item in unique_tensors:
            unique_list.append(item)
        unique_list = list(set(unique_list))

        return cats, val, unique_list


def train_cat_vae(hparam_batch, time, train, states, train_names, state_names, in_dim, enc_out_dim, dec_out_dim, categorical_dim, temp, beta, batch_size=256,
                  mid_layer_sizes=256, device="cpu", random_seed=123):
    mdl = DiscretizationCatVAE(in_dim=in_dim, enc_out_dim=enc_out_dim, dec_out_dim=dec_out_dim,
                               categorical_dim=categorical_dim, temp=temp, beta=beta, batch_size=batch_size,
                               mid_layer_sizes=mid_layer_sizes, device=device)

    logger = TensorBoardLogger('lightning_logs', name='betatemp_cat30', default_hp_metric=False)
    np.random.seed(random_seed)

    data_module = DataModule(hparam_batch, time, train, states, train_names, state_names, num_workers=20,
                             train_part=0.75)
    early_stop_callback = EarlyStopping(monitor="val_loss", mode='min', patience=40)
    trainer = pl.Trainer(max_epochs=400, log_every_n_steps=10, logger=logger, accelerator='gpu', devices=1,
                         callbacks=[early_stop_callback])
    trainer.fit(mdl, data_module)



