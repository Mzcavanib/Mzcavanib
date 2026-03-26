#!/usr/bin/env python3
import sys
import matplotlib.pyplot as plt
import numpy as np
import os

def load_rmsf(path):
    """Load RMSF data from a .xvg file, ignoring GROMACS headers."""
    x, y = [], []
    with open(path, 'r') as f:
        for line in f:
            if line.startswith(('#', '@')):
                continue
            parts = line.strip().split()
            if len(parts) == 2:
                x.append(int(parts[0]))           # Residue
                y.append(float(parts[1]) * 10.0)  # RMSF in Ångström
    return np.array(x), np.array(y)

def main():
    if len(sys.argv) < 2:
        print("Usage: ./plot.py file1.xvg file2.xvg ...")
        sys.exit(1)

    files = sys.argv[1:]

    # Fixed labels for the first five files
    fixed_labels = ["WT", "Alpha", "Gamma", "Delta", "Omicron BA.1"]

    # Optimized palette for overlay and accessibility
    colors = [
        (31/255, 119/255, 180/255),  # Deep blue
        (214/255, 39/255, 40/255),   # Crimson red    
        (148/255, 103/255, 189/255), # Dark purple
        (255/255, 127/255, 14/255),  # Intense orange
        (44/255, 160/255, 44/255),   # Vibrant green
        (23/255, 190/255, 207/255),  # Light cyan
        (140/255, 86/255, 75/255),   # Earth brown
        (227/255, 119/255, 194/255), # Strong pink
        (127/255, 127/255, 127/255), # Medium gray
        (188/255, 189/255, 34/255)   # Golden yellow
    ]

    plt.figure(figsize=(10, 6))
    for i, file in enumerate(files):
        if not os.path.isfile(file):
            print(f"File not found: {file}")
            continue

        x, y = load_rmsf(file)

        # Assign labels: first five with fixed names, rest with file name
        if i < len(fixed_labels):
            label = fixed_labels[i]
        else:
            label = os.path.splitext(os.path.basename(file))[0]

        color = colors[i % len(colors)]
        plt.plot(x, y, label=label, color=color, linewidth=1.5)

    plt.xlabel("Residue", fontsize=12)
    plt.ylabel("RMSF [Å]", fontsize=12)
    plt.title("RMSF fluctuations comparison", fontsize=14)
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
