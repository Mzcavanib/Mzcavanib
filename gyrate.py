#!/usr/bin/env python3
import sys
import matplotlib.pyplot as plt
import numpy as np
import os

def load_gyrate(path, column=1):
    """Load radius of gyration data from .xvg file, ignoring GROMACS headers."""
    x, y = [], []
    with open(path, 'r') as f:
        for line in f:
            if line.startswith(('#', '@')):
                continue
            parts = line.strip().split()
            if len(parts) > column:
                try:
                    time_ps = float(parts[0])
                    rg_nm = float(parts[column])
                    x.append(time_ps / 1000.0)     # ns
                    y.append(rg_nm * 10.0)         # Å
                except ValueError:
                    continue
    return np.array(x), np.array(y)

def smooth_curve(x, y, degree=35):
    """Apply Gaussian smoothing to the curve."""
    window = degree * 2 - 1
    if len(y) < window:
        return None, None
    weight = np.array([1.0] * window)
    weight_gauss = [1 / np.exp((4 * ((i - degree + 1) / float(window)) ** 2)) for i in range(window)]
    weight *= np.array(weight_gauss)
    y_smooth = [sum(np.array(y[i:i+window]) * weight) / sum(weight) for i in range(len(y) - window)]
    x_smooth = x[degree:(-1)*(degree-1)]
    return np.array(x_smooth), np.array(y_smooth)

def main():
    if len(sys.argv) < 2:
        print("Usage: ./gyrate.py file1.xvg file2.xvg ...")
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

    fig = plt.figure(figsize=(10, 6), constrained_layout=True)
    plotted = False

    for i, file in enumerate(files):
        if not os.path.isfile(file):
            print(f"File not found: {file}")
            continue

        x, y = load_gyrate(file, column=1)
        if len(x) == 0 or len(y) == 0:
            print(f"Empty or unreadable file: {file}")
            continue

        label = os.path.splitext(os.path.basename(file))[0]
        color = colors[i % len(colors)]

        plt.plot(x, y, label=label, color=color, alpha=0.2, linewidth=2.0)
        plotted = True

        x_smooth, y_smooth = smooth_curve(x, y)
        if x_smooth is not None and y_smooth is not None:
            plt.plot(x_smooth, y_smooth, color=color, linewidth=2.8)

    if not plotted:
        print("Could not plot any valid file.")
        sys.exit(1)

    plt.xlabel("Time [ns]", fontsize=12)
    plt.ylabel("Radius of gyration [Å]", fontsize=12)
    plt.title("Radius of gyration during simulation", fontsize=14)
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.show()

if __name__ == "__main__":
    main()
