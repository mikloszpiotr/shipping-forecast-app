import streamlit as st
import pandas as pd

from src.data_loader import load_shipping_data, train_test_split_ts
from src.eda import plot_time_series, decompose_time_series, detect_outliers
from src.models import (
    moving_average_forecast,
    arima_forecast,
    sarima_forecast,
    prophet_forecast,
    hw_forecast
)
from src.metrics import compute_mae, compute_rmse, compute_mape

st.set_page_config(page_title="Shipping Forecast Dashboard", layout="wide")
st.title("📦 Shipping Forecast Dashboard")

pages = ["Data Visualization & EDA", "Model Selection & Forecast", "Evaluation Metrics"]
choice = st.sidebar.selectbox("Choose a page", pages)

@st.cache_data
def load_data():
    df = load_shipping_data("data/shipping_history.csv")
    return df

df = load_data()
train, test = train_test_split_ts(df, test_months=3)

if choice == "Data Visualization & EDA":
    st.header("1. Data Visualization & EDA")
    st.write("Here you can see the raw time series and decomposition.")

    fig1 = plot_time_series(df)
    st.pyplot(fig1)

    model_type = st.radio("Decomposition Model Type", options=["additive", "multiplicative"])
    fig2 = decompose_time_series(df, model=model_type)
    st.pyplot(fig2)

    outliers = detect_outliers(df)
    if outliers:
        st.write(f"Detected outliers at: {', '.join([d.strftime('%Y-%m') for d in outliers])}")
    else:
        st.write("No major outliers detected via IQR method.")

elif choice == "Model Selection & Forecast":
    st.header("2. Model Selection & Forecast")
    st.write("Choose a forecasting model and see its 3‐month forecast.")

    model_options = [
        "Moving Average",
        "ARIMA",
        "SARIMA",
        "Holt‐Winters (Exponential Smoothing)",
        "Prophet (Facebook Prophet)"
    ]
    selected_model = st.selectbox("Select Model", model_options)

    if selected_model == "Moving Average":
        window = st.slider("Moving Average Window (months)", min_value=2, max_value=12, value=3)
        forecast_df = moving_average_forecast(train, window=window, forecast_periods=3)

    elif selected_model == "ARIMA":
        p = st.number_input("p (AR order)", min_value=0, max_value=5, value=1)
        d = st.number_input("d (Difference order)", min_value=0, max_value=2, value=1)
        q = st.number_input("q (MA order)", min_value=0, max_value=5, value=1)
        forecast_df = arima_forecast(train, order=(p, d, q), forecast_periods=3)

    elif selected_model == "SARIMA":
        p = st.number_input("p (AR order)", min_value=0, max_value=3, value=1)
        d = st.number_input("d (diff order)", min_value=0, max_value=2, value=1)
        q = st.number_input("q (MA order)", min_value=0, max_value=3, value=1)
        P = st.number_input("P (seasonal AR)", min_value=0, max_value=2, value=1)
        D = st.number_input("D (seasonal diff)", min_value=0, max_value=1, value=1)
        Q = st.number_input("Q (seasonal MA)", min_value=0, max_value=2, value=1)
        s = st.number_input("Seasonal Period (e.g. 12 for monthly)", min_value=2, max_value=24, value=12)
        forecast_df = sarima_forecast(train, order=(p, d, q), seasonal_order=(P, D, Q, s), forecast_periods=3)

    elif selected_model == "Holt‐Winters (Exponential Smoothing)":
        trend = st.selectbox("Trend Component", ["add", "mul", None])
        seasonal = st.selectbox("Seasonal Component", ["add", "mul", None])
        sp = st.number_input("Seasonal Period", min_value=2, max_value=24, value=12)
        forecast_df = hw_forecast(train, seasonal_periods=sp, trend=trend, seasonal=seasonal, forecast_periods=3)

    else:  # Prophet
        forecast_df = prophet_forecast(train, forecast_periods=3)

    st.session_state["last_forecast_df"] = forecast_df
    st.session_state["last_model"] = selected_model

    st.subheader("Forecast for Next 3 Months")
    st.line_chart(pd.concat([train['shipped_qty'], forecast_df['forecast']], axis=0))
    st.table(forecast_df.rename_axis("Date").reset_index())

elif choice == "Evaluation Metrics":
    st.header("3. Evaluation Metrics")
    st.write("Compare your chosen model’s 3‐month forecast against actuals:")

    if "last_forecast_df" not in st.session_state:
        st.write("⚠️ Please go back to ‘Model Selection & Forecast’ and generate a forecast first.")
    else:
        forecast_df = st.session_state["last_forecast_df"]
        y_true = test['shipped_qty']
        y_pred = forecast_df['forecast']

        mae = compute_mae(y_true, y_pred)
        rmse = compute_rmse(y_true, y_pred)
        mape = compute_mape(y_true, y_pred)

        st.metric("MAE", f"{mae:.2f}")
        st.metric("RMSE", f"{rmse:.2f}")
        st.metric("MAPE", f"{mape:.2f}%")

        st.write("Actual vs. Forecast:")
        comparison = pd.DataFrame({
            "Actual": y_true,
            "Forecast": y_pred
        })
        st.table(comparison.rename_axis("Date").reset_index())
