## **Data Description: Volume Forecasting Dataset (Jan 2023 – Mar 2025)**

### **1. Overview**

This dataset simulates synthetic monthly volume and forecast data across two business units—**Commercial** and **Retail**—for a range of service lines. 
The dataset is structured to include both actual and forecasted volumes, and embeds different correlation patterns between service lines (e.g. positive, negative, lead-lag, and independence).

The data is ideal for testing time-series models, evaluating forecasting accuracy under structured noise, and exploring aggregation logic across business hierarchies (streams, sub-streams, and service lines).

---

### **2. Entities and Relationships**

#### **A. Time Entity**

* **Attributes**: `date`, `year`, `month`
* **Description**: Each observation is associated with a unique month, ranging from **January 2023 to March 2025**. 
The year 2025 is designated as the forecasting horizon—actual `volume` values for this period are withheld (set to `None`) to simulate a real-world forecasting scenario.

---

#### **B. Business Unit Entity**

* **Attributes**: `business_unit` (e.g., `Commercial`, `Retail`)
* **Description**: The top-level grouping representing organizational domains. Each unit contains a complete set of service lines and related data.

---

#### **C. Stream Hierarchy**

##### **i. Stream**

* **Attributes**: `stream` (e.g., `stream_A`, `stream_B`)
* **Description**: Represents major operational groupings that encompass multiple sub-streams.

##### **ii. Sub-Stream**

* **Attributes**: `sub_stream` (e.g., `sub_stream_1`, ..., `sub_stream_4`)
* **Description**: Mid-level categorization used to group service lines under common operational themes or characteristics (e.g., correlated behaviors).

##### **iii. Service Line**

* **Attributes**: `service_line` (e.g., `service_line_1` to `service_line_8`)
* **Description**: The most granular entity. Each service line has a distinct volume time series, governed by a specific statistical pattern (e.g., correlated, lagged, independent).

| Forecast Label | Service Line     | Statistical Pattern                         | Sub-Stream     | Stream    |
| -------------- | ---------------- | ------------------------------------------- | -------------- | --------- |
| Correlated 1   | service\_line\_1 | Positively correlated with service\_line\_2 | sub\_stream\_1 | stream\_A |
| Correlated 2   | service\_line\_2 | Positively correlated with service\_line\_1 | sub\_stream\_1 | stream\_A |
| Lead           | service\_line\_3 | Leads service\_line\_4 by 1 month           | sub\_stream\_2 | stream\_A |
| Lag            | service\_line\_4 | Lags service\_line\_3 by 1 month            | sub\_stream\_2 | stream\_A |
| NegLead        | service\_line\_5 | Negative lead to service\_line\_6           | sub\_stream\_3 | stream\_B |
| NegLag         | service\_line\_6 | Negative lag to service\_line\_5            | sub\_stream\_3 | stream\_B |
| Indep 1        | service\_line\_7 | Independent random walk                     | sub\_stream\_4 | stream\_B |
| Indep 2        | service\_line\_8 | Independent random walk                     | sub\_stream\_4 | stream\_B |

---

#### **D. Metric Entity**

* **Attributes**: `volume`, `forecast`
* **Description**: These are the quantitative indicators tracked per service line per month.

  * `volume` – The actual (simulated) volume for a given service line and date. **Set to `None` in 2025** to allow forecasting model evaluation.
  * `forecast` – A noisy forecast of the volume, created by adding a small normal disturbance to the log-scale series.

**Relationships**:

* `forecast` is computed directly from `volume`, with added Gaussian noise.
* Both are **exponentiated** to simulate scale-adjusted metrics.

---

### **3. Relationships Across Entities**

| Entity            | Related Entities          | Relationship Description                                                               |
| ----------------- | ------------------------- | -------------------------------------------------------------------------------------- |
| **Time**          | All                       | Every observation is indexed to a unique month                                         |
| **Business Unit** | Stream, Sub-Stream        | Each business unit has a full set of hierarchical stream and service line groupings    |
| **Stream**        | Sub-Stream                | Each stream contains multiple sub-streams                                              |
| **Sub-Stream**    | Service Line              | Each sub-stream includes specific service lines with statistical dependency structures |
| **Service Line**  | Metric (volume, forecast) | Each service line reports actual and forecasted volumes monthly                        |

---

### **4. Dataset Format**

* **Final Data Format**: Long-form DataFrame with one row per `business_unit` × `service_line` × `date`

* **Key Columns**:

  * `date`, `year`, `month`
  * `business_unit`, `stream`, `sub_stream`, `service_line`
  * `volume`, `forecast`

* **Forecasting Test Period**: Entire year of 2025 (volume = `None`)

* **Usage Scenarios**:

  * Forecasting model development and backtesting
  * Evaluating correlation and lag effects across service lines
  * Aggregated reporting across sub-streams and streams
