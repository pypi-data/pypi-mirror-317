# Moral88/regression.py
import numpy as np

def mean_absolute_error(y_true, y_pred):
    """
    Compute MAE (Mean Absolute Error)
    """
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    return np.mean(np.abs(y_true - y_pred))

def mean_squared_error(y_true, y_pred):
    """
    Compute MSE (Mean Squared Error)
    """
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    return np.mean((y_true - y_pred) ** 2)

def r_squared(y_true, y_pred):
    """
    Compute R-Squared
    """
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    ss_total = np.sum((y_true - np.mean(y_true)) ** 2)
    ss_residual = np.sum((y_true - y_pred) ** 2)
    return 1 - (ss_residual / ss_total)
