#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
import sys
import os
from scipy.stats import gaussian_kde  # ← añadido para suavizar histogramas

def smooth_gaussian(data, degree=35):
    """Suavizado extremo tipo gaussiano para curvas RMSD."""
    window = degree * 2 - 1
    weight = np.array([1.0] * window)
    weight_gauss = [1 / np.exp((4 * ((i - degree + 1) / float(window)) ** 2)) for i in range(window)]
    weight *= np.array(weight_gauss)
    smoothed = [sum(np.array(data[i:i+window]) * weight) / sum(weight) for i in range(len(data) - window)]
    return np.array(smoothed)

def read_xvg(filepath):
    """Lee archivos .xvg ignorando encabezados de GROMACS."""
    data = []
    with open(filepath, 'r') as f:
        for line in f:
            if not line.startswith(('@', '#')):
                parts = line.strip().split()
                data.append(parts)
    return np.array(data)

def get_column(data, col):
    """Extrae una columna específica como array flotante."""
    return np.array([float(row[col]) for row in data])

# Validación de entrada
if len(sys.argv) < 2:
    print("Uso: ./plot.py archivo1.xvg archivo2.xvg ...")
    sys.exit(1)

archivos = sys.argv[1:]
colors = plt.cm.tab10.colors  # ← paleta uniforme y reproducible

fig = plt.figure(figsize=(10, 6))
gs = fig.add_gridspec(1, 2, width_ratios=[4, 1], wspace=0.05)
ax_main = fig.add_subplot(gs[0])
ax_hist = fig.add_subplot(gs[1], sharey=ax_main)

for i, archivo in enumerate(archivos):
    if not os.path.isfile(archivo):
        print(f"Archivo no encontrado: {archivo}")
        continue

    data = read_xvg(archivo)
    tiempo_ps = get_column(data, 0)
    tiempo_ns = tiempo_ps / 1000.0
    rmsd_nm = get_column(data, 1)
    rmsd_angstrom = rmsd_nm * 10.0
    color = colors[i % len(colors)]  # ← uso uniforme

    # Curva original con transparencia
    ax_main.plot(tiempo_ns, rmsd_angstrom, color=color, alpha=0.3)

    # Línea suavizada más gruesa
    degree = 120
    if len(rmsd_angstrom) > degree * 2:
        rmsd_smooth = smooth_gaussian(rmsd_angstrom, degree)
        tiempo_smooth = tiempo_ns[degree:(-1)*(degree-1)]
        ax_main.plot(tiempo_smooth, rmsd_smooth, color=color, linewidth=1.5)

    # Histograma KDE desde 20 ns en adelante
    mask_20ns = tiempo_ns >= 20.0
    rmsd_post20 = rmsd_angstrom[mask_20ns]
    kde = gaussian_kde(rmsd_post20)
    rmsd_range = np.linspace(min(rmsd_post20), max(rmsd_post20), 500)
    density = kde(rmsd_range)
    ax_hist.plot(density, rmsd_range, color=color, linewidth=2)

# Ejes y estética
ax_main.set_xlabel("Tiempo [ns]", fontsize=12)
ax_main.set_ylabel("RMSD [Å]", fontsize=12)
ax_main.grid(True)

ax_hist.set_xlabel("Frecuencia", fontsize=12)
ax_hist.set_xlim(left=0)
ax_hist.tick_params(labelleft=False)

plt.tight_layout()
plt.show()

