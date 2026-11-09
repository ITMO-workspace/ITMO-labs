#!/usr/bin/env python3
"""Генерация объединённого графика для л/р 1.08."""
import numpy as np
import matplotlib.pyplot as plt
import os

os.makedirs(os.path.join('docs', 'assets'), exist_ok=True)
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 11

g = 9.82
alpha_deg = np.array([0, 10, 20, 30, 40, 50, 60], dtype=float)
alpha_rad = np.deg2rad(alpha_deg)
cos_alpha = np.cos(alpha_rad)
x = 4 * np.pi**2 / (g * cos_alpha)

data = {
    r'$l = 20.67$ см': np.array([0.908, 0.915, 0.937, 0.976, 1.037, 1.132, 1.284]),
    r'$l = 15.50$ см': np.array([0.804, 0.810, 0.830, 0.864, 0.919, 1.003, 1.138]),
    r'$l = 10.33$ см': np.array([0.692, 0.697, 0.713, 0.743, 0.790, 0.863, 0.978]),
}
colors = ['tab:blue', 'tab:green', 'tab:orange']
markers = ['o', 's', '^']

fig, ax = plt.subplots(figsize=(9, 6))
x_fit = np.linspace(0, x.max() * 1.05, 100)

for (label, T), c, m in zip(data.items(), colors, markers):
    y = T**2
    k = np.sum(x * y) / np.sum(x**2)
    ax.scatter(x, y, color=c, marker=m, s=55, zorder=3, label=f'{label}: $T^2 = {k*100:.2f}\\cdot 10^{{-2}} x$')
    ax.plot(x_fit, k * x_fit, color=c, lw=1.4)

ax.set_xlabel(r'$4\pi^2/g_{\text{эфф}}$, с$^2$/м')
ax.set_ylabel(r'$T^2$, с$^2$')
ax.set_title('Зависимость $T^2$ от $4\\pi^2/g_{\\text{эфф}}$ для трёх положений груза')
ax.set_xlim(0, x.max() * 1.08)
ax.set_ylim(0, 1.8)
ax.grid(True, linestyle='--', alpha=0.6)
ax.legend(loc='upper left', fontsize=10)

fig.tight_layout()
fig.savefig('docs/assets/graph_all.png', dpi=150)
plt.close(fig)
print('Сохранён docs/assets/graph_all.png')