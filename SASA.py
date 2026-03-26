#!/usr/bin/env python3
import sys
import matplotlib.pyplot as plt
import numpy as np
import os

def load_sasa(path):
    """Load SASA data from a .xvg file, ignoring GROMACS headers."""
    x, y = [], []
    with open(path, 'r') as f:
        for line in f:
            if line.startswith(('#', '@')):
                continue
            parts = line.strip().split()
            if len(parts) == 2:
                time_ps = float(parts[0])
                sasa_nm2 = float(parts[1])
                x.append(time_ps / 1000.0)       # Time in ns
                y.append(sasa_nm2 * 100.0)       # SASA in Å²
    return np.array(x), np.array(y)

def smooth_curve(y, degree=35):
    """Apply Gaussian smoothing to a curve."""
    window = degree * 2 - 1
    weight = np.array([1.0] * window)
    weight_gauss = [1 / np.exp((4 * ((i - degree + 1) / float(window)) ** 2)) for i in range(window)]
    weight *= np.array(weight_gauss)
    smoothed = [sum(np.array(y[i:i+window]) * weight) / sum(weight) for i in range(len(y) - window)]
    return np.array(smoothed)

def main():
    if len(sys.argv) < 2:
        print("Usage: ./sasa.py sasa1.xvg sasa2.xvg ...")
        sys.exit(1)

    files = sys.argv[1:]

    # Colors for overlay and accessibility
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

    plt.figure(figsize=(10, 6))
    for i, file in enumerate(files):
        if not os.path.isfile(file):
            print(f"File not found: {file}")
            continue

        x, y = load_sasa(file)
        label = os.path.splitext(os.path.basename(file))[0]
        color = colors[i % len(colors)]  # cyclic use of optimized palette

        # Original curve with lighter transparency and thinner line
        plt.plot(x, y, label=label, color=color, alpha=0.2, linewidth=1.5)

        # Smoothed average curve with thicker line
        degree = 35
        if len(y) > degree * 2:
            y_smooth = smooth_curve(y, degree)
            x_smooth = x[degree:(-1)*(degree-1)]
            plt.plot(x_smooth, y_smooth, color=color, linewidth=2.8)

    plt.xlabel("Time [ns]", fontsize=12)
    plt.ylabel("SASA [Å²]", fontsize=12)
    plt.title("Solvent Accessible Surface Area (SASA)", fontsize=14)
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
