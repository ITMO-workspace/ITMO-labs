#!/usr/bin/env python3
"""
Генерация графиков для л/р 1.04 (Маятник Обербека).
Запуск: python gen_plots_1_04.py
Результат: assets/graph1.png, assets/graph2.png
"""
import numpy as np
import matplotlib.pyplot as plt
import os

os.makedirs('assets', exist_ok=True)
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 11

# ============================================================
# ГРАФИК 1: M = f(ε) для 4 положений грузов
# ============================================================
# Данные из Таблицы 2 (ε в рад/с², M в Н·м)
# Каждая серия — 4 точки (1, 2, 3, 4 шайбы)
data_M_eps = {
    'Риска 1 ($R = 0.077$ м)': {
        'eps': np.array([2.878, 6.196, 9.343, 12.326]),
        'M':   np.array([0.0596, 0.1076, 0.1549, 0.2016]),
        'color': 'tab:blue', 'marker': 'o'
    },
    'Риска 2 ($R = 0.102$ м)': {
        'eps': np.array([2.248, 3.604, 5.378, 8.570]),
        'M':   np.array([0.0597, 0.1083, 0.1564, 0.2034]),
        'color': 'tab:green', 'marker': 's'
    },
    'Риска 3 ($R = 0.127$ м)': {
        'eps': np.array([1.878, 3.352, 5.057, 6.004]),
        'M':   np.array([0.0597, 0.1083, 0.1565, 0.2047]),
        'color': 'tab:orange', 'marker': '^'
    },
    'Риска 4 ($R = 0.152$ м)': {
        'eps': np.array([1.422, 2.213, 3.765, 4.948]),
        'M':   np.array([0.0598, 0.1086, 0.1570, 0.2052]),
        'color': 'tab:red', 'marker': 'D'
    }
}

fig, ax = plt.subplots(figsize=(8, 5.5))

for label, d in data_M_eps.items():
    eps = d['eps']
    M = d['M']
    color = d['color']
    marker = d['marker']

    # Точки
    ax.scatter(eps, M, color=color, marker=marker, s=45, zorder=3, label=label)

    # МНК: M = I * eps + M_tr
    coeffs = np.polyfit(eps, M, 1)
    I_fit, M_tr_fit = coeffs[0], coeffs[1]

    # Линия
    eps_line = np.linspace(0, eps.max() * 1.1, 100)
    ax.plot(eps_line, I_fit * eps_line + M_tr_fit, color=color, lw=1.2, linestyle='-')

# Погрешности для первой точки Риски 1
eps1, M1 = data_M_eps['Риска 1 ($R = 0.077$ м)']['eps'][0], data_M_eps['Риска 1 ($R = 0.077$ м)']['M'][0]
d_eps1, d_M1 = 0.13, 0.0007
ax.errorbar(eps1, M1, xerr=d_eps1, yerr=d_M1, fmt='none', ecolor='black', capsize=4, zorder=4)

ax.set_xlabel(r'Угловое ускорение $\varepsilon$, рад/с$^2$')
ax.set_ylabel(r'Момент силы $M$, Н$\cdot$м')
ax.set_title('Зависимость момента силы натяжения от углового ускорения')
ax.set_xlim(0, 14)
ax.set_ylim(0, 0.23)
ax.grid(True, linestyle='--', alpha=0.6)
ax.legend(loc='upper left', fontsize=9)

fig.tight_layout()
fig.savefig('docs/assets/graph1.png', dpi=150)
plt.close(fig)
print('Сохранён docs/assets/graph1.png')

# ============================================================
# ГРАФИК 2: I = f(R²) (теорема Штейнера)
# ============================================================
R_sq = np.array([0.00593, 0.01040, 0.01613, 0.02310])  # м²
I_vals = np.array([0.0151, 0.0223, 0.0348, 0.0406])    # кг·м²

fig, ax = plt.subplots(figsize=(8, 5.5))

# Экспериментальные точки
ax.scatter(R_sq, I_vals, color='tab:red', s=60, zorder=3,
           label='Экспериментальные значения $I(R^2)$')

# МНК: I = I_0 + b * R^2
coeffs = np.polyfit(R_sq, I_vals, 1)
b_fit, I0_fit = coeffs[0], coeffs[1]

x_fit = np.linspace(0, R_sq.max() * 1.05, 100)
y_fit = b_fit * x_fit + I0_fit

ax.plot(x_fit, y_fit, color='tab:red', lw=1.5,
        label=f'Аппроксимация МНК: $I = {b_fit:.2f} \\cdot 10^{{-2}} R^2 + {I0_fit*1e3:.2f} \\cdot 10^{{-3}}$')

# Выносим 10^-2 за скобки по осям для красоты (как в примере)
ax.ticklabel_format(axis='both', style='sci', scilimits=(-2, -2))

ax.set_xlabel(r'Квадрат расстояния $R^2$, м$^2$')
ax.set_ylabel(r'Момент инерции $I$, кг$\cdot$м$^2$')
ax.set_title('Зависимость момента инерции от квадрата расстояния $R^2$')
ax.set_xlim(0, 0.025)
ax.set_ylim(0, 0.045)
ax.grid(True, linestyle='--', alpha=0.6)
ax.legend(loc='upper left', fontsize=10)

fig.tight_layout()
fig.savefig('docs/assets/graph2.png', dpi=150)
plt.close(fig)
print('Сохранён docs/assets/graph2.png')