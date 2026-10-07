#!/usr/bin/env python3
"""
Генерация графиков T^2 = f(4π²/g_эфф) для трех положений груза
лабораторной работы №1.08 "Маятник с переменным ускорением свободного падения"
"""
import numpy as np
import matplotlib.pyplot as plt
import os

os.makedirs(os.path.join('docs', 'assets'), exist_ok=True)
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 11

g = 9.82  # м/с²
pi2_4 = 4 * np.pi**2

# Углы и периоды для трех положений груза (по данным из main.tex)
alpha_deg = np.array([0, 10, 20, 30, 40, 50, 60], dtype=float)
alpha_rad = np.deg2rad(alpha_deg)
cos_alpha = np.cos(alpha_rad)
g_eff = g * cos_alpha
x_data = pi2_4 / g_eff          # 4π² / g_эфф

# Периоды (с) для трех положений груза
T1 = np.array([0.9078, 0.9148, 0.9365, 0.9755, 1.0372, 1.1323, 1.2838])
T2 = np.array([0.8045, 0.8107, 0.8299, 0.8645, 0.9192, 1.0034, 1.1378])
T3 = np.array([0.6916, 0.6970, 0.7134, 0.7432, 0.7902, 0.8627, 0.9781])

# Погрешности периода (инструментальная + на глаз)
dT = 0.005  # с
y_err = 2 * T1 * dT  # Δ(T²) = 2T·ΔT


def fit_through_origin(x, y):
    """МНК для y = k*x (через начало координат)."""
    k = np.sum(x * y) / np.sum(x**2)
    d = y - k * x
    S_k = np.sqrt(np.sum(d**2) / ((len(x) - 1) * np.sum(x**2)))
    return k, S_k


def make_plot(x, T, k, S_k, label_title, filename, color='tab:blue'):
    y = T**2
    fig, ax = plt.subplots(figsize=(7.5, 5.5))

    ax.errorbar(x, y, yerr=y_err, fmt='o', color=color,
                ecolor='gray', elinewidth=1, capsize=3,
                markersize=7, label='Экспериментальные точки')

    x_fit = np.linspace(0, max(x) * 1.05, 100)
    ax.plot(x_fit, k * x_fit, 'r-', lw=1.5,
            label=f'Аппроксимация: $T^2 = \\ell_{{\\rm пр}} \\cdot \\frac{{4\\pi^2}}{{g_{{\\rm эфф}}}}$')

    ax.set_xlabel(r'$\dfrac{4\pi^2}{g_{\rm эфф}}$, с$^2$/м')
    ax.set_ylabel(r'$T^2$, с$^2$')
    ax.set_title(label_title)
    ax.set_xlim(0, max(x) * 1.08)
    ax.set_ylim(0, max(y) * 1.10)
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.legend(loc='upper left')

    # Подпись со значением приведенной длины
    ax.text(0.97, 0.05,
            f'$\\ell_{{\\rm пр}} = ({k*100:.1f} \\pm {2*S_k*100:.1f})$ см',
            transform=ax.transAxes, ha='right', va='bottom',
            bbox=dict(boxstyle='round', facecolor='white', edgecolor='gray'))

    fig.tight_layout()
    fig.savefig(filename, dpi=150)
    plt.close(fig)

    print(f'{label_title}:  ℓ_пр = ({k*100:.2f} ± {2*S_k*100:.2f}) см')


# === Три графика ===
k1, S1 = fit_through_origin(x_data, T1**2)
make_plot(x_data, T1, k1, S1,
          r'$l = 20{,}67$ см ($2/3$ длины стержня)',
          'docs/assets/graph1.png', color='tab:blue')

k2, S2 = fit_through_origin(x_data, T2**2)
make_plot(x_data, T2, k2, S2,
          r'$l = 15{,}50$ см ($1/2$ длины стержня)',
          'docs/assets/graph2.png', color='tab:green')

k3, S3 = fit_through_origin(x_data, T3**2)
make_plot(x_data, T3, k3, S3,
          r'$l = 10{,}33$ см ($1/3$ длины стержня)',
          'docs/assets/graph3.png', color='tab:orange')

# === Совмещенный график (опционально) ===
fig, ax = plt.subplots(figsize=(8, 5.5))
for T, k, c, lab in [(T1, k1, 'tab:blue',  '20.67 см'),
                     (T2, k2, 'tab:green', '15.50 см'),
                     (T3, k3, 'tab:orange','10.33 см')]:
    y = T**2
    x_fit = np.linspace(0, max(x_data) * 1.05, 100)
    ax.errorbar(x_data, y, yerr=y_err, fmt='o', color=c,
                ecolor='gray', elinewidth=1, capsize=3,
                markersize=6, label=f'l = {lab}')
    ax.plot(x_fit, k * x_fit, '-', color=c, lw=1.3)

ax.set_xlabel(r'$\dfrac{4\pi^2}{g_{\rm эфф}}$, с$^2$/м')
ax.set_ylabel(r'$T^2$, с$^2$')
ax.set_title('Зависимость $T^2$ от $4\\pi^2/g_{\\rm эфф}$ для трех положений груза')
ax.set_xlim(0, max(x_data) * 1.08)
ax.grid(True, linestyle='--', alpha=0.6)
ax.legend(loc='upper left')
fig.tight_layout()
fig.savefig('docs/assets/graph_combined.png', dpi=150)
plt.close(fig)

print('\nГрафики сохранены в docs/assets/graph1.png, graph2.png, graph3.png, graph_combined.png')