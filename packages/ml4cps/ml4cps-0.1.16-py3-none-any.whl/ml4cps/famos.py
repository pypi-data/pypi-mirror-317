import numpy as np
from scipy.signal import find_peaks
from collections import defaultdict
from fastdtw import fastdtw
from collections import Counter
import pandas as pd
from dtaidistance import dtw


# Global variables (these need to be initialized in your code)
windowSize = None
num_ud = None
max_deriv = None
Ts = None
chp_depths = None

thresClusterMax = 1
thresClusterMin = 0.03
facThres = 2.5


def calculate_normalization(data):
    norm = np.max(np.concatenate([np.atleast_2d(np.max(np.abs(d), axis=0)) for d in data], axis=0), axis=0)
    return norm


def normalize(data):
    norm = calculate_normalization(data)
    return [d/norm for d in data]

def detect_change_points(data, num_var, window_size=10):
    """
    Detects local and global changepoints in the input and output traces.
    A sliding window approach utilizing the Euclidean distance between the
    immediate past and immediate future is used to detect changes in dynamic
    behavior on all available derivatives.
    """

    changepoints = {}
    # Process output variables
    for i in range(num_var):
        new_chp = find_changepoints(data[:, i:num_var:], 0, 0, len(data), window_size=window_size)
        changepoints[i] = pd.Series(index=new_chp, name=i, data=1, dtype=float)

    changepoints = pd.DataFrame(changepoints).sort_index().fillna(0)


    # Filter changepoints
    data, chpoints = filter_change_points(data, changepoints, window_size=window_size)
    return data, chpoints


def compute_past_future_diff_distance(array, windowSize):
    """
    Returns the similarity of the immediate past to the immediate future for all inner indices
    using the Euclidean distance metric.
    """
    array = np.asarray(array)
    dist = [0] * windowSize

    for i in range(windowSize, len(array) - windowSize):
        before = array[i - windowSize:i]
        after = array[i + 1:i + windowSize + 1]
        dist_new = np.linalg.norm((before - before[0]) - (after - after[0]))
        dist.append(dist_new)

    return np.array(dist)


def find_changepoints(data, depth, start, end, window_size, peak_height=0.001):
    """
    Recursively finds changepoints present in the interval using all available derivatives up to the selected one.
    """
    data = np.asarray(data)
    if data.ndim == 1:
        data = data.reshape(-1, 1)

    # Terminal case: If the interval is too small or the derivative depth exceeds max_depth
    if end - start - 1 < 2 * window_size:
        return []

    # Compute the current derivative and distance
    der = data[start:end, depth]
    dist = compute_past_future_diff_distance(der, window_size)

    # Find peaks in distance to indicate a change in dynamic behavior
    peaks, _ = find_peaks(dist, height=peak_height)
    locs_here = peaks + start
    locs_here = np.sort(locs_here)
    # locs_here = filter_consecutive_changepoints(locs_here, 1.5 * window_size) ?? WHY WAS THIS CALLED?

    locs = locs_here

    # Formulate new intervals for next recursion
    locs_here = np.concatenate(([start - window_size // 2], locs_here, [end + window_size // 2]))
    if depth + 1 < data.shape[1]:
        for i in range(len(locs_here) - 1):
            new_start = locs_here[i] + window_size // 2
            new_end = locs_here[i + 1] - window_size // 2
            locs_new = find_changepoints(data, depth + 1, new_start, new_end, window_size, peak_height)
            locs = np.concatenate((locs, locs_new))

    # If it's the top-most function call, consider the start and end of the trace as changepoints
    if depth == 0:
        locs = np.concatenate(([0], locs, [len(der)]))

    return locs


def filter_change_points(xout, chpoints, window_size):
    """
    Applies filtering to global and local changepoints to remove close proximity changepoints
    and ensures consistency across global and local changepoint sets.
    """

    # Remove close proximity changepoints
    chpoints = filter_consecutive_changepoints(chpoints, window_size)


    # TODO Should we here check with while loop? What should be the limit for cutting
    # Remove last segment if too short (they are already filtered)
    if (chpoints.index[-1] - chpoints.index[-2]) <= (2 * window_size):
        xout = xout[:int(chpoints.index[-2]), :]
        chpoints = chpoints.iloc[:-1]
    return xout, chpoints


def filter_consecutive_changepoints(df, max_distance):
    """
    Removes the second changepoint if two changepoints are within a specified window.
    """
    if len(df) == 0:
        return df
    return df.iloc[np.diff(df.index, prepend=df.index[0] - 2 * max_distance) > max_distance]


def cluster_segments(data, changepoints, windowSize):
    # Stack all segments together

    for ind, chp in enumerate(changepoints):
        if ind > 0:
            chp.index += changepoints[ind-1].index[-1]
            chp.drop(index=chp.index[0], inplace=True)

    changepoints = pd.concat(changepoints, axis=0)
    data = np.vstack(data)

    # columns = changepoints.columns
    # for c in columns:
    #
    # changepoints.index.name = 'Start'
    # changepoints.reset_index(drop=False, inplace=True)
    # changepoints['Finish'] = changepoints['Start'].shift(-1)

    segments = changepoints.reset_index(drop=False)
    # Compute similarity matrix which is used for clustering in the next step
    combined_metric = computeSimilarityMatrix(data, changepoints, winlen=1, offset=0)

    # Compute similarity matrix which is used for clustering in the next step
    cluster_segs = computeClustersLocal(combined_metric, changepoints, facThres)


    # Merge local clusters to global clusters, potentially refine with LMI
    # cluster_global = computeClustersGlobal(cluster_segs, changepoints)


    # Save global results into trace data structure
    # labels_num = np.unique(cluster_global[:, 0])

    # for i in range(len(data)):
    #     chpoints = data[i]["chpoints"]
    #     len_segs = len(chpoints) - 1
    #     data[i]["labels_num"] = labels_num
    #     data[i]["labels_trace"] = cluster_global[:len_segs, 0]
    #     cluster_global = cluster_global[len_segs:]

    return data


def computeSimilarityMatrix(x, changepoints, winlen, offset=0):
    combined_metric = [None] * changepoints.shape[1]

    # LOOP OVER ALL VARIABLES
    for k in range(changepoints.shape[1]):
        changepoints_var = changepoints.loc[:, k][changepoints.loc[:, k] == 1].index.values  # segIndex_var[k][0]
        num_segments_var = len(changepoints_var) - 1
        combined_curr = np.zeros((num_segments_var, num_segments_var))

        # TWO LOOPS OVER ALL SEGMENTS
        for i in range(num_segments_var):
            start_i = changepoints_var[i] + winlen
            end_i = changepoints_var[i + 1] - winlen
            seg_i = x[int(start_i):int(end_i), k + offset]

            for j in range(i, len(changepoints_var) - 1):
                start_j = changepoints_var[j] + winlen
                end_j = changepoints_var[j + 1] - winlen
                seg_j = x[int(start_j):int(end_j), k + offset]

                common_len = min(len(seg_i), len(seg_j))
                if common_len > 0:
                    incConst = 1 if offset == 0 else 0

                    # IS THIS NECESSARY? THIS CALCULATES LEFT AND RIGHT ALIGNMENT
                    sim_index_end = computeComparison(seg_i[-common_len:] - seg_i[-1] * incConst,
                                                      seg_j[-common_len:] - seg_j[-1] * incConst)
                    sim_index_start = computeComparison(seg_i[:common_len] - seg_i[0] * incConst,
                                                        seg_j[:common_len] - seg_j[0] * incConst)

                    sim_index = min(sim_index_start, sim_index_end)
                    combined_curr[i, j] = sim_index
                    combined_curr[j, i] = sim_index

        combined_metric[k] = combined_curr

    return combined_metric


def computeComparison(seg_1, seg_2):
    # dist, path = dtw.distance_fast(seg_1, seg_2, dist=2)
    dist, acc_cost_matrix = dtw.warping_paths_fast(seg_1, seg_2)
    path = dtw.best_path(acc_cost_matrix)
    i_x, i_y = zip(*path)
    diag = np.corrcoef(i_x, i_y)[0, 1]
    diag = 0.0 if np.isnan(diag) else diag
    dist /= len(i_x)

    return 0.5 * dist + 0.5 * (1 - diag)


def computeClustersLocal(combined_metric, changepoints, facThres):
    num_var = changepoints.shape[1]
    cluster_segs = []

    for k in range(num_var):
        changepoints_var = changepoints.loc[:, k][changepoints.loc[:, k] == 1].index.values
        num_segments_var = len(changepoints_var) - 1
        clusters = [{i} for i in range(num_segments_var)]
        alreadyClustered = np.zeros((num_segments_var, 2))

        for i in range(num_segments_var-1):
            thres = facThres * np.min(combined_metric[k][i, np.arange(combined_metric[k].shape[1]) != i])
            thres = max(thresClusterMin, min(thres, thresClusterMax))

            for j in range(i+1, num_segments_var):
                if combined_metric[k][i, j] > thres:
                    continue

                if alreadyClustered[j, 0] == 0 or alreadyClustered[j, 1] > combined_metric[k][i, j]:
                    if alreadyClustered[j, 0] != 0:
                        clusters[int(alreadyClustered[j, 0]) - 1].discard(j)

                    if alreadyClustered[i, 0] != 0:
                        clusters[int(alreadyClustered[i, 0]) - 1].add(j)
                        alreadyClustered[j, 0] = alreadyClustered[i, 0]
                    else:
                        clusters[i].add(j)
                        alreadyClustered[j, 0] = i + 1

                    alreadyClustered[j, 1] = combined_metric[k][i, j]

        cluster_segs.append(alreadyClustered[:, 0])

        # for d in data:
        #     chpoints_var = changepoints[k]
        #     len_segs = len(chpoints_var) - 1
        #     # d["labels_trace_per_var"][k] = cluster_segs[k][:len_segs]
        #     cluster_segs[k] = cluster_segs[k][len_segs:]

    return cluster_segs


def computeClustersGlobal(cluster_segs, changepoints):
    num_var = changepoints.shape[1]
    indices = np.ones(num_var, dtype=int)
    nextid = 0
    num_segments = len(changepoints) - 1
    cluster_global = np.zeros(num_segments, dtype=int)
    M = dict()
    for i in range(num_segments):
        key = "-".join([str(int(cluster_segs[k][indices[k] - 1])) for k in range(num_var)])

        if key not in M:
            M[key] = nextid
            nextid += 1

        cluster_global[i] = M[key]

        for k in range(num_var):
            changepoints_var = changepoints.loc[:, k][changepoints.loc[:, k] == 1].index.values
            if changepoints[i, 1] == segIndex_var[k][0][indices[k] - 1, 1]:
                indices[k] += 1

    return cluster_global


def FnDecideSimilar(i, j, clusters, alreadyClustered, combined_metric, thres):
    if combined_metric[i, j] > thres:
        return clusters, alreadyClustered

    if alreadyClustered[j, 0] == 0 or alreadyClustered[j, 1] > combined_metric[i, j]:
        if alreadyClustered[j, 0] != 0:
            clusters[int(alreadyClustered[j, 0]) - 1].discard(j)

        if alreadyClustered[i, 0] != 0:
            clusters[int(alreadyClustered[i, 0]) - 1].add(j)
            alreadyClustered[j, 0] = alreadyClustered[i, 0]
        else:
            clusters[i].add(j)
            alreadyClustered[j, 0] = i + 1

        alreadyClustered[j, 1] = combined_metric[i, j]

    return clusters, alreadyClustered


import time
from sklearn.tree import DecisionTreeClassifier
from sklearn import tree


def build_decision_tree(X, Y):
    """
    FnBuildDT trains a Decision Tree using feature vectors provided by X and classifiers provided by Y.

    Parameters:
    X (array-like): Feature matrix.
    Y (array-like): Labels/classifiers.

    Returns:
    Mdl (DecisionTreeClassifier): Trained Decision Tree model.
    impure_leaves (int): Number of impure leaves.
    num_nodes (int): Total number of nodes in the tree.
    learn_time (float): Time taken to train the model.
    """
    # Start the timer
    start_time = time.time()

    # Create and train the Decision Tree Classifier
    # Assume the first column of X (corresponding to 'state id') is categorical
    Mdl = DecisionTreeClassifier(min_samples_split=2)  # equivalent to MATLAB's 'MinParentSize',1
    Mdl.fit(X, Y)

    # End the timer and calculate the learning time
    learn_time = time.time() - start_time

    # Get the total number of nodes
    num_nodes = Mdl.tree_.node_count

    # Calculate the number of impure leaves
    # Impure leaves have non-zero impurity and are leaf nodes (no children)
    is_leaf = Mdl.tree_.children_left == -1  # Leaf nodes have no children
    impure_leaves = sum(is_leaf & (Mdl.tree_.impurity > 0))

    return Mdl, impure_leaves, num_nodes, learn_time


if __name__ == '__main__':
    # x = [1, 4, 5, 10, 12, 15, 20]
    # y = find_changepoints(x, depth=1, start=0, end=6, max_depth=1, window_size=2)
    # # y = filter_consecutive_changepoints(x, 2)
    # # y = compute_past_future_diff_distance(x, 2)
    # print(y)

    from ml4cps import examples, vis, tools

    _, data = examples.buck_converter()
    data = data[0:3]

    true_change_points = [d[0] for d in data]

    data = [d[2] for d in data]

    data = normalize(data)
    num_var = data[0].shape[1]

    data = tools.extend_derivative(data, use_derivatives=[0, 1])

    WINDOW_SIZE = 10
    change_points = []

    shortened_data = []
    for d in data:
        d, chp = detect_change_points(d, num_var,  window_size=WINDOW_SIZE)
        shortened_data.append(d)
        change_points.append(chp)


    # fig = vis.plot_timeseries(data, modedata=change_points, showlegend=True)
    # fig.update_layout(height=1000).show()
    clusters = cluster_segments(shortened_data, change_points, WINDOW_SIZE)
