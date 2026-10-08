"""
Polynomial Regression Assignment - IMT2024072
==============================================
Problem 1 (var1): Steam Turbine Optimization
  - Features: x1, x2, x3, x4, x5, x6 (all 6)
  - Polynomial degree: 4
  - Model: LinearRegression on PolynomialFeatures(degree=4)

Problem 2 (var2): Subterranean Thermal Reservoir Mapping
  - Features: x1, x2, x3 (all 3)
  - Polynomial degree: 8
  - Model: LinearRegression on PolynomialFeatures(degree=8)

Degree selection rationale (5-fold CV):
  var1 deg=4: CV R²=0.9043, CV MSE=0.9618  (deg=3: 0.8965, deg=5: overfits)
  var2 deg=8: CV R²=0.9946, CV MSE=0.2523  (deg=7: 0.9935, deg=9: starts degrading)
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import KFold, cross_val_score
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import sys
import warnings
warnings.filterwarnings('ignore')

def p(msg): print(msg); sys.stdout.flush()

DATA_DIR = 'IMT2024072/IMT2024072'
ROLL_NO = 'IMT2024072'
kf = KFold(n_splits=5, shuffle=True, random_state=42)

# =====================================================================
# PROBLEM 1: var1 — Polynomial degree 4, all 6 features
# =====================================================================
p("=" * 70)
p("PROBLEM 1 (var1): Steam Turbine Optimization")
p("  Features: x1, x2, x3, x4, x5, x6 | Degree: 4")
p("=" * 70)

train1 = pd.read_csv(f'{DATA_DIR}/{ROLL_NO}_train_var1.csv')
test1 = pd.read_csv(f'{DATA_DIR}/{ROLL_NO}_test_var1.csv')

features_var1 = ['x1', 'x2', 'x3', 'x4', 'x5', 'x6']
X_train1 = train1[features_var1].values
y_train1 = train1['y'].values
X_test1 = test1[features_var1].values

# Build polynomial features
poly1 = PolynomialFeatures(degree=4, include_bias=True)
X_train1_poly = poly1.fit_transform(X_train1)
X_test1_poly = poly1.transform(X_test1)

p(f"  Polynomial terms: {X_train1_poly.shape[1]}")
p(f"  Train samples: {X_train1_poly.shape[0]}")
p(f"  Test samples: {X_test1_poly.shape[0]}")

# Cross-validation
lr1 = LinearRegression(fit_intercept=False)  # bias already in poly features
cv_mse1 = -cross_val_score(lr1, X_train1_poly, y_train1, cv=kf, scoring='neg_mean_squared_error')
cv_r2_1 = cross_val_score(lr1, X_train1_poly, y_train1, cv=kf, scoring='r2')
p(f"\n  5-Fold CV Results:")
p(f"    MSE:  {cv_mse1.mean():.4f} ± {cv_mse1.std():.4f}")
p(f"    R²:   {cv_r2_1.mean():.4f} ± {cv_r2_1.std():.4f}")

# Train final model on all training data
lr1.fit(X_train1_poly, y_train1)
train_pred1 = lr1.predict(X_train1_poly)
p(f"\n  Training Set Performance:")
p(f"    MSE:  {mean_squared_error(y_train1, train_pred1):.4f}")
p(f"    R²:   {r2_score(y_train1, train_pred1):.4f}")

# Predict on test
test_pred1 = lr1.predict(X_test1_poly)
p(f"\n  Test Predictions: min={test_pred1.min():.4f}, max={test_pred1.max():.4f}, "
  f"mean={test_pred1.mean():.4f}, std={test_pred1.std():.4f}")

# Save predictions
pred_df1 = pd.DataFrame({'y': test_pred1})
pred_df1.to_csv(f'{ROLL_NO}_pred_var1.csv', index=False)
p(f"  Saved: {ROLL_NO}_pred_var1.csv")

# =====================================================================
# PROBLEM 2: var2 — Polynomial degree 8, all 3 features
# =====================================================================
p("\n" + "=" * 70)
p("PROBLEM 2 (var2): Subterranean Thermal Reservoir Mapping")
p("  Features: x1, x2, x3 | Degree: 8")
p("=" * 70)

train2 = pd.read_csv(f'{DATA_DIR}/{ROLL_NO}_train_var2.csv')
test2 = pd.read_csv(f'{DATA_DIR}/{ROLL_NO}_test_var2.csv')

features_var2 = ['x1', 'x2', 'x3']
X_train2 = train2[features_var2].values
y_train2 = train2['y'].values
X_test2 = test2[features_var2].values

# Build polynomial features
poly2 = PolynomialFeatures(degree=8, include_bias=True)
X_train2_poly = poly2.fit_transform(X_train2)
X_test2_poly = poly2.transform(X_test2)

p(f"  Polynomial terms: {X_train2_poly.shape[1]}")
p(f"  Train samples: {X_train2_poly.shape[0]}")
p(f"  Test samples: {X_test2_poly.shape[0]}")

# Cross-validation
lr2 = LinearRegression(fit_intercept=False)
cv_mse2 = -cross_val_score(lr2, X_train2_poly, y_train2, cv=kf, scoring='neg_mean_squared_error')
cv_r2_2 = cross_val_score(lr2, X_train2_poly, y_train2, cv=kf, scoring='r2')
p(f"\n  5-Fold CV Results:")
p(f"    MSE:  {cv_mse2.mean():.4f} ± {cv_mse2.std():.4f}")
p(f"    R²:   {cv_r2_2.mean():.4f} ± {cv_r2_2.std():.4f}")

# Train final model on all training data
lr2.fit(X_train2_poly, y_train2)
train_pred2 = lr2.predict(X_train2_poly)
p(f"\n  Training Set Performance:")
p(f"    MSE:  {mean_squared_error(y_train2, train_pred2):.4f}")
p(f"    R²:   {r2_score(y_train2, train_pred2):.4f}")

# Predict on test
test_pred2 = lr2.predict(X_test2_poly)
p(f"\n  Test Predictions: min={test_pred2.min():.4f}, max={test_pred2.max():.4f}, "
  f"mean={test_pred2.mean():.4f}, std={test_pred2.std():.4f}")

# Save predictions
pred_df2 = pd.DataFrame({'y': test_pred2})
pred_df2.to_csv(f'{ROLL_NO}_pred_var2.csv', index=False)
p(f"  Saved: {ROLL_NO}_pred_var2.csv")


# =====================================================================
# GENERATE PLOTS FOR REPORT
# =====================================================================
p("\n" + "=" * 70)
p("GENERATING PLOTS FOR REPORT")
p("=" * 70)

fig, axes = plt.subplots(2, 3, figsize=(18, 10))

# --- VAR1 PLOTS ---

# 1a. Degree sweep plot for var1
degrees_v1 = list(range(1, 6))
cv_mses_v1 = []
cv_r2s_v1 = []
for deg in degrees_v1:
    poly = PolynomialFeatures(degree=deg, include_bias=True)
    X_p = poly.fit_transform(X_train1)
    lr = LinearRegression(fit_intercept=False)
    mse = -cross_val_score(lr, X_p, y_train1, cv=kf, scoring='neg_mean_squared_error').mean()
    r2 = cross_val_score(lr, X_p, y_train1, cv=kf, scoring='r2').mean()
    cv_mses_v1.append(mse)
    cv_r2s_v1.append(r2)

ax = axes[0, 0]
ax.plot(degrees_v1, cv_r2s_v1, 'bo-', linewidth=2, markersize=8)
ax.axvline(x=4, color='r', linestyle='--', alpha=0.7, label='Selected (deg=4)')
ax.set_xlabel('Polynomial Degree', fontsize=12)
ax.set_ylabel('CV R² Score', fontsize=12)
ax.set_title('var1: CV R² vs Degree (all 6 features)', fontsize=13)
ax.legend(fontsize=10)
ax.grid(True, alpha=0.3)
ax.set_xticks(degrees_v1)

ax = axes[0, 1]
ax.plot(degrees_v1, cv_mses_v1, 'ro-', linewidth=2, markersize=8)
ax.axvline(x=4, color='b', linestyle='--', alpha=0.7, label='Selected (deg=4)')
ax.set_xlabel('Polynomial Degree', fontsize=12)
ax.set_ylabel('CV MSE', fontsize=12)
ax.set_title('var1: CV MSE vs Degree (all 6 features)', fontsize=13)
ax.legend(fontsize=10)
ax.grid(True, alpha=0.3)
ax.set_xticks(degrees_v1)

# 1c. Actual vs Predicted (train)
ax = axes[0, 2]
ax.scatter(y_train1, train_pred1, alpha=0.5, s=15, c='steelblue')
lims = [min(y_train1.min(), train_pred1.min()), max(y_train1.max(), train_pred1.max())]
ax.plot(lims, lims, 'r--', linewidth=1.5, label='Perfect fit')
ax.set_xlabel('Actual y', fontsize=12)
ax.set_ylabel('Predicted y', fontsize=12)
ax.set_title('var1: Actual vs Predicted (Train)', fontsize=13)
ax.legend(fontsize=10)
ax.grid(True, alpha=0.3)

# --- VAR2 PLOTS ---

# 2a. Degree sweep plot for var2
degrees_v2 = list(range(1, 13))
cv_mses_v2 = []
cv_r2s_v2 = []
for deg in degrees_v2:
    poly = PolynomialFeatures(degree=deg, include_bias=True)
    X_p = poly.fit_transform(X_train2)
    lr = LinearRegression(fit_intercept=False)
    mse = -cross_val_score(lr, X_p, y_train2, cv=kf, scoring='neg_mean_squared_error').mean()
    r2 = cross_val_score(lr, X_p, y_train2, cv=kf, scoring='r2').mean()
    cv_mses_v2.append(mse)
    cv_r2s_v2.append(r2)

ax = axes[1, 0]
ax.plot(degrees_v2, cv_r2s_v2, 'bo-', linewidth=2, markersize=8)
ax.axvline(x=8, color='r', linestyle='--', alpha=0.7, label='Selected (deg=8)')
ax.set_xlabel('Polynomial Degree', fontsize=12)
ax.set_ylabel('CV R² Score', fontsize=12)
ax.set_title('var2: CV R² vs Degree (all 3 features)', fontsize=13)
ax.legend(fontsize=10)
ax.grid(True, alpha=0.3)
ax.set_xticks(degrees_v2)

ax = axes[1, 1]
ax.plot(degrees_v2, cv_mses_v2, 'ro-', linewidth=2, markersize=8)
ax.axvline(x=8, color='b', linestyle='--', alpha=0.7, label='Selected (deg=8)')
ax.set_xlabel('Polynomial Degree', fontsize=12)
ax.set_ylabel('CV MSE', fontsize=12)
ax.set_title('var2: CV MSE vs Degree (all 3 features)', fontsize=13)
ax.legend(fontsize=10)
ax.grid(True, alpha=0.3)
ax.set_xticks(degrees_v2)

# 2c. Actual vs Predicted (train)
ax = axes[1, 2]
ax.scatter(y_train2, train_pred2, alpha=0.5, s=15, c='darkorange')
lims = [min(y_train2.min(), train_pred2.min()), max(y_train2.max(), train_pred2.max())]
ax.plot(lims, lims, 'r--', linewidth=1.5, label='Perfect fit')
ax.set_xlabel('Actual y', fontsize=12)
ax.set_ylabel('Predicted y', fontsize=12)
ax.set_title('var2: Actual vs Predicted (Train)', fontsize=13)
ax.legend(fontsize=10)
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('regression_plots.png', dpi=150, bbox_inches='tight')
p("  Saved: regression_plots.png")

# --- Residual plots ---
fig2, axes2 = plt.subplots(1, 2, figsize=(14, 5))

ax = axes2[0]
residuals1 = y_train1 - train_pred1
ax.scatter(train_pred1, residuals1, alpha=0.5, s=15, c='steelblue')
ax.axhline(y=0, color='r', linestyle='--', linewidth=1.5)
ax.set_xlabel('Predicted y', fontsize=12)
ax.set_ylabel('Residual', fontsize=12)
ax.set_title('var1: Residual Plot (Train, deg=4)', fontsize=13)
ax.grid(True, alpha=0.3)

ax = axes2[1]
residuals2 = y_train2 - train_pred2
ax.scatter(train_pred2, residuals2, alpha=0.5, s=15, c='darkorange')
ax.axhline(y=0, color='r', linestyle='--', linewidth=1.5)
ax.set_xlabel('Predicted y', fontsize=12)
ax.set_ylabel('Residual', fontsize=12)
ax.set_title('var2: Residual Plot (Train, deg=8)', fontsize=13)
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('residual_plots.png', dpi=150, bbox_inches='tight')
p("  Saved: residual_plots.png")

p("\n" + "=" * 70)
p("ALL DONE — Predictions saved, plots generated.")
p("=" * 70)
