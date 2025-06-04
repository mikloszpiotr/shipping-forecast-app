import pandas as pd

def load_shipping_data(path: str) -> pd.DataFrame:
    """
    Reads a CSV with columns ['date', 'shipped_qty'].
    Parses 'date' as datetime and sets it as index (frequency='MS' for monthly).
    """
    df = pd.read_csv(path, parse_dates=['date'])
    df = df.sort_values('date').reset_index(drop=True)
    df.set_index('date', inplace=True)
    # Ensure it’s monthly frequency (first day of each month):
    df = df.asfreq('MS')
    return df

def train_test_split_ts(df: pd.DataFrame, test_months: int = 3) -> (pd.DataFrame, pd.DataFrame):
    """
    Splits last `test_months` for testing, rest for training.
    E.g. if df has 36 rows and test_months=3, train=first 33, test=last 3.
    """
    train = df.iloc[:-test_months]
    test = df.iloc[-test_months:]
    return train, test
