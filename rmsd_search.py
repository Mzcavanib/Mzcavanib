#!/usr/bin/env python3
import sys

def search_rmsd(file, times_ns):
    results = {}
    with open(file) as f:
        for line in f:
            if line.startswith(("#", "@")):
                continue
            parts = line.split()
            if len(parts) < 2:
                continue
            try:
                time_ps = float(parts[0])        # time in ps
                rmsd_nm = float(parts[1])        # RMSD in nm

                time_ns = time_ps / 1000.0       # convert to ns
                rmsd_A = rmsd_nm * 10.0          # convert to Å

                # comparison with requested times (in ns)
                for t in times_ns:
                    if abs(time_ns - t) < 1e-6:  # floating-point tolerance
                        results[t] = rmsd_A
            except ValueError:
                continue
    return results

def main():
    if len(sys.argv) < 3:
        print("Usage: python3 search_rmsd.py file.xvg time1 time2 ...")
        sys.exit(1)

    file = sys.argv[1]
    times_ns = [float(t) for t in sys.argv[2:]]

    results = search_rmsd(file, times_ns)

    for t in times_ns:
        if t in results:
            print(f"Time {t:.3f} ns | RMSD {results[t]:.4f} Å")
        else:
            print(f"Time {t:.3f} ns | Not found in {file}")

if __name__ == "__main__":
    main()
