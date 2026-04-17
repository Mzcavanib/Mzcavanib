#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
import sys
import os
from scipy.stats import gaussian_kde  # For histogram smoothing

def smooth_gaussian(data, degree=35):
    """Extreme Gaussian-like smoothing for RMSD curves."""
    window = degree * 2 - 1
    weight = np.array([1.0] * window)
    weight_gauss = [1 / np.exp((4 * ((i - degree + 1) / float(window)) ** 2)) for i in range(window)]
    weight *= np.array(weight_gauss)
    smoothed = [sum(np.array(data[i:i+window]) * weight) / sum(weight) for i in range(len(data) - window)]
    return np.array(smoothed)

def read_xvg(filepath):
    """Read .xvg files ignoring GROMACS headers."""
    data = []
    with open(filepath, 'r') as f:
        for line in f:
            if not line.startswith(('@', '#')):
                parts = line.strip().split()
                data.append(parts)
    return np.array(data)

def get_column(data, col):
    """Extract a specific column as a float array."""
    return np.array([float(row[col]) for row in data])


if len(sys.argv) < 2:
    print("Usage: ./plot.py file1.xvg file2.xvg ...")
    sys.exit(1)

files = sys.argv[1:]


colors = [
    (31/255, 119/255, 180/255),  # Deep blue
    (214/255, 39/255, 40/255),   # Crimson red    
    (148/255, 103/255, 189/255), # Dark purple
    (140/255, 86/255, 75/255),   # Earth brown
    (23/255, 190/255, 207/255),  # Light cyan
    (44/255, 160/255, 44/255),   # Vibrant green
    (255/255, 127/255, 14/255),  # Intense orange
    (227/255, 119/255, 194/255), # Strong pink
    (127/255, 127/255, 127/255), # Medium gray
    (188/255, 189/255, 34/255)   # Golden yellow
]


fig = plt.figure(figsize=(10, 6), constrained_layout=True)
gs = fig.add_gridspec(1, 2, width_ratios=[4, 1])
ax_main = fig.add_subplot(gs[0])
ax_hist = fig.add_subplot(gs[1], sharey=ax_main)

labels = [
    "WT",
    "Alpha",
    "Gamma",
    "Delta",
    "Omicron BA.1"
]

for i, file in enumerate(files):
    if not os.path.isfile(file):
        print(f"File not found: {file}")
        continue

    data = read_xvg(file)
    time_ps = get_column(data, 0)
    time_ns = time_ps / 1000.0
    rmsd_nm = get_column(data, 1)
    rmsd_angstrom = rmsd_nm * 10.0
    color = colors[i % len(colors)]  # cyclic use of optimized palette

    ax_main.plot(time_ns, rmsd_angstrom, color=color, alpha=0.3, label=labels[i] if i < len(labels) else f"Input {i+1}")

    degree = 120
    if len(rmsd_angstrom) > degree * 2:
        rmsd_smooth = smooth_gaussian(rmsd_angstrom, degree)
        time_smooth = time_ns[degree:(-1)*(degree-1)]
        ax_main.plot(time_smooth, rmsd_smooth, color=color, linewidth=1.5)

    mask_20ns = time_ns >= 20.0
    rmsd_post20 = rmsd_angstrom[mask_20ns]
    kde = gaussian_kde(rmsd_post20)
    rmsd_range = np.linspace(min(rmsd_post20), max(rmsd_post20), 500)
    density = kde(rmsd_range)
    ax_hist.plot(density, rmsd_range, color=color, linewidth=3)

plt.tick_params(axis='both', which='major', labelsize=20)
plt.rcParams['font.family'] = 'serif'

ax_main.set_xlabel("Tiempo [ns]", fontsize=20, labelpad=10)
ax_main.set_ylabel("RMSD [Å]", fontsize=20, labelpad=10)
ax_main.set_xticklabels(ax_main.get_xticks(), fontsize=20)
ax_main.set_yticklabels(ax_main.get_yticks(), fontsize=20)
ax_main.grid(True)
plt.tick_params(axis='both', which='major', labelsize=20)
plt.rcParams['font.family'] = 'serif'

#ax_hist.set_xlabel("Frecuencia", fontsize=25, labelpad=10)
ax_hist.set_xlim(left=0)
ax_hist.tick_params(labelleft=False)

ax_main.legend(loc="lower right", fontsize=10, frameon=True)

plt.show()
