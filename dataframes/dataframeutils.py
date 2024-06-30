import numpy as np
import pandas as pd

#Chat GPT wrote this function
def downsample_dataframe(df, column1, column2, n_samples):
    # Calculate the step size for downsampling
    step = len(df) // n_samples
    
    # Downsample the first column by taking evenly spaced samples
    downsampled_column1 = df[column1][::step].reset_index(drop=True)
    
    # Downsample the second column by taking the average of complex numbers in each window
    downsampled_column2 = []
    for i in range(0, len(df[column2]), step):
        window = df[column2][i:i+step]
        avg_complex = np.mean(window)
        downsampled_column2.append(avg_complex)

    downsampled_column2 = pd.Series(downsampled_column2)
    
    return downsampled_column1, downsampled_column2