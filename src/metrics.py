import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error

def compute_mae(y_true, y_pred):
    return mean_absolute_error(y_true, y_pred)

def compute_rmse(y_true, y_pred):
    return np.sqrt(mean_squared_error(y_true, y_pred))

def compute_mape(y_true, y_pred):
    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100
