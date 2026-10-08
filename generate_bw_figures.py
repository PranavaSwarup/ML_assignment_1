import os
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

plt.rcParams.update({
    'font.size': 10,
    'axes.labelsize': 10.5,
    'axes.titlesize': 11.5,
    'xtick.labelsize': 9,
    'ytick.labelsize': 9,
    'legend.fontsize': 9,
    'figure.titlesize': 12,
    'lines.linewidth': 1.5
})

# 1. Var1 CV Metrics Plot (Black & White Academic Style)
degrees_v1 = [1, 2, 3, 4, 5]
v1_mse = [9.1704, 3.0651, 1.0438, 0.9618, 2.2071]
v1_r2 = [0.0937, 0.6974, 0.8965, 0.9043, 0.7787]

fig, ax1 = plt.subplots(figsize=(6.2, 2.8))
ax1.set_xlabel('Polynomial Degree (d)')
ax1.set_ylabel(r'5-Fold CV $R^2$ Score', color='black')
l1 = ax1.plot(degrees_v1, v1_r2, 'k-o', markersize=5, label=r'CV $R^2$')
ax1.set_ylim(0, 1.05)
ax1.grid(True, linestyle=':', alpha=0.6, color='gray')

ax2 = ax1.twinx()
ax2.set_ylabel('5-Fold CV MSE', color='black')
l2 = ax2.plot(degrees_v1, v1_mse, 'k--s', markersize=5, label='CV MSE')

ax1.axvline(x=4, color='black', linestyle=':', linewidth=1.8, label=r'Selected ($d=4$)')
lines = l1 + l2 + [ax1.get_lines()[-1]]
labels = [l.get_label() for l in lines]
ax1.legend(lines, labels, loc='center left', framealpha=0.95)
ax1.set_title(r'Problem 1 (var1): 5-Fold Cross-Validation Metrics vs. Degree')
plt.tight_layout()
plt.savefig('fig_bw_var1_cv.png', dpi=250)
plt.close()

# 2. Var2 CV Metrics Plot (Black & White Academic Style)
degrees_v2 = list(range(1, 13))
v2_mse = [35.3692, 23.8213, 12.3349, 3.9875, 1.5147, 0.5406, 0.3067, 0.2523, 0.2954, 0.3484, 0.6158, 1.0140]
v2_r2 = [0.2531, 0.4975, 0.7399, 0.9159, 0.9680, 0.9885, 0.9935, 0.9946, 0.9937, 0.9926, 0.9870, 0.9786]

fig, ax1 = plt.subplots(figsize=(6.2, 2.8))
ax1.set_xlabel('Polynomial Degree (d)')
ax1.set_ylabel(r'5-Fold CV $R^2$ Score', color='black')
l1 = ax1.plot(degrees_v2, v2_r2, 'k-o', markersize=4.5, label=r'CV $R^2$')
ax1.set_ylim(0.2, 1.02)
ax1.grid(True, linestyle=':', alpha=0.6, color='gray')

ax2 = ax1.twinx()
ax2.set_ylabel('5-Fold CV MSE', color='black')
l2 = ax2.plot(degrees_v2, v2_mse, 'k--s', markersize=4.5, label='CV MSE')

ax1.axvline(x=8, color='black', linestyle=':', linewidth=1.8, label=r'Selected ($d=8$)')
lines = l1 + l2 + [ax1.get_lines()[-1]]
labels = [l.get_label() for l in lines]
ax1.legend(lines, labels, loc='center left', framealpha=0.95)
ax1.set_title(r'Problem 2 (var2): 5-Fold Cross-Validation Metrics vs. Degree')
plt.tight_layout()
plt.savefig('fig_bw_var2_cv.png', dpi=250)
plt.close()

# 3. Model Diagnostics (Fit & Residuals, Grayscale)
train1 = pd.read_csv('IMT2024072/IMT2024072/IMT2024072_train_var1.csv')
train2 = pd.read_csv('IMT2024072/IMT2024072/IMT2024072_train_var2.csv')
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression

# var1
p1 = PolynomialFeatures(4, include_bias=True)
X1_p = p1.fit_transform(train1[['x1','x2','x3','x4','x5','x6']].values)
lr1 = LinearRegression(fit_intercept=False).fit(X1_p, train1['y'].values)
y1_pred = lr1.predict(X1_p)
res1 = train1['y'].values - y1_pred

# var2
p2 = PolynomialFeatures(8, include_bias=True)
X2_p = p2.fit_transform(train2[['x1','x2','x3']].values)
lr2 = LinearRegression(fit_intercept=False).fit(X2_p, train2['y'].values)
y2_pred = lr2.predict(X2_p)
res2 = train2['y'].values - y2_pred

fig, axes = plt.subplots(2, 2, figsize=(7.0, 5.6))

# var1 Fit
axes[0, 0].scatter(train1['y'].values, y1_pred, alpha=0.35, s=11, color='#333333', edgecolors='none')
axes[0, 0].plot([train1['y'].min(), train1['y'].max()], [train1['y'].min(), train1['y'].max()], 'k--', lw=1.2)
axes[0, 0].set_xlabel('Actual Net Power Score (y)')
axes[0, 0].set_ylabel('Predicted y')
axes[0, 0].set_title(r'var1: Actual vs. Predicted ($d=4$)')
axes[0, 0].grid(True, linestyle=':', alpha=0.5)

# var1 Residuals
axes[0, 1].scatter(y1_pred, res1, alpha=0.35, s=11, color='#333333', edgecolors='none')
axes[0, 1].axhline(y=0, color='black', linestyle='--', lw=1.2)
axes[0, 1].set_xlabel('Predicted y')
axes[0, 1].set_ylabel('Residual (y - y_hat)')
axes[0, 1].set_title(r'var1: Residual Plot ($d=4$)')
axes[0, 1].grid(True, linestyle=':', alpha=0.5)

# var2 Fit
axes[1, 0].scatter(train2['y'].values, y2_pred, alpha=0.35, s=11, color='#333333', edgecolors='none')
axes[1, 0].plot([train2['y'].min(), train2['y'].max()], [train2['y'].min(), train2['y'].max()], 'k--', lw=1.2)
axes[1, 0].set_xlabel('Actual Thermal Score (y)')
axes[1, 0].set_ylabel('Predicted y')
axes[1, 0].set_title(r'var2: Actual vs. Predicted ($d=8$)')
axes[1, 0].grid(True, linestyle=':', alpha=0.5)

# var2 Residuals
axes[1, 1].scatter(y2_pred, res2, alpha=0.35, s=11, color='#333333', edgecolors='none')
axes[1, 1].axhline(y=0, color='black', linestyle='--', lw=1.2)
axes[1, 1].set_xlabel('Predicted y')
axes[1, 1].set_ylabel('Residual (y - y_hat)')
axes[1, 1].set_title(r'var2: Residual Plot ($d=8$)')
axes[1, 1].grid(True, linestyle=':', alpha=0.5)

plt.tight_layout()
plt.savefig('fig_bw_diagnostics.png', dpi=250)
plt.close()

print("Clean B&W academic figures saved successfully.")
