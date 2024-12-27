import pandas as pd
import numpy as np

# Create an empty DataFrame with the desired columns
df = pd.DataFrame(columns=['A', 'B'], dtype=bool)

# Define the new indices
# new_indices = np.array([0, 114, 198, 356, 799])

# Set scalar True value for column 'A' at the specified indices
df['A'].loc[[0, 1]] = True

print(df)