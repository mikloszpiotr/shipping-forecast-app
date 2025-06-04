# Shipping Forecast App

This Streamlit application forecasts the monthly quantity of shipped goods for the next 3 months. It is designed as a problem‐solving tool for supply‐chain teams who need to:

- **Optimize inventory levels** (avoid stockouts and overstock)  
- **Plan capacity and labor** (ensure warehouses and carriers are neither under‐ nor over‐utilized)  
- **Reduce costs** (by aligning procurement, production, and logistics)  
- **Anticipate seasonal spikes or dips** (e.g. holiday surges)

Forecasting shipping volume is critical: if you ship too many goods, you incur storage costs and tie up working capital. If you ship too few, you risk lost revenue and unhappy customers. By having a reliable 3‐month forecast, businesses can align procurement, production schedules, and logistics contracts more accurately.

---

## Folder Structure

```
shipping_forecast_app/
│
├── data/
│   └── shipping_history.csv      # Historical monthly shipping data (date, shipped_qty)
│
├── src/
│   ├── data_loader.py            # Functions to load & preprocess data
│   ├── eda.py                    # Plotting, trend/seasonality decomposition, outlier detection
│   ├── models.py                 # Wrappers for forecasting algorithms
│   ├── metrics.py                # Compute MAE, RMSE, MAPE, etc.
│   └── utils.py                  # Any shared utilities
│
├── streamlit_app.py              # Main Streamlit application
├── requirements.txt              # List of dependencies
└── README.md                     # This file
```

---

## Why Forecast Shipping?

1. **Inventory Optimization**  
   - A 3-month forecast helps determine how much raw material or finished goods to hold in warehouses.  
   - If you overestimate demand, excess stock sits idle (higher storage costs).  
   - If you underestimate demand, you risk stockouts, expedite fees, and lost sales.  

2. **Cost Control**  
   - Logistics contracts often have volume‐based pricing. If you can predict shipping volume reliably, you can negotiate better rates.  
   - Planning pick/pack labor and transportation capacity in advance avoids premium fees for last‐minute adjustments.  

3. **Production & Procurement Planning**  
   - A shipping forecast feeds directly into a Production Plan and Purchase Orders.  
   - You can align production schedules with expected shipments, reducing changeover downtime and waste.  

4. **Seasonality & Trend Management**  
   - Many industries have clear seasonal cycles (e.g., retail peaks in Q4).  
   - Detecting and planning for seasonal spikes (or dips) early allows you to pre‐book carriers, secure space, and hire temporary staff.  

In short, accurate shipping forecasts translate into lower costs, higher customer satisfaction, and more efficient operations.

---

## Forecasting Models Used

This app includes five different forecasting approaches. Each has its own strengths, assumptions, and typical use cases.

### 1. Moving Average (MA)
- **How it works:**  
  - Calculates the simple average of the last *N* months (rolling window).  
  - Uses that rolling average (e.g. 3-month average) as the forecast for each of the next 3 months.  
- **Strengths:**  
  - Easy to understand and implement.  
  - Smooths out short-term fluctuations.  
- **Limitations:**  
  - Assumes no clear trend or seasonality beyond what is captured in the window.  
  - Cannot adapt quickly to sudden changes (a big spike/dip in the window will propagate).  
- **When to use:**  
  - “Baseline” or quick sanity check when you have a stable, relatively flat series.  
  - Very small datasets where complex models cannot be reliably fitted.

### 2. ARIMA (Autoregressive Integrated Moving Average)
- **How it works:**  
  - **AR (p):** Uses past values (lagged observations) to predict current value.  
  - **I (d):** Number of differences applied to the series to make it stationary.  
  - **MA (q):** Uses past forecast errors in a regression‐like model.  
- **Strengths:**  
  - Good for non-seasonal data with a trend or small autocorrelations.  
  - Can capture short-term dependencies.  
- **Limitations:**  
  - Requires manual selection (or an automated procedure) to find optimal (p, d, q).  
  - Assumes the series is stationary (or can be made stationary via differencing).  
- **When to use:**  
  - When your shipping data shows a trend but no clear seasonality.  
  - If autocorrelations are present and a simple MA doesn’t capture them.

### 3. SARIMA (Seasonal ARIMA)
- **How it works:**  
  - Extends ARIMA with a seasonal component (P, D, Q, s), where *s* is the seasonal period (e.g. 12 for monthly data).  
  - Models both non-seasonal (p, d, q) and seasonal (P, D, Q) effects.  
- **Strengths:**  
  - Captures both trend and repeating seasonal patterns (e.g., higher shipments every December).  
  - Flexible: you can tune both seasonal and non-seasonal hyperparameters.  
- **Limitations:**  
  - Model complexity grows quickly: more parameters to tune → risk of overfitting if data history is short.  
  - Computationally more intensive than simple ARIMA.  
- **When to use:**  
  - When your shipping history clearly shows seasonal cycles (e.g., monthly, quarterly) plus a trend.  
  - When you have at least 2–3 years of monthly data so that seasonality parameters (e.g., s=12) can be estimated reliably.

### 4. Holt-Winters Exponential Smoothing (HW)
- **How it works:**  
  - Applies exponential smoothing to level, trend, and seasonality components.  
  - Assigns exponentially decreasing weights to older observations.  
- **Strengths:**  
  - Captures additive (or multiplicative) seasonality and trend without requiring explicit differencing.  
  - Fewer hyperparameters than SARIMA (you choose whether trend/seasonality are additive or multiplicative and the seasonal period).  
- **Limitations:**  
  - Cannot model complex autocorrelations beyond trend/seasonality.  
  - Less interpretable coefficients than ARIMA.  
- **When to use:**  
  - When you need a simple model that handles trend + seasonality.  
  - If ARIMA/SARIMA fit is slow or fails to converge, HW often succeeds.

### 5. Prophet (by Facebook/Meta)
- **How it works:**  
  - Decomposable additive model with built-in handling for seasonality, holidays, and trend changepoints.  
  - User supplies a DataFrame with columns `ds` (timestamp) and `y` (value).  
- **Strengths:**  
  - Automatically detects yearly, weekly, and daily seasonality; you can also add custom seasonalities.  
  - Robust to missing data and outliers.  
  - Easy to include known holidays or events that may cause anomalies.  
- **Limitations:**  
  - Can overfit if too many holidays or changepoints are specified.  
  - Less transparent “black-box” compared to ARIMA/SARIMA; tuning is more high-level.  
- **When to use:**  
  - When you want an automated pipeline that handles most seasonality/trend situations with minimal parameter tweaking.  
  - If you have irregular data (e.g., missing months) or known one-off events that must be included.

---

## Key Differences at a Glance

| Model                     | Trend Handling         | Seasonality Handling    | Data Requirements                   | Complexity     | Best For                                            |
|---------------------------|------------------------|-------------------------|-------------------------------------|----------------|-----------------------------------------------------|
| **Moving Average (MA)**   | None (flat)            | None beyond window      | Very small samples (>= window size) | Very Low       | Baseline; very stable series without trend/season.  |
| **ARIMA**                 | Explicit via differencing (d) | None (unless you manually add seasonal terms) | ≥ 3× the max(p, q) in points        | Low to Moderate | Non-seasonal series with autocorrelations & trend.  |
| **SARIMA**                | Explicit + seasonal differencing | Explicit via seasonal order (P, D, Q) | ≥ 2–3 years of monthly data          | Moderate to High | Series with both trend and clear periodic season.   |
| **Holt-Winters (HW)**     | Exponential smoothing  | Additive or multiplicative option | ≥ 2 seasonal cycles (e.g., ≥ 24 months) | Low to Moderate | Trend + seasonality where you want fewer hyperparams. |
| **Prophet**               | Piecewise linear/trend changepoints | Built-in yearly, weekly, daily; custom | ≥ 1 year of data (ideally ≥ 2 years) | Moderate       | Automated, robust to outliers, with holiday effects. |

---

## Setup & Installation

1. **Clone the repository** (or download the ZIP):  
   ```bash
   git clone https://github.com/mikloszpiotr/shipping-forecast-app.git
   cd shipping-forecast-app
   ```

2. **Create and activate a virtual environment** (strongly recommended):  
   - Windows:
     ```bash
     python -m venv .venv
     .venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```

3. **Install dependencies**:  
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Prepare your data**:  
   - Place your historical shipping data as `shipping_history.csv` in the `data/` folder.  
   - The CSV **must** have exactly two columns:  
     1. `date` in `YYYY-MM-DD` format (month’s first day)  
     2. `shipped_qty` as an integer or float.  
   - Feel free to replace the sample data with your real dataset—as long as it follows the same schema, the app will work without code changes.

---

## Running the App

From the project root, with your virtual environment active, run:

```bash
streamlit run streamlit_app.py
```

Then open your browser at `http://localhost:8501`. You’ll see three main sections:

1. **Data Visualization & EDA**  
   - View the raw time series, seasonal decomposition, and detect outliers via IQR.  

2. **Model Selection & Forecast**  
   - Choose one of the five forecasting methods (MA, ARIMA, SARIMA, Holt-Winters, Prophet).  
   - Adjust hyperparameters (e.g., window size, ARIMA p/d/q, seasonal orders, trend/seasonal types).  
   - Generate and visualize a 3-month forecast.

3. **Evaluation Metrics**  
   - Automatically compare your 3-month forecast to the actuals (last 3 months of data).  
   - See MAE, RMSE, and MAPE, plus a side-by-side Actual vs. Forecast table.

---

## How to Interpret and Use This App

1. **Start with EDA**  
   - In “Data Visualization & EDA,” look for clear trends (upward or downward) and seasonality (e.g., consistent peaks each December).  
   - If the decomposition shows strong seasonal components (large seasonal sub-series), you know SARIMA or Holt-Winters will likely outperform a simple Moving Average.

2. **Pick a Baseline Model**  
   - A 3-month Moving Average (e.g. window=3) is an easy starting point. It gives a sense of the “status quo.”  
   - Check the Evaluation Metrics: if MAE is low, maybe you don’t need something more complex.

3. **Try ARIMA or Holt-Winters**  
   - If EDA shows a clear trend without seasonality, try ARIMA.  
   - If you see trend + seasonality, Holt-Winters or SARIMA can capture both.  
   - Use the “Model Selection” page to tune hyperparameters. For SARIMA, start with `(p,d,q)=(1,1,1)` and seasonal `(P,D,Q,s)=(1,1,1,12)` as defaults.

4. **Consider Prophet for Automation**  
   - If your data has irregularities (missing months, outliers), Prophet is robust.  
   - Easily incorporate known holidays or promotions.  
   - Prophet often works well out-of-the-box—just feed it your `date`/`shipped_qty` pairs.

5. **Compare with Evaluation Metrics**  
   - The “Evaluation Metrics” page will automatically recompute MAE, RMSE, and MAPE for whichever model you most recently ran.  
   - Use these metrics to identify which model best solves your forecasting problem. For example:  
     - If SARIMA’s MAPE is significantly lower than a 3-month moving average, that indicates you do have meaningful seasonality that ARIMA alone didn’t capture.

6. **Deploy & Iterate**  
   - Once you identify the best model, you can schedule regular forecasting runs (e.g., monthly).  
   - Export forecasts into your ERP or supply-chain planning system.  
   - Periodically re‐train on new data (e.g., after each month or quarter) to keep forecasts up to date.

---

## Extending or Customizing

- **Add more models**  
  - You could integrate an LSTM/RNN (using TensorFlow or PyTorch) if you have a long history and want a deep learning approach.  
  - Consider TBATS or other advanced models if you have multiple seasonalities (e.g., weekly + yearly).

- **Add external regressors**  
  - If you know the dates of major promotions, holidays, or supply disruptions, incorporate them as covariates in ARIMAX/SARIMAX or Prophet’s holidays parameter.

- **Automate data ingestion**  
  - Instead of manually updating `shipping_history.csv`, connect directly to your database (e.g., SQL) in `data_loader.py`.  
  - Schedule a cron job or use GitHub Actions to pull fresh data, run forecasts, and store results.

- **Deploy to Streamlit Cloud or Heroku**  
  - Push your code to GitHub (which you’ve already done).  
  - Link to Streamlit Cloud and deploy in one click—your app will be live at a public URL.  

---

## Dependencies

All dependencies are listed in `requirements.txt`. Major packages include:

- `streamlit` (for the web UI)  
- `pandas` & `numpy` (data handling)  
- `matplotlib` (static plotting)  
- `statsmodels` (ARIMA, SARIMA, Holt-Winters)  
- `prophet` (Facebook/Meta’s forecasting package)  
- `scikit-learn` (for error metrics)  

You can install everything with:

```bash
pip install -r requirements.txt
```

---

## License & Contribution

This project is released under the MIT License. Feel free to fork, submit issues, or open pull requests if you’d like to add new features (e.g., additional models, data sources, or improved visualizations).

---

*By following this README, supply-chain teams or portfolio reviewers can immediately understand the motivation behind forecasting shipping volumes, see which statistical or machine‐learning methods are available, and learn how to compare and choose the right model for their needs.*  
