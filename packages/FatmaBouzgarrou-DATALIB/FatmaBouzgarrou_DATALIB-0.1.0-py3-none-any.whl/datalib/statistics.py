import numpy as np

def calculate_mean(data):
    """Calcule la moyenne."""
    return np.mean(data)

def calculate_median(data):
    """Calcule la médiane."""
    return np.median(data)

def calculate_correlation(data1, data2):
    """Calcule la corrélation entre deux jeux de données."""
    return np.corrcoef(data1, data2)[0, 1]
