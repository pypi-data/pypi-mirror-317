import pandas as pd

def load_csv(filepath):
    """Charge un fichier CSV en DataFrame pandas."""
    return pd.read_csv(filepath)

def normalize_data(df):
    """Normalise les données (entre 0 et 1)."""
    return (df - df.min()) / (df.max() - df.min())

def handle_missing_values(df, method="mean"):
    """Gère les valeurs manquantes dans un DataFrame."""
    if method == "mean":
        return df.fillna(df.mean())
    elif method == "median":
        return df.fillna(df.median())
    else:
        return df.dropna()
