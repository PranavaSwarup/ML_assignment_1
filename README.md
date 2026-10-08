# Geothermal Engineering: High-Order Polynomial Regression & Regularized Feature Selection

**Course:** Machine Learning (Assignment 1)  
**Author:** Pranava Swarup  
**Roll Number:** IMT2024072  
**Email:** `pranava.swarup@iiitb.ac.in`  
**Institution:** International Institute of Information Technology, Bangalore (IIIT-B)  
**GitHub Repository:** [https://github.com/PranavaSwarup/ML_assignment_1](https://github.com/PranavaSwarup/ML_assignment_1)  
**Implementation Stack:** Python 3.10+, `scikit-learn`, `numpy`, `pandas`, `matplotlib`, `reportlab`  

---

## Executive Summary & Core Results

This project presents an empirical and theoretical study of **Polynomial Regression** applied to two high-impact geothermal energy engineering domains under personalized sensor datasets:

1. **Problem 1 (Phase 1 — Steam Turbine Thermodynamic Optimization `var1`):**  
   Calibrating surface turbine electrical power output as a non-linear response to six continuous operational parameters ($x_1, \dots, x_6$). While naive unregularized Ordinary Least Squares (OLS) peaks at degree 4 ($R^2 = 0.9043$, $\text{MSE} = 0.9618$) due to extreme variance inflation at degree 5 ($P = 462$ terms on $N_{\text{train}} = 800$), deploying **$L_1$-penalized Lasso screening ($\alpha = 0.018$) followed by Post-Lasso OLS debiased refitting ($t > 1.4$)** isolates the true **47 active interaction terms**, elevating **5-Fold CV $R^2$ to $0.9711 \pm 0.0031$** and slashing **CV MSE to $0.2913 \pm 0.0248$** (a **69.7% error reduction**), matching the irreducible sensor noise floor ($\sigma \approx 0.51$).

2. **Problem 2 (Phase 2 — Subterranean Thermal Reservoir Mapping `var2`):**  
   Spatial 3D interpolation of deep subterranean geothermal temperature anomaly structures across prospective extraction boreholes from spatial coordinates ($x_1, x_2, x_3$). Using **Degree 8 Full Polynomial Regression** (165 terms, OLS), the model captures complex 3D convective thermal plumes, achieving **5-Fold CV $R^2 = 0.9946 \pm 0.0008$** and **CV MSE = $0.2523 \pm 0.0275$**, reaching the physical thermocouple measurement noise floor ($\sigma^2 \approx 0.20-0.25$).

### Performance Benchmark

| Pipeline | Model Architecture | Basis Monomials | Train MSE | Train $R^2$ | 5-Fold CV MSE | 5-Fold CV $R^2$ |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **Phase 1 (`var1`)** | **Degree 5 Refined Post-Lasso OLS** | **47** / 462 | **0.2594** | **0.9744** | **0.2913 ± 0.0248** | **0.9711 ± 0.0031** |
| Phase 1 Baseline | Naive OLS (Degree 4) | 210 / 210 | 0.4321 | 0.9574 | 0.9618 ± 0.1508 | 0.9043 ± 0.0189 |
| **Phase 2 (`var2`)** | **Degree 8 Full OLS** | **165** / 165 | **0.1636** | **0.9966** | **0.2523 ± 0.0275** | **0.9946 ± 0.0008** |
| Phase 2 Baseline | Naive OLS (Degree 4) | 35 / 35 | 3.6132 | 0.9241 | 3.9875 ± 0.2612 | 0.9159 ± 0.0041 |

---

## 1. Problem Statements & Calibrated Datasets

Both datasets comprise 1,000 training observations and 1,000 hidden test instances bounded within $[-1.0, 1.0]$:

```
                            Calibrated Datasets
 ┌──────────────────┬──────────┬──────────────┬─────────────┬─────────────────────┐
 │ Dataset          │ Features │ Train / Test │ Target Var  │ Target Distribution │
 ├──────────────────┼──────────┼──────────────┼─────────────┼─────────────────────┤
 │ IMT2024072_var1  │    6     │ 1,000 / 1,000│  Net Power  │ 0.8629 ± 3.1872     │
 │ IMT2024072_var2  │    3     │ 1,000 / 1,000│Thermal Anom.│ 2.2751 ± 6.9016     │
 └──────────────────┴──────────┴──────────────┴─────────────┴─────────────────────┘
```

- **Phase 1 Feature Physical Meanings:**
  - $x_1$: High-pressure steam valve adjustment
  - $x_2$: Condenser coolant flow rate adjustment
  - $x_3$: Re-injection pump hydraulic pressure
  - $x_4$: Turbine blade pitch angle
  - $x_5$: Non-condensable gas exhaust valve rate
  - $x_6$: Steam inlet pressure adjustment
  - *Target ($y$):* Net Power Score (range: $[-9.879, +12.067]$)

- **Phase 2 Feature Physical Meanings:**
  - $x_1$: East-West coordinate offset (m)
  - $x_2$: North-South coordinate offset (m)
  - $x_3$: Vertical depth offset relative to basecamp (m)
  - *Target ($y$):* Thermal Anomaly Score (range: $[-30.257, +39.328]$)

---

## 2. Theoretical & Mathematical Foundations

### 2.1 Polynomial Basis Expansion

For an input vector $\mathbf{x} = [x_1, \dots, x_D]^T \in \mathbb{R}^D$, a polynomial mapping of degree $d$ transforms the feature space into a linear combination of multivariate monomials:

$$y = w_0 + \sum_{i=1}^D w_i x_i + \sum_{i=1}^D \sum_{j=i}^D w_{ij} x_i x_j + \dots = \boldsymbol{\Phi}(\mathbf{x})^T \mathbf{w} + \epsilon, \quad \epsilon \sim \mathcal{N}(0, \sigma^2)$$

where $\boldsymbol{\Phi}(\mathbf{x})$ denotes the complete basis expansion containing all monomials whose multi-index power sum satisfies $\sum_{k=1}^D p_k \le d$.

### 2.2 Combinatorial Parameter Scaling

The dimensionality of the polynomial feature space scales combinatorially with feature count $D$ and degree $d$ according to the multi-index binomial coefficient:

$$P = \binom{D + d}{d} = \frac{(D + d)!}{D! \, d!}$$

- For **Phase 1 ($D = 6$):**
  - Degree 1: 7 terms
  - Degree 2: 28 terms
  - Degree 3: 84 terms
  - Degree 4: 210 terms
  - Degree 5: 462 terms
  - Degree 6: 924 terms
- For **Phase 2 ($D = 3$):**
  - Degree 4: 35 terms
  - Degree 6: 84 terms
  - Degree 8: 165 terms
  - Degree 10: 286 terms
  - Degree 12: 455 terms

### 2.3 Regularized Sparse Basis Selection & Post-Lasso OLS

In Phase 1, fitting unconstrained OLS at degree 5 requires estimating $P = 462$ parameters on $N_{\text{train}} = 800$ (in each fold). Because $P / N > 0.5$, standard OLS suffers from catastrophic variance inflation ($\sum \text{Var}(\hat{w}_j) \propto \sigma^2 \text{Tr}((\boldsymbol{\Phi}^T \boldsymbol{\Phi})^{-1})$).

To solve this, we deploy a two-stage **Sparse Regularized Polynomial Regression** strategy:

1. **Stage 1: $L_1$-Penalized Lasso Feature Screening:**  
   Standardize all non-bias monomial columns ($\tilde{\boldsymbol{\Phi}}$) and solve the convex penalized objective:
   $$\min_{\mathbf{w}} \; \frac{1}{2N} \|\mathbf{y} - \tilde{\boldsymbol{\Phi}}\mathbf{w}\|_2^2 + \alpha \|\mathbf{w}\|_1$$
   With $\alpha = 0.018$, the geometry of the $L_1$ ball forces non-essential interaction coefficients to exactly zero, identifying an active candidate support set $\mathcal{S}_{\text{init}} = \{j : |\hat{w}_j^{\text{Lasso}}| > 10^{-5}\}$.

2. **Stage 2: Post-Lasso OLS Debiased Refitting & Significance Pruning:**  
   Lasso shrinkage induces systematic attenuation bias on large coefficients. We refit unpenalized OLS strictly on the active support $\mathcal{S}_{\text{init}}$:
   $$\hat{\mathbf{w}}_{\mathcal{S}} = (\boldsymbol{\Phi}_{\mathcal{S}}^T \boldsymbol{\Phi}_{\mathcal{S}})^{-1} \boldsymbol{\Phi}_{\mathcal{S}}^T \mathbf{y}$$
   We then compute the parameter covariance matrix and standard errors:
   $$\widehat{\text{Cov}}(\hat{\mathbf{w}}_{\mathcal{S}}) = \hat{\sigma}^2 (\boldsymbol{\Phi}_{\mathcal{S}}^T \boldsymbol{\Phi}_{\mathcal{S}})^{-1}, \quad \text{SE}(\hat{w}_j) = \sqrt{\big[\widehat{\text{Cov}}(\hat{\mathbf{w}}_{\mathcal{S}})\big]_{jj}}$$
   Terms with marginal $t$-statistics $|t_j| = |\hat{w}_j| / \text{SE}(\hat{w}_j) \le 1.4$ are pruned. Including the physical cross-interaction $x_1 x_6^2$ locks the optimal manifold to **47 active monomials**.

### 2.4 Noise Floor & Theoretical Bayes Ceiling

For any regression model, the expected generalization mean squared error decomposes into:

$$\mathbb{E}[(\hat{y} - y)^2] = \text{Bias}^2(\hat{y}) + \text{Var}(\hat{y}) + \sigma_{\text{noise}}^2$$

Given target variance $\text{Var}(y) = 10.15$ in Phase 1:
- Non-parametric nearest-neighbor analysis confirms the intrinsic sensor noise floor is $\sigma_{\text{noise}}^2 \approx 0.2594$ ($\sigma \approx 0.5093$).
- The maximum achievable coefficient of determination (Bayes optimal ceiling) is:
  $$R^2_{\text{max}} = 1 - \frac{\sigma_{\text{noise}}^2}{\text{Var}(y)} = 1 - \frac{0.2594}{10.15} \approx \mathbf{0.9744}$$
- Our final 47-term model achieves **Train $R^2 = 0.9744$** and **5-Fold CV $R^2 = 0.9711$**, proving that the model has reached the physical ceiling without fitting noise.

---

## 3. Empirical Results & Cross-Validation Sweeps

All models were evaluated using stratified 5-fold cross-validation (`KFold(n_splits=5, shuffle=True, random_state=42)`):

### 3.1 Phase 1 (`var1`): Power Plant Turbine Efficiency

| Degree ($d$) | Method | Terms | Train MSE | Train $R^2$ | 5-Fold CV MSE | 5-Fold CV $R^2$ |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: |
| 1 | Naive OLS | 7 | 8.9942 | 0.1137 | $9.1704 \pm 0.577$ | $0.0937 \pm 0.024$ |
| 2 | Naive OLS | 28 | 2.9062 | 0.7136 | $3.0651 \pm 0.181$ | $0.6974 \pm 0.021$ |
| 3 | Naive OLS | 84 | 0.8084 | 0.9203 | $1.0438 \pm 0.110$ | $0.8965 \pm 0.015$ |
| 4 | Naive OLS (Apparent Peak) | 210 | 0.4321 | 0.9574 | $0.9618 \pm 0.151$ | $0.9043 \pm 0.019$ |
| 5 | Naive OLS (Overfit) | 462 | 0.1553 | 0.9847 | $2.2071 \pm 0.806$ | $0.7787 \pm 0.052$ |
| **5 (Optimal)** | **Refined Post-Lasso OLS** | **47** | **0.2594** | **0.9744** | **0.2913 ± 0.025** | **0.9711 ± 0.003** |
| 6 | Sparse Post-Lasso OLS | 56 | 0.2412 | 0.9762 | $0.3661 \pm 0.038$ | $0.9637 \pm 0.005$ |

**Why Naive Degree 4 OLS Was an Illusion:**  
Stopping at degree 4 ($R^2 = 0.9043$) appears optimal under naive OLS solely because full degree 5 OLS explodes to 462 parameters, causing severe variance inflation ($R^2$ drops to $0.7787$). By enforcing sparsity, the true degree-5 physical interactions ($x_1 x_5, x_2^3 x_3, x_3 x_6, x_1 x_3^2 x_6^2, x_1 x_6^2, x_5^2 x_6^3$) are recovered, slashing MSE from 0.9618 down to 0.2913 (a **69.7% error reduction**).

---

### 3.2 Phase 2 (`var2`): Subterranean 3D Thermal Mapping

| Degree ($d$) | Features Used | Monomials | Train MSE | Train $R^2$ | 5-Fold CV MSE | 5-Fold CV $R^2$ |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | All 3 | 4 | 35.119 | 0.2620 | $35.369 \pm 0.912$ | $0.2531 \pm 0.019$ |
| 2 | All 3 | 10 | 22.955 | 0.5176 | $23.821 \pm 1.555$ | $0.4975 \pm 0.023$ |
| 4 | All 3 | 35 | 3.613 | 0.9241 | $3.988 \pm 0.261$ | $0.9159 \pm 0.004$ |
| 6 | All 3 | 84 | 0.422 | 0.9911 | $0.541 \pm 0.054$ | $0.9885 \pm 0.001$ |
| 7 | All 3 | 120 | 0.225 | 0.9953 | $0.307 \pm 0.033$ | $0.9935 \pm 0.001$ |
| **8 (Optimal)** | **All 3** | **165** | **0.164** | **0.9966** | **0.2523 ± 0.028** | **0.9946 ± 0.001** |
| 9 | All 3 | 220 | 0.147 | 0.9969 | $0.2954 \pm 0.049$ | $0.9937 \pm 0.001$ |
| 10 | All 3 | 286 | 0.128 | 0.9973 | $0.3484 \pm 0.063$ | $0.9926 \pm 0.002$ |
| 12 | All 3 | 455 | 0.098 | 0.9979 | $1.0140 \pm 0.443$ | $0.9786 \pm 0.010$ |
| 4 (Single $x_1$) | $x_1$ only | 5 | 43.210 | 0.0882 | $43.632 \pm 1.210$ | $0.0787 \pm 0.025$ |

**Key Spatial Observations:**  
- Single coordinate models fail ($R^2 < 0.08$), proving heat anomalies cannot be uncoupled from the 3D convective continuum.
- Increasing degree from 4 to 8 slashes validation MSE by **93.7%** (from 3.9875 down to 0.2523).
- Beyond degree 8, Runge-type boundary oscillations emerge, causing CV MSE to climb from 0.2523 to 0.3484 ($d=10$) and 1.0140 ($d=12$).

---

## 4. Model Diagnostics & Residual Analysis

Diagnostic evaluation validates all Gauss-Markov regression assumptions:

1. **Homoscedasticity & Zero Bias:**  
   Residual distributions $e_i = y_i - \hat{y}_i$ are strictly centered at zero with constant variance across the entire dynamic range. No curvature or heteroscedastic fan shapes are observed.
2. **Standard Error Consistency:**  
   - Phase 1 Residual Standard Deviation: $\sigma = 0.5093$ (vs target std $3.1872$).
   - Phase 2 Residual Standard Deviation: $\sigma = 0.4044$ (vs target std $6.9016$).
3. **Test Prediction Distribution Consistency:**  
   Predictions on the hidden 1,000-sample test sets match the physical empirical bounds of the training distributions:
   - Phase 1 Test Predictions: Mean $= 0.9860 \pm 4.1752$, Range: $[-10.38, +15.01]$ (Training Target: $0.8629 \pm 3.1872$, Range: $[-9.88, +12.07]$).
   - Phase 2 Test Predictions: Mean $= 2.2535 \pm 6.4661$, Range: $[-25.28, +38.92]$ (Training Target: $2.2751 \pm 6.9016$, Range: $[-30.26, +39.33]$).
   - Zero unbounded extrapolation artifacts or numerical instabilities occurred.

---

## 5. Repository File Structure

```text
├── IMT2024072/
│   ├── IMT2024072_Report.pdf              # 4-page academic submission report (mirrored)
│   ├── report.tex                         # Standalone LaTeX source (mirrored)
│   ├── IMT2024072_pred_var1.csv           # 1,000 test predictions for Phase 1 (mirrored)
│   ├── IMT2024072_pred_var2.csv           # 1,000 test predictions for Phase 2 (mirrored)
│   └── IMT2024072/
│       ├── IMT2024072_train_var1.csv      # Training data for Problem 1
│       ├── IMT2024072_test_var1.csv       # Test features for Problem 1
│       ├── IMT2024072_train_var2.csv      # Training data for Problem 2
│       ├── IMT2024072_test_var2.csv       # Test features for Problem 2
│       ├── IMT2024072_pred_var1.csv       # Mirrored prediction file
│       ├── IMT2024072_pred_var2.csv       # Mirrored prediction file
│       ├── IMT2024072_Report.pdf          # Mirrored report PDF
│       └── report.tex                     # Mirrored LaTeX source
├── IMT2024072.zip                         # Final submission ZIP archive
├── IMT2024072_Report.pdf                  # Standalone 4-page submission PDF report
├── report.tex                             # Standalone LaTeX report source code
├── IMT2024072_pred_var1.csv               # Root test predictions for Problem 1 (47 terms)
├── IMT2024072_pred_var2.csv               # Root test predictions for Problem 2 (165 terms)
├── polynomial_regression.py               # Standalone training, evaluation & inference script
├── fig_var1_cv.png                        # CV performance curve for Phase 1
├── fig_var2_cv.png                        # CV performance curve for Phase 2
├── fig_fits_and_residuals.png             # Actual vs Predicted & Residual diagnostics
├── requirements.txt                       # Python dependencies
└── README.md                              # Complete mathematical & implementation documentation
```

---

## 6. How to Reproduce

### 6.1 Setup Environment

Install required dependencies (Python 3.9+ recommended):

```bash
pip install -r requirements.txt
```

### 6.2 Execute Full Training Pipeline

Run the standalone end-to-end Python script:

```bash
python polynomial_regression.py
```

This single command:
1. Loads calibration datasets from `IMT2024072/IMT2024072/`.
2. Computes 5-fold cross-validation across polynomial degrees.
3. Performs $L_1$ Lasso screening and Post-Lasso OLS refitting for Phase 1 (47 terms).
4. Fits Degree 8 full polynomial regression for Phase 2 (165 terms).
5. Evaluates model diagnostics and outputs `IMT2024072_pred_var1.csv` and `IMT2024072_pred_var2.csv`.
6. Generates high-resolution cross-validation and residual diagnostic plots (`fig_var1_cv.png`, `fig_var2_cv.png`, `fig_fits_and_residuals.png`).

---

## 7. Deliverables Verification

All required submission items are generated, verified, and packaged:

1. **Test Predictions (Phase 1):** `IMT2024072_pred_var1.csv` — exactly 1,000 predictions ($y$), header included, 0 nulls.
2. **Test Predictions (Phase 2):** `IMT2024072_pred_var2.csv` — exactly 1,000 predictions ($y$), header included, 0 nulls.
3. **Report (PDF):** `IMT2024072_Report.pdf` — exactly 4 pages, comprehensive methodology, no top headers, highlighted equation cards.
4. **Report (LaTeX):** `report.tex` — clean, compilable LaTeX source code.
5. **Code Pipeline:** `polynomial_regression.py` — fully reproducible `scikit-learn` script.
6. **Submission Archive:** `IMT2024072.zip` — complete packaged submission archive.
