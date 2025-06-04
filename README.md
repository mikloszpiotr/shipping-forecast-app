# Shipping Forecast App

This Streamlit application forecasts the quantity of shipped goods for the next 3 months using various time series models.

## Folder Structure

```
shipping_forecast_app/
│
├── data/
│   └── shipping_history.csv      # Place your historical shipping data here.
│
├── src/
│   ├── data_loader.py            # Functions to load & preprocess data.
│   ├── eda.py                    # Functions for plotting & detecting trends/outliers.
│   ├── models.py                 # Wrappers for forecasting algorithms.
│   ├── metrics.py                # Compute MAE, RMSE, MAPE, etc.
│   └── utils.py                  # Any shared utilities.
│
├── streamlit_app.py              # Main Streamlit application.
├── requirements.txt              # List of dependencies.
└── README.md                     # This file.
```

## Setup & Installation

1. **Clone the repository** or download the folder.
2. **Install dependencies**:
   ```
   pip install -r requirements.txt
   ```
3. **Prepare data**:
   - Place your historical shipping data as `shipping_history.csv` in the `data/` directory.
   - The CSV should have two columns: `date` (YYYY-MM-DD) and `shipped_qty`.

## Running the App

From the root directory:
```
streamlit run streamlit_app.py
```

This will launch the Streamlit app at `http://localhost:8501/`.

## Features

1. **Data Visualization & EDA**: View the time series, seasonal decomposition, and detect outliers.
2. **Model Selection & Forecast**: Choose from Moving Average, ARIMA, SARIMA, Holt-Winters, or Prophet, tune hyperparameters, and view a 3-month forecast.
3. **Evaluation Metrics**: Compare forecasts against actual data (last 3 months) using MAE, RMSE, and MAPE.

Feel free to customize and extend this application for your portfolio or production use!
