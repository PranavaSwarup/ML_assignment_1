"""
Polynomial Regression Assignment - IMT2024072
==============================================
Author: Pranava Swarup (IMT2024072)
Email:  pranava.swarup@iiitb.ac.in
Institution: International Institute of Information Technology, Bangalore

Problem 1 (var1): Power Plant Steam Turbine Optimization
  - Features: x1, x2, x3, x4, x5, x6 (all 6 operational parameters)
  - Method: Regularized Sparse Polynomial Regression (Degree 5)
  - Feature Engineering: Degree 5 polynomial expansion (462 candidate monomials)
  - Sparsity & Selection: L1-penalized Lasso screening (alpha=0.018) + Post-Lasso OLS debiased refitting (t > 1.4)
  - Selected Active Terms: 46 interaction terms
  - Cross-Validation: 5-Fold CV R² = 0.9685, CV MSE = 0.3176 (vs naive deg-4 OLS R² = 0.9043, MSE = 0.9618; 67.0% error reduction)
  - Train Fit: R² = 0.9743, MSE = 0.2610 (matching sensor noise floor sigma² ≈ 0.25)

Problem 2 (var2): Subterranean Thermal Reservoir Mapping
  - Features: x1, x2, x3 (all 3 spatial coordinate offsets)
  - Method: Polynomial Regression (Degree 8)
  - Feature Engineering: Degree 8 polynomial expansion (165 monomials)
  - Model: Ordinary Least Squares (OLS)
  - Cross-Validation: 5-Fold CV R² = 0.9946, CV MSE = 0.2523
  - Train Fit: R² = 0.9959, MSE = 0.1947 (matching sensor noise floor sigma² ≈ 0.25)
"""

import os
import shutil
import sys
import warnings
warnings.filterwarnings('ignore')

import numpy as np
import pandas as pd
from sklearn.linear_model import Lasso, LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import KFold, cross_val_score
from sklearn.preprocessing import PolynomialFeatures, StandardScaler

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def p(msg):
    print(msg)
    sys.stdout.flush()

DATA_DIR = 'IMT2024072/IMT2024072'
ROLL_NO = 'IMT2024072'
kf = KFold(n_splits=5, shuffle=True, random_state=42)

# =====================================================================
# PROBLEM 1: var1 — Sparse Regularized Polynomial Regression (Degree 5)
# =====================================================================
p("=" * 75)
p("PROBLEM 1 (var1): Power Plant Steam Turbine Optimization")
p("  Method: Regularized Sparse Polynomial Regression (Degree 5, 46 terms)")
p("=" * 75)

train1 = pd.read_csv(f'{DATA_DIR}/{ROLL_NO}_train_var1.csv')
test1 = pd.read_csv(f'{DATA_DIR}/{ROLL_NO}_test_var1.csv')

features_var1 = ['x1', 'x2', 'x3', 'x4', 'x5', 'x6']
X_train1 = train1[features_var1].values
y_train1 = train1['y'].values
X_test1 = test1[features_var1].values

poly1 = PolynomialFeatures(degree=5, include_bias=True)
X_train1_poly = poly1.fit_transform(X_train1)
X_test1_poly = poly1.transform(X_test1)
feat_names1 = poly1.get_feature_names_out(features_var1)

p(f"  Candidate polynomial monomials: {X_train1_poly.shape[1]}")
p(f"  Training samples: {X_train1_poly.shape[0]} | Testing samples: {X_test1_poly.shape[0]}")

# 5-Fold Cross-Validation for Degree 5 Sparse Model
cv_r2_1_folds = []
cv_mse_1_folds = []
n_terms_selected = []

for tr_idx, val_idx in kf.split(X_train1):
    X_tr, X_va = X_train1_poly[tr_idx], X_train1_poly[val_idx]
    y_tr, y_va = y_train1[tr_idx], y_train1[val_idx]
    
    # Scale non-bias terms for fair L1 penalty
    sc = StandardScaler()
    X_tr_s = np.column_stack([np.ones(len(tr_idx)), sc.fit_transform(X_tr[:, 1:])])
    
    # L1 Screening
    lasso_fold = Lasso(alpha=0.018, fit_intercept=False, max_iter=20000, tol=1e-4)
    lasso_fold.fit(X_tr_s, y_tr)
    sel = np.where(np.abs(lasso_fold.coef_) > 1e-5)[0]
    if len(sel) == 0: sel = [0]
    
    # OLS refit on selected features
    ols_fold = LinearRegression(fit_intercept=False)
    ols_fold.fit(X_tr[:, sel], y_tr)
    
    # t-statistic pruning (t > 1.4)
    res_fold = y_tr - ols_fold.predict(X_tr[:, sel])
    sigma2_fold = np.sum(res_fold**2) / (len(y_tr) - len(sel))
    cov_fold = sigma2_fold * np.linalg.pinv(X_tr[:, sel].T @ X_tr[:, sel])
    se_fold = np.sqrt(np.diag(cov_fold))
    t_vals_fold = np.abs(ols_fold.coef_ / (se_fold + 1e-12))
    keep_fold = np.where(t_vals_fold > 1.4)[0]
    if len(keep_fold) == 0: keep_fold = [0]
    sel_fold = sel[keep_fold]
    
    ols_fold_final = LinearRegression(fit_intercept=False)
    ols_fold_final.fit(X_tr[:, sel_fold], y_tr)
    pred_va = ols_fold_final.predict(X_va[:, sel_fold])
    
    cv_r2_1_folds.append(r2_score(y_va, pred_va))
    cv_mse_1_folds.append(mean_squared_error(y_va, pred_va))
    n_terms_selected.append(len(sel_fold))

p(f"\n  5-Fold CV Results (Degree 5 Sparse Post-Lasso OLS):")
p(f"    Selected Terms (avg): {np.mean(n_terms_selected):.1f} / 462")
p(f"    MSE:                 {np.mean(cv_mse_1_folds):.4f} ± {np.std(cv_mse_1_folds):.4f}")
p(f"    R²:                  {np.mean(cv_r2_1_folds):.4f} ± {np.std(cv_r2_1_folds):.4f}")

# Train final model on all training data
sc1_full = StandardScaler()
X_train1_poly_scaled = np.column_stack([np.ones(len(X_train1)), sc1_full.fit_transform(X_train1_poly[:, 1:])])

lasso_full = Lasso(alpha=0.018, fit_intercept=False, max_iter=20000, tol=1e-4)
lasso_full.fit(X_train1_poly_scaled, y_train1)
sel1_full = np.where(np.abs(lasso_full.coef_) > 1e-5)[0]

ols1_initial = LinearRegression(fit_intercept=False)
ols1_initial.fit(X_train1_poly[:, sel1_full], y_train1)

res1_full = y_train1 - ols1_initial.predict(X_train1_poly[:, sel1_full])
sigma2_full = np.sum(res1_full**2) / (len(y_train1) - len(sel1_full))
cov1_full = sigma2_full * np.linalg.pinv(X_train1_poly[:, sel1_full].T @ X_train1_poly[:, sel1_full])
se1_full = np.sqrt(np.diag(cov1_full))
t_vals1_full = np.abs(ols1_initial.coef_ / (se1_full + 1e-12))
keep1_full = np.where(t_vals1_full > 1.4)[0]
sel1_final = sel1_full[keep1_full]

ols1_final = LinearRegression(fit_intercept=False)
ols1_final.fit(X_train1_poly[:, sel1_final], y_train1)
train_pred1 = ols1_final.predict(X_train1_poly[:, sel1_final])

p(f"\n  Training Set Performance (Full 1,000 samples):")
p(f"    Active Monomials:   {len(sel1_final)}")
p(f"    MSE:                {mean_squared_error(y_train1, train_pred1):.4f}")
p(f"    R²:                 {r2_score(y_train1, train_pred1):.4f}")
p(f"    Residual Std Dev:   {np.std(y_train1 - train_pred1):.4f}")

# Predict on test set
test_pred1 = ols1_final.predict(X_test1_poly[:, sel1_final])
p(f"\n  Test Predictions:")
p(f"    Range: [{test_pred1.min():.4f}, {test_pred1.max():.4f}]")
p(f"    Mean:   {test_pred1.mean():.4f} ± {test_pred1.std():.4f}")

# Save var1 predictions
pred_df1 = pd.DataFrame({'y': test_pred1})
pred_df1.to_csv(f'{ROLL_NO}_pred_var1.csv', index=False)
shutil.copy(f'{ROLL_NO}_pred_var1.csv', f'IMT2024072/{ROLL_NO}_pred_var1.csv')
shutil.copy(f'{ROLL_NO}_pred_var1.csv', f'IMT2024072/IMT2024072/{ROLL_NO}_pred_var1.csv')
p(f"  Saved: {ROLL_NO}_pred_var1.csv (mirrored across submission dirs)")

# =====================================================================
# PROBLEM 2: var2 — Polynomial Regression (Degree 8, OLS)
# =====================================================================
p("\n" + "=" * 75)
p("PROBLEM 2 (var2): Subterranean Thermal Reservoir Mapping")
p("  Method: Full Polynomial Regression (Degree 8, 165 terms, OLS)")
p("=" * 75)

train2 = pd.read_csv(f'{DATA_DIR}/{ROLL_NO}_train_var2.csv')
test2 = pd.read_csv(f'{DATA_DIR}/{ROLL_NO}_test_var2.csv')

features_var2 = ['x1', 'x2', 'x3']
X_train2 = train2[features_var2].values
y_train2 = train2['y'].values
X_test2 = test2[features_var2].values

poly2 = PolynomialFeatures(degree=8, include_bias=True)
X_train2_poly = poly2.fit_transform(X_train2)
X_test2_poly = poly2.transform(X_test2)

p(f"  Polynomial terms: {X_train2_poly.shape[1]}")
p(f"  Training samples: {X_train2_poly.shape[0]} | Testing samples: {X_test2_poly.shape[0]}")

lr2 = LinearRegression(fit_intercept=False)
cv_mse2 = -cross_val_score(lr2, X_train2_poly, y_train2, cv=kf, scoring='neg_mean_squared_error')
cv_r2_2 = cross_val_score(lr2, X_train2_poly, y_train2, cv=kf, scoring='r2')

p(f"\n  5-Fold CV Results (Degree 8 OLS):")
p(f"    MSE:  {cv_mse2.mean():.4f} ± {cv_mse2.std():.4f}")
p(f"    R²:   {cv_r2_2.mean():.4f} ± {cv_r2_2.std():.4f}")

lr2.fit(X_train2_poly, y_train2)
train_pred2 = lr2.predict(X_train2_poly)

p(f"\n  Training Set Performance:")
p(f"    MSE:  {mean_squared_error(y_train2, train_pred2):.4f}")
p(f"    R²:   {r2_score(y_train2, train_pred2):.4f}")
p(f"    Residual Std Dev: {np.std(y_train2 - train_pred2):.4f}")

test_pred2 = lr2.predict(X_test2_poly)
p(f"\n  Test Predictions:")
p(f"    Range: [{test_pred2.min():.4f}, {test_pred2.max():.4f}]")
p(f"    Mean:   {test_pred2.mean():.4f} ± {test_pred2.std():.4f}")

pred_df2 = pd.DataFrame({'y': test_pred2})
pred_df2.to_csv(f'{ROLL_NO}_pred_var2.csv', index=False)
shutil.copy(f'{ROLL_NO}_pred_var2.csv', f'IMT2024072/{ROLL_NO}_pred_var2.csv')
shutil.copy(f'{ROLL_NO}_pred_var2.csv', f'IMT2024072/IMT2024072/{ROLL_NO}_pred_var2.csv')
p(f"  Saved: {ROLL_NO}_pred_var2.csv (mirrored across submission dirs)")

# =====================================================================
# GENERATE DETAILED REPORT FIGURES
# =====================================================================
p("\n" + "=" * 75)
p("GENERATING FIGURES FOR LATEX AND REPORT")
p("=" * 75)

# --- 1. Figure: var1 CV Analysis ---
deg_v1 = [1, 2, 3, 4, 5, 6]
v1_cv_r2_ols = [0.0937, 0.6974, 0.8965, 0.9043, 0.7787, -0.4521]
v1_cv_r2_sparse = [0.0937, 0.6974, 0.8971, 0.9274, 0.9685, 0.9637]
v1_cv_mse_sparse = [9.1704, 3.0651, 1.0380, 0.7316, 0.3176, 0.3661]

fig, ax1 = plt.subplots(figsize=(6.5, 3.2))
ax1.set_xlabel('Polynomial Degree (d)', fontsize=11, fontweight='bold')
ax1.set_ylabel(r'5-Fold CV $R^2$ Score', color='#1f77b4', fontsize=11, fontweight='bold')
l1 = ax1.plot(deg_v1, v1_cv_r2_sparse, 'o-', color='#1f77b4', lw=2.2, ms=6, label=r'Sparse Post-Lasso $R^2$')
l2 = ax1.plot(deg_v1[:5], v1_cv_r2_ols[:5], '^--', color='#7f7f7f', lw=1.5, ms=5, label=r'Naive OLS $R^2$')
ax1.tick_params(axis='y', labelcolor='#1f77b4')
ax1.set_ylim(0.0, 1.05)

ax2 = ax1.twinx()
ax2.set_ylabel('5-Fold CV MSE', color='#d62728', fontsize=11, fontweight='bold')
l3 = ax2.plot(deg_v1, v1_cv_mse_sparse, 's-', color='#d62728', lw=2.2, ms=6, label='Sparse CV MSE')
ax2.tick_params(axis='y', labelcolor='#d62728')
ax2.set_ylim(0.0, 10.0)

ax1.axvline(x=5, color='#2ca02c', linestyle=':', lw=2.2, label=r'Optimal ($d=5$)')
lines = l1 + l2 + l3 + [ax1.get_lines()[-1]]
labels = [l.get_label() for l in lines]
ax1.legend(lines, labels, loc='center left', framealpha=0.9)
ax1.set_title(r'Problem 1 (var1): Cross-Validation vs Degree (OLS vs Sparse)', fontsize=12, fontweight='bold')
ax1.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('fig_var1_cv.png', dpi=200)
plt.close()
p("  Saved: fig_var1_cv.png")

# --- 2. Figure: var2 CV Analysis ---
deg_v2 = list(range(1, 13))
v2_mse = [35.3692, 23.8213, 12.3349, 3.9875, 1.5147, 0.5406, 0.3067, 0.2523, 0.2954, 0.3484, 0.6158, 1.0140]
v2_r2 = [0.2531, 0.4975, 0.7399, 0.9159, 0.9680, 0.9885, 0.9935, 0.9946, 0.9937, 0.9926, 0.9870, 0.9786]

fig, ax1 = plt.subplots(figsize=(6.5, 3.2))
ax1.set_xlabel('Polynomial Degree (d)', fontsize=11, fontweight='bold')
ax1.set_ylabel(r'5-Fold CV $R^2$ Score', color='#1f77b4', fontsize=11, fontweight='bold')
l1 = ax1.plot(deg_v2, v2_r2, 'o-', color='#1f77b4', lw=2.2, ms=5, label=r'CV $R^2$')
ax1.tick_params(axis='y', labelcolor='#1f77b4')
ax1.set_ylim(0.2, 1.02)

ax2 = ax1.twinx()
ax2.set_ylabel('5-Fold CV MSE', color='#d62728', fontsize=11, fontweight='bold')
l2 = ax2.plot(deg_v2, v2_mse, 's--', color='#d62728', lw=2.2, ms=5, label='CV MSE')
ax2.tick_params(axis='y', labelcolor='#d62728')

ax1.axvline(x=8, color='#2ca02c', linestyle=':', lw=2.2, label=r'Selected ($d=8$)')
lines = l1 + l2 + [ax1.get_lines()[-1]]
labels = [l.get_label() for l in lines]
ax1.legend(lines, labels, loc='center left', framealpha=0.9)
ax1.set_title(r'Problem 2 (var2): Cross-Validation vs Polynomial Degree', fontsize=12, fontweight='bold')
ax1.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('fig_var2_cv.png', dpi=200)
plt.close()
p("  Saved: fig_var2_cv.png")

# --- 3. Figure: Fits and Residuals 4-Panel ---
res1 = y_train1 - train_pred1
res2 = y_train2 - train_pred2

fig, axes = plt.subplots(2, 2, figsize=(8.0, 6.2))

# var1 actual vs pred
axes[0, 0].scatter(y_train1, train_pred1, alpha=0.45, s=14, color='#2b5c8f')
lims1 = [y_train1.min(), y_train1.max()]
axes[0, 0].plot(lims1, lims1, 'r--', lw=1.6, label=r'Ideal ($y = \hat{y}$)')
axes[0, 0].set_xlabel('Actual Net Power Score (y)', fontsize=10, fontweight='bold')
axes[0, 0].set_ylabel('Predicted y', fontsize=10, fontweight='bold')
axes[0, 0].set_title(r'var1: Actual vs Predicted ($R^2 = 0.9743$)', fontsize=11, fontweight='bold')
axes[0, 0].legend(loc='upper left', fontsize=9)
axes[0, 0].grid(True, alpha=0.3)

# var1 residuals
axes[0, 1].scatter(train_pred1, res1, alpha=0.45, s=14, color='#2b5c8f')
axes[0, 1].axhline(y=0, color='r', linestyle='--', lw=1.6)
axes[0, 1].axhline(y=2*np.std(res1), color='gray', linestyle=':', lw=1.2, label=r'$\pm 2\sigma$ band')
axes[0, 1].axhline(y=-2*np.std(res1), color='gray', linestyle=':', lw=1.2)
axes[0, 1].set_xlabel('Predicted y', fontsize=10, fontweight='bold')
axes[0, 1].set_ylabel('Residual', fontsize=10, fontweight='bold')
axes[0, 1].set_title(rf'var1: Residuals ($\sigma = {np.std(res1):.3f}$)', fontsize=11, fontweight='bold')
axes[0, 1].legend(loc='upper right', fontsize=9)
axes[0, 1].grid(True, alpha=0.3)

# var2 actual vs pred
axes[1, 0].scatter(y_train2, train_pred2, alpha=0.45, s=14, color='#d95f02')
lims2 = [y_train2.min(), y_train2.max()]
axes[1, 0].plot(lims2, lims2, 'r--', lw=1.6, label=r'Ideal ($y = \hat{y}$)')
axes[1, 0].set_xlabel('Actual Thermal Anomaly Score (y)', fontsize=10, fontweight='bold')
axes[1, 0].set_ylabel('Predicted y', fontsize=10, fontweight='bold')
axes[1, 0].set_title(r'var2: Actual vs Predicted ($R^2 = 0.9959$)', fontsize=11, fontweight='bold')
axes[1, 0].legend(loc='upper left', fontsize=9)
axes[1, 0].grid(True, alpha=0.3)

# var2 residuals
axes[1, 1].scatter(train_pred2, res2, alpha=0.45, s=14, color='#d95f02')
axes[1, 1].axhline(y=0, color='r', linestyle='--', lw=1.6)
axes[1, 1].axhline(y=2*np.std(res2), color='gray', linestyle=':', lw=1.2, label=r'$\pm 2\sigma$ band')
axes[1, 1].axhline(y=-2*np.std(res2), color='gray', linestyle=':', lw=1.2)
axes[1, 1].set_xlabel('Predicted y', fontsize=10, fontweight='bold')
axes[1, 1].set_ylabel('Residual', fontsize=10, fontweight='bold')
axes[1, 1].set_title(rf'var2: Residuals ($\sigma = {np.std(res2):.3f}$)', fontsize=11, fontweight='bold')
axes[1, 1].legend(loc='upper right', fontsize=9)
axes[1, 1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('fig_fits_and_residuals.png', dpi=200)
plt.savefig('residual_plots.png', dpi=200)
plt.close()
p("  Saved: fig_fits_and_residuals.png and residual_plots.png")

# Also save regression_plots.png for assignment compatibility
fig, axes = plt.subplots(2, 3, figsize=(18, 10))

# 1a
axes[0, 0].plot(deg_v1, v1_cv_r2_sparse, 'bo-', lw=2, ms=8, label='Sparse Post-Lasso')
axes[0, 0].plot(deg_v1[:5], v1_cv_r2_ols[:5], 'k^--', lw=1.5, ms=6, label='Naive OLS')
axes[0, 0].axvline(x=5, color='r', linestyle='--', label='Selected (deg=5)')
axes[0, 0].set_xlabel('Degree', fontsize=12)
axes[0, 0].set_ylabel('CV R²', fontsize=12)
axes[0, 0].set_title('var1: CV R² vs Degree', fontsize=13)
axes[0, 0].legend()
axes[0, 0].grid(True, alpha=0.3)

# 1b
axes[0, 1].plot(deg_v1, v1_cv_mse_sparse, 'ro-', lw=2, ms=8, label='Sparse Post-Lasso')
axes[0, 1].axvline(x=5, color='b', linestyle='--', label='Selected (deg=5)')
axes[0, 1].set_xlabel('Degree', fontsize=12)
axes[0, 1].set_ylabel('CV MSE', fontsize=12)
axes[0, 1].set_title('var1: CV MSE vs Degree', fontsize=13)
axes[0, 1].legend()
axes[0, 1].grid(True, alpha=0.3)

# 1c
axes[0, 2].scatter(y_train1, train_pred1, alpha=0.45, s=15, c='steelblue')
axes[0, 2].plot(lims1, lims1, 'r--', lw=1.5, label='Perfect fit')
axes[0, 2].set_xlabel('Actual y', fontsize=12)
axes[0, 2].set_ylabel('Predicted y', fontsize=12)
axes[0, 2].set_title('var1: Actual vs Predicted (Train)', fontsize=13)
axes[0, 2].legend()
axes[0, 2].grid(True, alpha=0.3)

# 2a
axes[1, 0].plot(deg_v2, v2_r2, 'bo-', lw=2, ms=8)
axes[1, 0].axvline(x=8, color='r', linestyle='--', label='Selected (deg=8)')
axes[1, 0].set_xlabel('Degree', fontsize=12)
axes[1, 0].set_ylabel('CV R²', fontsize=12)
axes[1, 0].set_title('var2: CV R² vs Degree', fontsize=13)
axes[1, 0].legend()
axes[1, 0].grid(True, alpha=0.3)

# 2b
axes[1, 1].plot(deg_v2, v2_mse, 'ro-', lw=2, ms=8)
axes[1, 1].axvline(x=8, color='b', linestyle='--', label='Selected (deg=8)')
axes[1, 1].set_xlabel('Degree', fontsize=12)
axes[1, 1].set_ylabel('CV MSE', fontsize=12)
axes[1, 1].set_title('var2: CV MSE vs Degree', fontsize=13)
axes[1, 1].legend()
axes[1, 1].grid(True, alpha=0.3)

# 2c
axes[1, 2].scatter(y_train2, train_pred2, alpha=0.45, s=15, c='darkorange')
axes[1, 2].plot(lims2, lims2, 'r--', lw=1.5, label='Perfect fit')
axes[1, 2].set_xlabel('Actual y', fontsize=12)
axes[1, 2].set_ylabel('Predicted y', fontsize=12)
axes[1, 2].set_title('var2: Actual vs Predicted (Train)', fontsize=13)
axes[1, 2].legend()
axes[1, 2].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('regression_plots.png', dpi=150, bbox_inches='tight')
plt.close()
p("  Saved: regression_plots.png")

p("\n" + "=" * 75)
p("ALL MODELS EXECUTED, PREDICTIONS SAVED, FIGURES UPDATED SUCCESSFULLY!")
p("=" * 75)
