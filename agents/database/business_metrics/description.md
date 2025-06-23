## **Data Description: Home Loan Performance and Marketing Dataset (Jan 2022 – Jun 2025)**

### **1. Overview**

This dataset contains time-stamped measurements of key performance, pricing, marketing, and customer satisfaction metrics related to ANZ’s home loan business. It spans from **January 2022 to June 2025**, enabling longitudinal insights and business performance analysis. Each row represents a single metric observation at a given point in time.

---

### **2. Data Structure**

The dataset is in a **long format**, where each row captures the value of a single metric for a specific time period. This format enables flexible time-series analysis and efficient reporting.

#### **Current Schema**

| Column Name          | Description                                                                               |
| -------------------- | ----------------------------------------------------------------------------------------- |
| `date`               | Start date of the observation (typically the first day of the month, e.g., `2022-01-01`). |
| `metric_name`        | Name of the metric or KPI being recorded.                                                 |
| `metric_description` | Explanation of what the metric represents and how it is interpreted.                      |
| `metric_owner`       | The person accountable for monitoring or owning the metric.                               |
| `metric_value`       | The actual recorded value of the metric (numeric or percentage, depending on the metric). |
| `period_type`        | The type of time grouping used for reporting (e.g., `Calendar Period`, `Fiscal Period`).  |
| `period_value`       | The formatted label for the time period (e.g., `2022_January`, `FY2025_Q2`).              |

---

### **3. Metric Categories**

#### **A. Performance Metrics**

| `metric_name`                          | Description                                                                |
| -------------------------------------- | -------------------------------------------------------------------------- |
| Home Loan Growth Rate (%)              | Month-over-month change in total home loan balances.                       |
| Home Loan 3-Monthly Attrition Rate (%) | Percentage of customer attrition calculated over a rolling 3-month window. |
| Home Loan Application Volume           | Total number of new home loan applications.                                |
| System Growth Rate                     | Industry-level home loan portfolio growth benchmark.                       |

---

#### **B. Pricing Metrics**

| `metric_name`                             | Description                                                             |
| ----------------------------------------- | ----------------------------------------------------------------------- |
| ANZ Best Home Loan Rate (<80% LVR)        | ANZ’s most competitive rate for loans with less than 80% loan-to-value. |
| Competitor Best Home Loan Rate (<80% LVR) | Comparable rate offered by competitors for the same LVR segment.        |

---

#### **C. Marketing Metrics**

| `metric_name`                 | Description                                                             |
| ----------------------------- | ----------------------------------------------------------------------- |
| BTL Home Loan Campaign Volume | Volume of targeted BTL campaigns sent to potential home loan customers. |
| BTL Campaign Conversion Rate  | Conversion rate of BTL outreach into new home loan customers.           |
| ATL Marketing Spend (\$)      | Total investment in broad-reach ATL marketing campaigns.                |

---

#### **D. Complaints Metrics**

| `metric_name`               | Description                                        |
| --------------------------- | -------------------------------------------------- |
| Overall Complaints Volume   | Number of complaints received across all services. |
| Home Loan Complaints Volume | Subset of complaints specific to home loans.       |

---

### **4. Relationships Across Fields**

| Field                                   | Related Fields                | Description                                                          |
| --------------------------------------- | ----------------------------- | -------------------------------------------------------------------- |
| `date`                                  | `metric_name`, `metric_value` | Time anchor for every metric record.                                 |
| `metric_name`                           | `metric_owner`                | Each metric is assigned a responsible stakeholder.                   |
| `metric_value`                          | `metric_name`                 | Stores the actual numeric value associated with the named metric.    |
| `period_type/value`                     | `date`, `metric_name`         | Offers alternate time grouping for reporting (calendar or fiscal).   |
| Pricing ↔ Performance                   | —                             | Pricing metrics influence growth and attrition.                      |
| Marketing ↔ Application Volume          | —                             | Campaign effectiveness drives application volume.                    |
| Complaints ↔ Growth, Marketing, Pricing | —                             | Complaints may lag but correlate with experience and pricing shifts. |

---

### **5. Sample Record (Updated Format)**

| date       | metric\_name              | metric\_description                                                 | metric\_owner | metric\_value       | period\_type    | period\_value |
| ---------- | ------------------------- | ------------------------------------------------------------------- | ------------- | ------------------- | --------------- | ------------- |
| 2022-01-01 | Home Loan Growth Rate (%) | The month-over-month percentage change in total home loan balances. | Sophie Tan    | 0.06279107911114418 | Calendar Period | 2022\_January |