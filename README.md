# Geothermal Engineering: Polynomial Regression Models

**Course:** Machine Learning  
**Assignment:** Polynomial Regression  
**Student Roll No:** IMT2024072  
**Implementation Framework:** `scikit-learn`  

---

## 1. Project Overview

This repository implements optimal **Polynomial Regression** models for two distinct engineering problems in a multi-stage geothermal energy project:

1. **Problem 1 (Phase 1 — Steam Turbine Optimization `var1`):**  
   Optimizing surface turbine efficiency governed by six operational parameters:
   - $x_1$: High-pressure steam valve adjustment
   - $x_2$: Condenser coolant flow rate adjustment
   - $x_3$: Re-injection pump hydraulic pressure
   - $x_4$: Turbine blade pitch angle
   - $x_5$: Non-condensable gas exhaust valve rate
   - $x_6$: Steam inlet pressure adjustment  
   **Target ($y$):** Net Power Score

2. **Problem 2 (Phase 2 — Subterranean Thermal Reservoir Mapping `var2`):**  
   Spatial 3D interpolation of subsurface heat map anomalies across prospective geothermal extraction sites:
   - $x_1$: East-West coordinate offset (m)
   - $x_2$: North-South coordinate offset (m)
   - $x_3$: Vertical depth offset relative to basecamp (m)  
   **Target ($y$):** Thermal Anomaly Score

---

## 2. Model Selection & Empirical Findings

Using strict **5-fold cross-validation** (`KFold(n_splits=5, shuffle=True, random_state=42)`), we evaluated feature subsets, polynomial degree sweeps, and regularization.

### Summary of Selected Architectures

| Problem | Features Used | Optimal Degree | Total Basis Terms | 5-Fold CV MSE | 5-Fold CV $R^2$ | Train $R^2$ |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **Phase 1 (`var1`)** | All 6 features ($x_1, \dots, x_6$) | **4** | **210** | **0.9618 ± 0.1508** | **0.9043 ± 0.0189** | 0.9574 |
| **Phase 2 (`var2`)** | All 3 features ($x_1, x_2, x_3$) | **8** | **165** | **0.2523 ± 0.0275** | **0.9946 ± 0.0008** | 0.9966 |

### Key Observations:
- **Phase 1 (`var1`):**  
  - Feature ablation confirmed all 6 physical operational parameters are essential; any subset (e.g., omitting coolant rate $x_2$ or blade pitch $x_4$) caps $R^2$ under $0.63$.
  - Degrees 1–3 underfit ($R^2$ progresses from $0.0937$ to $0.8965$).  
  - **Degree 4 achieves the global minimum CV MSE (0.9618) and peak $R^2$ (0.9043)**.  
  - Degree 5 introduces 462 terms, causing severe overfitting (CV MSE balloons to $2.2071$).

- **Phase 2 (`var2`):**  
  - Single-variable models (such as $x_1$ alone) fail completely ($R^2 \approx 0.0787$), as convective subsurface heat structures depend inherently on the 3D manifold.
  - As degree increases from 4 to 8, validation MSE plummets by >93% (from $3.9875$ to $0.2523$).  
  - **Degree 8 achieves the global minimum CV MSE (0.2523) and peak $R^2$ (0.9946)** with lowest inter-fold variance (±0.0275).  
  - Degrees $\ge 9$ plateau and exhibit slight overparameterization.

---

## 3. Repository Structure

```text
├── IMT2024072/
│   └── IMT2024072/
│       ├── IMT2024072_train_var1.csv   # Training data for Problem 1
│       ├── IMT2024072_test_var1.csv    # Test features for Problem 1
│       ├── IMT2024072_train_var2.csv   # Training data for Problem 2
│       └── IMT2024072_test_var2.csv    # Test features for Problem 2
├── polynomial_regression.py            # Primary standalone training & inference script
├── generate_report_figures.py          # Script generating report visualization plots
├── generate_pdf_report.py              # Script generating the 4-page academic PDF report
├── IMT2024072_Report.pdf               # Final 4-page academic submission report
├── IMT2024072_pred_var1.csv            # Final predictions for Problem 1 (test set)
├── IMT2024072_pred_var2.csv            # Final predictions for Problem 2 (test set)
├── regression_plots.png                # CV curves, Actual vs Predicted diagnostics
├── residual_plots.png                  # Residual homoscedasticity diagnostics
├── requirements.txt                    # Project dependencies
└── README.md                           # Documentation & reproduction instructions
```

---

## 4. How to Reproduce

### 4.1 Prerequisites & Setup

Install the required Python packages (Python 3.9+ recommended):

```bash
pip install -r requirements.txt
```

### 4.2 Run Training & Generate Predictions

Execute the complete scikit-learn training and prediction pipeline:

```bash
python polynomial_regression.py
```

This will:
1. Load `IMT2024072_train_var1.csv` and `IMT2024072_train_var2.csv`.
2. Compute 5-fold cross-validation metrics for both problems.
3. Fit the optimal degree-4 (var1) and degree-8 (var2) polynomial pipelines.
4. Generate the submission-ready prediction files `IMT2024072_pred_var1.csv` and `IMT2024072_pred_var2.csv`.
5. Export diagnostic fit and residual plots.

### 4.3 Rebuild the PDF Report

To re-generate the 4-page academic report:

```bash
python generate_report_figures.py
python generate_pdf_report.py
```

Output: `IMT2024072_Report.pdf`
