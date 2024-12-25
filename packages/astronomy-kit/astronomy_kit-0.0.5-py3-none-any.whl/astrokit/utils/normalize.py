import numpy as np

def normalize(data, method='min_max'):
    """
    Normalize the data using the specified method.
    """
    if method == 'min_max':
        return min_max_normalize(data)
    elif method == 'z_score':
        return z_score_normalize(data)
    elif method == 'decimal_scaling':
        return decimal_scaling_normalize(data)
    else:
        raise ValueError('Invalid normalization method.')

def min_max_normalize(data):
    """
    Min-Max Normalization
    Scales the data to a fixed range [0, 1].
    """
    min_val = np.min(data)
    max_val = np.max(data)
    return (data - min_val) / (max_val - min_val)

def z_score_normalize(data):
    """
    Z-Score Normalization
    Scales the data based on the mean and standard deviation.
    """
    mean = np.mean(data)
    std = np.std(data)
    return (data - mean) / std

def decimal_scaling_normalize(data):
    """
    Decimal Scaling Normalization
    Scales the data by moving the decimal point of values.
    """
    max_val = np.max(np.abs(data))
    scaling_factor = 10 ** np.ceil(np.log10(max_val))
    return data / scaling_factor