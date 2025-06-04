import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from prophet import Prophet

def moving_average_forecast(train: pd.DataFrame, window: int = 3, forecast_periods: int = 3) -> pd.DataFrame:
    """
    Compute a rolling moving average on 'shipped_qty' with given window,
    then forecast the next `forecast_periods` by repeating the last MA.
    """
    ma_series = train['shipped_qty'].rolling(window=window).mean()
    last_ma = ma_series.iloc[-1]
    last_date = train.index[-1]
    future_index = pd.date_range(start=last_date + pd.DateOffset(months=1),
                                 periods=forecast_periods, freq='MS')
    forecast_values = np.repeat(last_ma, forecast_periods)
    forecast_df = pd.DataFrame({'date': future_index, 'forecast': forecast_values})
    forecast_df.set_index('date', inplace=True)
    return forecast_df

def arima_forecast(train: pd.DataFrame, order: tuple = (1, 1, 1), forecast_periods: int = 3) -> pd.DataFrame:
    model = ARIMA(train['shipped_qty'], order=order)
    fitted = model.fit()
    pred = fitted.get_forecast(steps=forecast_periods)
    forecast_df = pred.predicted_mean.to_frame(name='forecast')
    return forecast_df

def sarima_forecast(train: pd.DataFrame, order: tuple = (1, 1, 1), seasonal_order: tuple = (1, 1, 1, 12), forecast_periods: int = 3) -> pd.DataFrame:
    model = SARIMAX(train['shipped_qty'], order=order, seasonal_order=seasonal_order, enforce_stationarity=False, enforce_invertibility=False)
    fitted = model.fit(disp=False)
    pred = fitted.get_forecast(steps=forecast_periods)
    forecast_df = pred.predicted_mean.to_frame(name='forecast')
    return forecast_df

def prophet_forecast(train: pd.DataFrame, forecast_periods: int = 3) -> pd.DataFrame:
    df_prop = train.reset_index().rename(columns={'date': 'ds', 'shipped_qty': 'y'})
    m = Prophet(yearly_seasonality=True, weekly_seasonality=False, daily_seasonality=False)
    m.fit(df_prop)
    future = m.make_future_dataframe(periods=forecast_periods, freq='MS')
    fcst = m.predict(future)
    # Only return the forecast for the last `forecast_periods` rows
    fcst_indexed = fcst[['ds', 'yhat']].set_index('ds').iloc[-forecast_periods:]
    fcst_indexed = fcst_indexed.rename(columns={'yhat': 'forecast'})
    return fcst_indexed

def hw_forecast(train: pd.DataFrame, seasonal_periods: int = 12, trend: str = 'add', seasonal: str = 'add', forecast_periods: int = 3) -> pd.DataFrame:
    model = ExponentialSmoothing(train['shipped_qty'], trend=trend, seasonal=seasonal, seasonal_periods=seasonal_periods)
    fitted = model.fit()
    forecast = fitted.forecast(forecast_periods)
    return forecast.to_frame(name='forecast')
