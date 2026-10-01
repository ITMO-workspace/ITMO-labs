import numpy as np
import matplotlib.pyplot as plt
import os

# Ensure output directory exists
os.makedirs('docs/assets', exist_ok=True)

# Set font to support Cyrillic
plt.rcParams['font.family'] = 'DejaVu Sans'

# ========== Task 1 data ==========
x1 = 0.15  # m
x2_vals = np.array([0.40, 0.50, 0.70, 0.90, 1.10])  # m
t1_vals = np.array([1.3, 1.3, 1.3, 0.9, 1.4])       # s
t2_vals = np.array([2.5, 2.8, 3.4, 3.9, 4.5])       # s

Y = x2_vals - x1
Z = (t2_vals**2 - t1_vals**2) / 2.0

# Linear regression through origin: Y = a * Z
a_task1 = np.sum(Z * Y) / np.sum(Z**2)

# Plot Task 1
plt.figure(figsize=(8, 6))
plt.scatter(Z, Y, color='blue', label='Экспериментальные точки')
Z_fit = np.linspace(0, max(Z)*1.05, 100)
plt.plot(Z_fit, a_task1 * Z_fit, 'r-', label=f'Аппроксимация: Y = {a_task1:.4f}·Z')
plt.xlabel('Z = (t₂² - t₁²)/2, с²')
plt.ylabel('Y = x₂ - x₁, м')
plt.title('Зависимость Y = f(Z) (Задание 1)')
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()
plt.tight_layout()
plt.savefig('docs/assets/task1_graph.png', dpi=150)
plt.close()

print(f"Task 1: a = {a_task1:.6f} m/s²")

# ========== Task 2 data ==========
x1_task2 = 0.15  # m
x2_task2 = 1.10  # m
distance = x2_task2 - x1_task2  # 0.95 m

# Heights (mm)
h0 = 174.0
h0_prime = 174.0
X = 220.0
X_prime = 1000.0
L = X_prime - X  # 780 mm

h_list = np.array([183, 193, 203, 213, 223])       # mm
h_prime_list = np.array([174, 175, 177, 178, 179]) # mm

sin_alpha = np.abs(h_prime_list - h_list) / L

# Time measurements (5 runs each)
t1_meas = [
    [1.3, 1.0, 1.2, 1.2, 1.2],
    [0.9, 0.9, 0.9, 0.8, 0.9],
    [0.8, 0.7, 0.7, 0.7, 0.8],
    [0.7, 0.6, 0.6, 0.6, 0.6],
    [0.6, 0.6, 0.6, 0.6, 0.6]
]
t2_meas = [
    [3.4, 4.0, 4.3, 4.3, 4.3],
    [3.1, 3.1, 3.1, 3.0, 3.0],
    [2.5, 2.5, 2.5, 2.5, 2.5],
    [2.2, 2.1, 2.2, 2.2, 2.2],
    [2.0, 2.0, 2.0, 2.0, 2.0]
]

mean_t1 = np.array([np.mean(run) for run in t1_meas])
mean_t2 = np.array([np.mean(run) for run in t2_meas])

a_task2 = 2.0 * distance / (mean_t2**2 - mean_t1**2)

# Linear fit: a = A + B * sin(alpha)
B, A = np.polyfit(sin_alpha, a_task2, 1)  # B = g, A = intercept

# Plot Task 2
plt.figure(figsize=(8, 6))
plt.scatter(sin_alpha, a_task2, color='blue', label='Экспериментальные точки')
sin_fit = np.linspace(0, max(sin_alpha)*1.1, 100)
plt.plot(sin_fit, A + B * sin_fit, 'r-', label=f'Аппроксимация: a = {A:.4f} + {B:.4f}·sin α')
plt.xlabel('sin α')
plt.ylabel('a, м/с²')
plt.title('Зависимость a = f(sin α) (Задание 2)')
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()
plt.tight_layout()
plt.savefig('docs/assets/task2_graph.png', dpi=150)
plt.close()

print(f"Task 2: g = B = {B:.6f} m/s², A = {A:.6f} m/s²")
print("Plots saved to docs/assets/task1_graph.png and docs/assets/task2_graph.png")