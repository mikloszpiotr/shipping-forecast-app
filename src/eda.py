import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm

def plot_time_series(df: pd.DataFrame):
    """
    Basic line plot of 'shipped_qty' over time.
    """
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(df.index, df['shipped_qty'], marker='o')
    ax.set_title("Monthly Shipped Quantity Over Time")
    ax.set_xlabel("Date")
    ax.set_ylabel("Quantity Shipped")
    return fig

def decompose_time_series(df: pd.DataFrame, model: str = 'additive'):
    """
    Decompose into trend/seasonal/residual using statsmodels.
    """
    decomposition = sm.tsa.seasonal_decompose(df['shipped_qty'], model=model)
    fig = decomposition.plot()
    fig.set_size_inches(10, 8)
    return fig

def detect_outliers(df: pd.DataFrame):
    """
    Simple IQR‐based outlier detection in monthly shipments.
    Returns a list of dates considered outliers.
    """
    q1 = df['shipped_qty'].quantile(0.25)
    q3 = df['shipped_qty'].quantile(0.75)
    iqr = q3 - q1
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr
    outlier_mask = (df['shipped_qty'] < lower) | (df['shipped_qty'] > upper)
    return df.index[outlier_mask].tolist()
