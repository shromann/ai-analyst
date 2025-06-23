import pandas as pd
import numpy as np
import yaml

# Load the YAML file
with open('volume_forecasts/structure.yaml', 'r') as file:
    metadata = yaml.safe_load(file)

forecast_name_map = metadata['forecast_name']
sub_stream_map = metadata['sub_stream']
stream_map = metadata['stream']

def generate_volume_data(business_unit, n_months, seed=42):
    np.random.seed(seed)

    dates = pd.date_range(start="2023-01-01", periods=n_months, freq="MS")

    base = np.cumsum(np.random.normal(0, 0.5, n_months))
    series1 = base + np.random.normal(0, 0.2, n_months)
    series2 = base + np.random.normal(0, 0.2, n_months)

    series3 = np.cumsum(np.random.normal(0, 0.2, n_months))
    series4 = np.roll(series3, 1)
    series4[0] = series4[1]

    series5 = np.cumsum(np.random.normal(0, 0.2, n_months))
    series6 = np.roll(-series5, 1)
    series6[0] = series6[1]

    series7 = np.cumsum(np.random.normal(0, 0.2, n_months))
    series8 = np.cumsum(np.random.normal(0, 0.2, n_months))

    ts_df = pd.DataFrame({
        "date": dates,
        "Correlated 1": series1,
        "Correlated 2": series2,
        "Lead": series3,
        "Lag": series4,
        "NegLead": series5,
        "NegLag": series6,
        "Indep 1": series7,
        "Indep 2": series8
    })

    ts_df.rename(columns=forecast_name_map, inplace=True)

    df = ts_df.melt(ignore_index=True, value_vars=ts_df.columns[1:], id_vars=["date"], var_name="service_line", value_name="volume")
    df['forecast'] = df['volume'] + np.random.normal(0, 0.2, len(df)).round(2)

    df[['forecast', 'volume']] = 100 * df[['forecast', 'volume']].map(np.exp)

    # Map sub_stream based on service_line
    # Inverse the sub_stream_map for quick lookup:
    service_line_to_sub_stream = {}
    for sub_stream, service_lines in sub_stream_map.items():
        for sl in service_lines:
            service_line_to_sub_stream[sl] = sub_stream

    df['sub_stream'] = df['service_line'].map(service_line_to_sub_stream)

    # Map stream based on sub_stream
    # Inverse the stream_map for quick lookup:
    sub_stream_to_stream = {}
    for stream, sub_streams in stream_map.items():
        for ss in sub_streams:
            sub_stream_to_stream[ss] = stream

    df['stream'] = df['sub_stream'].map(sub_stream_to_stream)

    df['business_unit'] = business_unit

    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df.loc[df['year'] == 2025, ['volume']] = None

    return df


df = pd.concat([
    generate_volume_data("Commercial", 27, seed=42),
    generate_volume_data("Retail", 27, seed=41)
])

df.to_csv("volume_forecasts/data.csv", index=False)
