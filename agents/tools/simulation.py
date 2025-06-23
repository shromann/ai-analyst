import pandas as pd
from prophet import Prophet

def _forecast(y: pd.Series, forecast_horizon: int, freq: str) -> pd.Series:
    """
    Forecast future values using Prophet directly.

    Parameters:
    - y: pd.Series with a DatetimeIndex
    - forecast_horizon: number of future periods to forecast

    Returns:
    - pd.Series: predicted values with future datetime index
    """
    if not isinstance(y.index, pd.DatetimeIndex):
        raise ValueError("Input series must have a DatetimeIndex.")

    # Prepare data for Prophet
    df = y.reset_index()
    df.columns = ['ds', 'y']

    prophet_kwargs = {
        "seasonality_mode": "multiplicative"
    }

    # Fit model
    model = Prophet(**prophet_kwargs)
    model.fit(df)

    # Create future dataframe
    future = model.make_future_dataframe(periods=forecast_horizon, freq=freq)
    forecast = model.predict(future)

    # Extract predicted values for the future only
    forecast_result = forecast.set_index("ds")["yhat"][-forecast_horizon:]

    return forecast_result
