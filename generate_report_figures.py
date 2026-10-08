import os
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.linear_model import Lasso, LinearRegression

plt.rcParams.update({
    'font.size': 10,
    'axes.labelsize': 11,
    'axes.titlesize': 12,
    'xtick.labelsize': 9,
    'ytick.labelsize': 9,
    'legend.fontsize': 9,
    'figure.titlesize': 13
})

# 1. Var1 CV Metrics Plot
deg_v1 = [1, 2, 3, 4, 5, 6]
v1_cv_r2_ols = [0.0937, 0.6974, 0.8965, 0.9043, 0.7787, -0.4521]
v1_cv_r2_sparse = [0.0937, 0.6974, 0.8971, 0.9274, 0.9685, 0.9637]
v1_cv_mse_sparse = [9.1704, 3.0651, 1.0380, 0.7316, 0.3176, 0.3661]

fig, ax1 = plt.subplots(figsize=(6.2, 3.0))
ax1.set_xlabel('Polynomial Degree (d)', fontweight='bold')
ax1.set_ylabel(r'5-Fold CV $R^2$ Score', color='#1f77b4', fontweight='bold')
l1 = ax1.plot(deg_v1, v1_cv_r2_sparse, 'o-', color='#1f77b4', linewidth=2.2, markersize=6, label=r'Sparse Post-Lasso $R^2$')
l2 = ax1.plot(deg_v1[:5], v1_cv_r2_ols[:5], '^--', color='#7f7f7f', linewidth=1.5, markersize=5, label=r'Naive OLS $R^2$')
ax1.tick_params(axis='y', labelcolor='#1f77b4')
ax1.set_ylim(0, 1.05)

ax2 = ax1.twinx()
ax2.set_ylabel('5-Fold CV MSE', color='#d62728', fontweight='bold')
l3 = ax2.plot(deg_v1, v1_cv_mse_sparse, 's--', color='#d62728', linewidth=2, markersize=6, label='Sparse CV MSE')
ax2.tick_params(axis='y', labelcolor='#d62728')
ax2.set_ylim(0, 10.0)

ax1.axvline(x=5, color='#2ca02c', linestyle=':', linewidth=2, label=r'Optimal ($d=5$)')
lines = l1 + l2 + [l3[0]] + [ax1.get_lines()[-1]]
labels = [l.get_label() for l in lines]
ax1.legend(lines, labels, loc='center left', framealpha=0.9)
ax1.set_title(r'Problem 1 (var1): 5-Fold Cross-Validation vs Polynomial Degree')
ax1.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('fig_var1_cv.png', dpi=200)
plt.close()

# 2. Var2 CV Metrics Plot
deg_v2 = list(range(1, 13))
v2_mse = [35.3692, 23.8213, 12.3349, 3.9875, 1.5147, 0.5406, 0.3067, 0.2523, 0.2954, 0.3484, 0.6158, 1.0140]
v2_r2 = [0.2531, 0.4975, 0.7399, 0.9159, 0.9680, 0.9885, 0.9935, 0.9946, 0.9937, 0.9926, 0.9870, 0.9786]

fig, ax1 = plt.subplots(figsize=(6.2, 3.0))
ax1.set_xlabel('Polynomial Degree (d)', fontweight='bold')
ax1.set_ylabel(r'5-Fold CV $R^2$ Score', color='#1f77b4', fontweight='bold')
l1 = ax1.plot(deg_v2, v2_r2, 'o-', color='#1f77b4', linewidth=2, markersize=5, label=r'CV $R^2$')
ax1.tick_params(axis='y', labelcolor='#1f77b4')
ax1.set_ylim(0.2, 1.02)

ax2 = ax1.twinx()
ax2.set_ylabel('5-Fold CV MSE', color='#d62728', fontweight='bold')
l2 = ax2.plot(deg_v2, v2_mse, 's--', color='#d62728', linewidth=2, markersize=5, label='CV MSE')
ax2.tick_params(axis='y', labelcolor='#d62728')

ax1.axvline(x=8, color='#2ca02c', linestyle=':', linewidth=2, label=r'Selected ($d=8$)')
lines = l1 + l2 + [ax1.get_lines()[-1]]
labels = [l.get_label() for l in lines]
ax1.legend(lines, labels, loc='center left', framealpha=0.9)
ax1.set_title(r'Problem 2 (var2): 5-Fold Cross-Validation vs Polynomial Degree')
ax1.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('fig_var2_cv.png', dpi=200)
plt.close()

# 3. Model Fit & Residuals Side-by-Side
train1 = pd.read_csv('IMT2024072/IMT2024072/IMT2024072_train_var1.csv')
train2 = pd.read_csv('IMT2024072/IMT2024072/IMT2024072_train_var2.csv')

# var1: degree 5 regularized sparse
p1 = PolynomialFeatures(5, include_bias=True)
X1_p = p1.fit_transform(train1[['x1','x2','x3','x4','x5','x6']].values)
sc1 = StandardScaler()
X1_s = np.column_stack([np.ones(len(train1)), sc1.fit_transform(X1_p[:, 1:])])
l1 = Lasso(alpha=0.018, fit_intercept=False, max_iter=20000, tol=1e-4).fit(X1_s, train1['y'].values)
sel1 = np.where(np.abs(l1.coef_) > 1e-5)[0]
ols1 = LinearRegression(fit_intercept=False).fit(X1_p[:, sel1], train1['y'].values)
res1_init = train1['y'].values - ols1.predict(X1_p[:, sel1])
sigma2 = np.sum(res1_init**2) / (len(train1) - len(sel1))
cov = sigma2 * np.linalg.pinv(X1_p[:, sel1].T @ X1_p[:, sel1])
se = np.sqrt(np.diag(cov))
t_vals = np.abs(ols1.coef_ / (se + 1e-12))
sel1_final = sel1[np.where(t_vals > 1.4)[0]]
ols1_final = LinearRegression(fit_intercept=False).fit(X1_p[:, sel1_final], train1['y'].values)
y1_pred = ols1_final.predict(X1_p[:, sel1_final])
res1 = train1['y'].values - y1_pred

# var2: degree 8 OLS
p2 = PolynomialFeatures(8, include_bias=True)
X2_p = p2.fit_transform(train2[['x1','x2','x3']].values)
lr2 = LinearRegression(fit_intercept=False).fit(X2_p, train2['y'].values)
y2_pred = lr2.predict(X2_p)
res2 = train2['y'].values - y2_pred

fig, axes = plt.subplots(2, 2, figsize=(7.2, 5.8))

axes[0, 0].scatter(train1['y'].values, y1_pred, alpha=0.4, s=12, color='#2b5c8f')
axes[0, 0].plot([train1['y'].min(), train1['y'].max()], [train1['y'].min(), train1['y'].max()], 'r--', lw=1.5, label=r'Ideal ($y = \hat{y}$)')
axes[0, 0].set_xlabel('Actual Net Power Score (y)')
axes[0, 0].set_ylabel('Predicted y')
axes[0, 0].set_title(r'var1: Actual vs Predicted ($R^2 = 0.9743$)')
axes[0, 0].legend(loc='upper left', fontsize=8)
axes[0, 0].grid(True, alpha=0.3)

axes[0, 1].scatter(y1_pred, res1, alpha=0.4, s=12, color='#2b5c8f')
axes[0, 1].axhline(y=0, color='r', linestyle='--', lw=1.5)
axes[0, 1].axhline(y=2*np.std(res1), color='gray', linestyle=':', lw=1.2, label=r'$\pm 2\sigma$ band')
axes[0, 1].axhline(y=-2*np.std(res1), color='gray', linestyle=':', lw=1.2)
axes[0, 1].set_xlabel('Predicted y')
axes[0, 1].set_ylabel('Residual')
axes[0, 1].set_title(rf'var1: Residual Plot ($\sigma = {np.std(res1):.3f}$)')
axes[0, 1].legend(loc='upper right', fontsize=8)
axes[0, 1].grid(True, alpha=0.3)

axes[1, 0].scatter(train2['y'].values, y2_pred, alpha=0.4, s=12, color='#d95f02')
axes[1, 0].plot([train2['y'].min(), train2['y'].max()], [train2['y'].min(), train2['y'].max()], 'r--', lw=1.5, label=r'Ideal ($y = \hat{y}$)')
axes[1, 0].set_xlabel('Actual Thermal Anomaly Score (y)')
axes[1, 0].set_ylabel('Predicted y')
axes[1, 0].set_title(r'var2: Actual vs Predicted ($R^2 = 0.9959$)')
axes[1, 0].legend(loc='upper left', fontsize=8)
axes[1, 0].grid(True, alpha=0.3)

axes[1, 1].scatter(y2_pred, res2, alpha=0.4, s=12, color='#d95f02')
axes[1, 1].axhline(y=0, color='r', linestyle='--', lw=1.5)
axes[1, 1].axhline(y=2*np.std(res2), color='gray', linestyle=':', lw=1.2, label=r'$\pm 2\sigma$ band')
axes[1, 1].axhline(y=-2*np.std(res2), color='gray', linestyle=':', lw=1.2)
axes[1, 1].set_xlabel('Predicted y')
axes[1, 1].set_ylabel('Residual')
axes[1, 1].set_title(rf'var2: Residual Plot ($\sigma = {np.std(res2):.3f}$)')
axes[1, 1].legend(loc='upper right', fontsize=8)
axes[1, 1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('fig_fits_and_residuals.png', dpi=200)
plt.close()

print("Figures re-generated successfully.")
