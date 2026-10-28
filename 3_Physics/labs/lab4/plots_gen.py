#!/usr/bin/env python3
"""
Генерация графиков для л/р 1.09.
Запуск:  python gen_plots_1_09.py
Результат: assets/graph1.png, assets/graph2.png
"""
import numpy as np
import matplotlib.pyplot as plt
import os

os.makedirs(os.path.join('docs', 'assets'), exist_ok=True)
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 11


phi_deg = np.array([270, 180, 90, -90, -180, -270], dtype=float)
phi_rad = np.deg2rad(phi_deg)
M_vals  = np.array([9.37e-2, 4.70e-2, 8.71e-2, -3.86e-2, -3.32e-2, -7.16e-2])

phi_all = np.concatenate(([0.0], phi_rad))
M_all   = np.concatenate(([0.0], M_vals))

idx = np.argsort(phi_all)
phi_all = phi_all[idx]
M_all   = M_all[idx]

n        = len(phi_all)
phi_mean = np.mean(phi_all)
M_mean   = np.mean(M_all)
Sxx      = np.sum((phi_all - phi_mean)**2)
Sxy      = np.sum((phi_all - phi_mean) * (M_all - M_mean))
k        = Sxy / Sxx
c        = M_mean - k * phi_mean

M_pred = k * phi_all + c
SS_res = np.sum((M_all - M_pred)**2)
SS_tot = np.sum((M_all - M_mean)**2)
R2     = 1 - SS_res / SS_tot

s    = np.sqrt(SS_res / (n - 2))
s_k  = s / np.sqrt(Sxx)
Dk   = 2 * s_k


fig, ax = plt.subplots(figsize=(8, 5.5))
ax.scatter(phi_all, M_all, color='black', s=55, zorder=3, label='Эксперимент')

phi_line = np.linspace(phi_all.min() * 1.1, phi_all.max() * 1.1, 200)
sign = '+' if c >= 0 else '-'
ax.plot(phi_line, k * phi_line + c, color='tab:blue', lw=1.5,
        label=(f'МНК: $M = {k*100:.2f}\\cdot10^{{-2}}\\,\\varphi '
               f'{sign} {abs(c)*100:.2f}\\cdot10^{{-2}}$'))

ax.axhline(0, color='gray', lw=0.7)
ax.axvline(0, color='gray', lw=0.7)
ax.set_xlabel(r'Угол закручивания $\varphi$, рад')
ax.set_ylabel(r'Момент силы $M$, Н$\cdot$м')
ax.set_title('Зависимость момента силы от угла закручивания')
ax.grid(True, linestyle='--', alpha=0.6)
ax.legend(loc='upper left')
ax.text(0.97, 0.05,
        f'$k = ({k*100:.2f} \\pm {Dk*100:.2f})\\cdot10^{{-2}}$ Н$\\cdot$м/рад\n'
        f'$R^2 = {R2:.3f}$',
        transform=ax.transAxes, ha='right', va='bottom', fontsize=10,
        bbox=dict(boxstyle='round', facecolor='white', edgecolor='gray'))
fig.tight_layout()
fig.savefig('docs/assets/graph1.png', dpi=150)
plt.close(fig)
print(f'[graph1] k = {k:.4e} Н·м/рад, c = {c:.4e} Н·м, R² = {R2:.3f}, Δk = {Dk:.4e}')

# ============================================================
# ГРАФИК 2: T² = f(ℓ²)  (для диска с отверстиями)
# ============================================================
ell_sq_m2 = np.array([0.0, 9.0e-4, 3.6e-3])    # ℓ², м²
T_vals    = np.array([1.481, 1.571, 1.647])     # ⟨T⟩, с
dT_vals   = np.array([0.012, 0.008, 0.010])     # ΔT, с

T_sq = T_vals**2
dT2  = 2 * T_vals * dT_vals                     # Δ(T²) = 2T·ΔT

# ---- МНК: T² = α·ℓ² + b ----
n        = len(ell_sq_m2)
x_mean   = np.mean(ell_sq_m2)
y_mean   = np.mean(T_sq)
Sxx2     = np.sum((ell_sq_m2 - x_mean)**2)
Sxy2     = np.sum((ell_sq_m2 - x_mean) * (T_sq - y_mean))
alpha    = Sxy2 / Sxx2
b        = y_mean - alpha * x_mean

y_pred   = alpha * ell_sq_m2 + b
SS_res2  = np.sum((T_sq - y_pred)**2)
SS_tot2  = np.sum((T_sq - y_mean)**2)
R2_2     = 1 - SS_res2 / SS_tot2

x_cm2      = ell_sq_m2 * 1e4
x_line_cm2 = np.linspace(-0.5, 40, 200)
y_line     = alpha * (x_line_cm2 * 1e-4) + b

fig, ax = plt.subplots(figsize=(8, 5.5))
ax.errorbar(x_cm2, T_sq, yerr=dT2, fmt='o', color='black',
            ecolor='gray', elinewidth=1, capsize=4, markersize=7,
            zorder=3, label='Эксперимент')
ax.plot(x_line_cm2, y_line, color='tab:blue', lw=1.5,
        label=(f'МНК: $T^2 = {alpha*1e-4:.4f}\\cdot\\ell^2 + {b:.3f}$ '
               f'(по $\\ell^2$ в см$^2$)'))

ax.set_xlabel(r'Квадрат смещения оси $\ell^2$, см$^2$')
ax.set_ylabel(r'Квадрат периода $T^2$, с$^2$')
ax.set_title(r'Зависимость $T^2$ от $\ell^2$ для диска с отверстиями')
ax.set_xlim(-1, 40)
ax.grid(True, linestyle='--', alpha=0.6)
ax.legend(loc='lower right')
ax.text(0.03, 0.97,
        f'$\\alpha = {alpha:.1f}$ с$^2$/м$^2$\n$b = {b:.3f}$ с$^2$\n$R^2 = {R2_2:.3f}$',
        transform=ax.transAxes, va='top', fontsize=10,
        bbox=dict(boxstyle='round', facecolor='white', edgecolor='gray'))
fig.tight_layout()
fig.savefig('docs/assets/graph2.png', dpi=150)
plt.close(fig)
print(f'[graph2] α = {alpha:.2f} с²/м², b = {b:.4f} с², R² = {R2_2:.3f}')
