import numpy as np

def scale_features(data, method="zscore"):
    """
    Scales numerical features using z-score normalization or min-max scaling.

    Parameters:
    data (numpy.ndarray): A 2D array where rows represent samples and columns represent features.
    method (str): The scaling method to use. Options are "zscore" (default) or "minmax".

    Returns:
    numpy.ndarray: A scaled version of the input data.
    """
    if not isinstance(data, np.ndarray):
        raise ValueError("Input data must be a numpy ndarray.")
    
    if method == "zscore":
        
        mean = np.mean(data, axis=0)
        std = np.std(data, axis=0)
        scaled_data = (data - mean) / std
    elif method == "minmax":
        min_val = np.min(data, axis=0)
        max_val = np.max(data, axis=0)
        scaled_data = (data - min_val) / (max_val - min_val)
    else:
        raise ValueError("Invalid scaling method. Choose 'zscore' or 'minmax'.")
    
    return scaled_data
