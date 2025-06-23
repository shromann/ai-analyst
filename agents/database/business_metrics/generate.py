import pandas as pd
import numpy as np
import yaml

# Set seed for reproducibility
np.random.seed(42)

# Create date range from Jan 2022 to Jun 2025
dates = pd.date_range(start='2022-01-01', end='2025-06-01', freq='MS')

n_months = len(dates)

# System growth rate (between 0.01% to 0.75%)
system_growth_rate = np.random.uniform(0.0001, 0.0075, n_months)

# Competitor best rate (fluctuates between 4% to 7%)
competitor_rate = np.random.uniform(0.04, 0.07, n_months)

# ANZ best home loan rate, initially random, then smoothed
anz_rate = np.random.uniform(0.035, 0.065, n_months)
anz_rate = pd.Series(anz_rate).rolling(window=3, min_periods=1).mean().values

# Home loan growth rate - strongly negatively correlated with lagged ANZ rate and slightly with competitor rate
lag_anz_rate = np.roll(anz_rate, 3)
lag_anz_rate[:3] = anz_rate[:3]  # Prevent introducing NaNs
home_loan_growth = 0.1 - lag_anz_rate * 0.7 - competitor_rate * 0.2 + system_growth_rate * 0.5
home_loan_growth += np.random.normal(0, 0.002, n_months)  # add noise

# Home loan 3-monthly attrition rate (random with slight trend)
attrition_rate = np.random.uniform(0.01, 0.03, n_months)

# Application volume (between 1000 and 5000)
application_volume = np.random.randint(1000, 5001, n_months)

# Below the line campaign volume targeting non-home loan customers
btl_campaign_volume = np.random.randint(100, 2001, n_months)

# Above the line marketing spend ($10,000 to $250,000)
atl_spend = np.random.randint(10000, 250001, n_months)

# Overall complaints volume (range 100 to 500)
overall_complaints = np.random.randint(100, 501, n_months)

# Complaints for home loan products (20% to 50% of overall)
home_loan_complaints = (overall_complaints * np.random.uniform(0.2, 0.5, n_months)).astype(int)

# BTL campaign conversion rate (2% to 8%)
btl_conversion_rate = np.random.uniform(0.02, 0.08, n_months)

# Create DataFrame
df = pd.DataFrame({
    'Date': dates,
    'Calendar Year': dates.year,
    'Month': dates.month_name(),
    'Financial Year': dates.year - dates.month // 7,
    'Quarter': (dates.month - 1) // 3 + 1,
    'Home Loan Growth Rate (%)': home_loan_growth,
    'ANZ Best Home Loan Rate (<80% LVR)': anz_rate,
    'Competitor Best Home Loan Rate (<80% LVR)': competitor_rate,
    'Home Loan 3-Monthly Attrition Rate (%)': attrition_rate,
    'Home Loan Application Volume': application_volume,
    'BTL Home Loan Campaign Volume': btl_campaign_volume,
    'ATL Marketing Spend ($)': atl_spend,
    'Overall Complaints Volume': overall_complaints,
    'Home Loan Complaints Volume': home_loan_complaints,
    'BTL Campaign Conversion Rate': btl_conversion_rate,
    'System Growth Rate': system_growth_rate
})

metric_cols = df.columns[5:]

# Load metrics.yaml
with open('metrics.yaml', 'r') as file:
    metrics_info = yaml.safe_load(file)

# Extract descriptions and owners dictionaries from loaded YAML
metric_descriptions = {k: v['description'] for k, v in metrics_info.items()}
metric_owners = {k: v['owner'] for k, v in metrics_info.items()}


df = df.melt(
    id_vars=['Date', 'Calendar Year', 'Month', 'Financial Year', 'Quarter'],
    value_vars=metric_cols,
    var_name='Metric Name',
    value_name='Metric Value'
)
df['Metric Description'] = df['Metric Name'].map(metric_descriptions)
df['Metric Owner'] = df['Metric Name'].map(metric_owners)



df.melt(
    id_vars=['Date', 'Metric Name', 'Metric Description', 'Metric Owner', 'Metric Value'], 
    value_vars=['Calendar Year', 'Month', 'Financial Year', 'Quarter'],
    var_name='Period Type',
    value_name='Period Value'
)

df['Calendar Period'] =  df['Calendar Year'].astype(str) + '_' + df['Month'].astype(str)
df['Fiscal Period'] =  'FY' + df['Financial Year'].astype(str) + '_Q' + df['Quarter'].astype(str)
df = df.melt(
    id_vars=['Date', 'Metric Name', 'Metric Description', 'Metric Owner', 'Metric Value'], 
    value_vars=['Calendar Period', 'Fiscal Period'],
    var_name='Period Type',
    value_name='Period Value'
)

df.rename(
    columns={col: col.lower().replace(' ', '_') for col in df.columns},
    inplace=True
)

df.to_csv('data.csv', index=False)