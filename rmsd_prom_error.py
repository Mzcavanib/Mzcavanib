#!/usr/bin/env python3
import numpy as np
import glob

# Find all .xvg files
files = glob.glob("*.xvg")

for file in files:
    # Load data, ignoring comments
    data = np.loadtxt(file, comments=["@", "#"])
    
    # First column: time in ps → convert to ns
    time_ns = data[:, 0] / 1000.0
    
    # Second column: RMSD in nm → convert to Å
    rmsd_ang = data[:, 1] * 10.0
    
    # Statistics
    mean = np.mean(rmsd_ang)
    std = np.std(rmsd_ang, ddof=1)  # sample standard deviation
    sem = std / np.sqrt(len(rmsd_ang))  # standard error
    
    print(f"File: {file}")
    print(f"  RMSD mean: {mean:.4f} Å")
    print(f"  Standard deviation: {std:.4f} Å")
    print(f"  Standard error: {sem:.4f} Å")
    print(f"  Initial time: {time_ns[0]:.2f} ns | Final time: {time_ns[-1]:.2f} ns")
    print("-" * 50)
