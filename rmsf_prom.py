#!/usr/bin/env python3
import sys

def read_rmsf(file, residues):
    values = {}
    with open(file) as f:
        for line in f:
            if line.startswith(("#", "@")):
                continue
            parts = line.split()
            if len(parts) < 2:
                continue
            try:
                res = int(parts[0])
                rmsf_nm = float(parts[1])   # value in nm
                rmsf_ang = rmsf_nm * 10.0   # convert to Å
                if res in residues:
                    values[res] = rmsf_ang
            except ValueError:
                continue
    return values

def main():
    if len(sys.argv) < 3:
        print("Usage: python3 rmsf_avg.py rmsf*.xvg #res #res ...")
        sys.exit(1)

    files = []
    residues = []
    for arg in sys.argv[1:]:
        if arg.endswith(".xvg"):
            files.append(arg)
        else:
            residues.append(int(arg))

    accumulated = {res: [] for res in residues}

    for file in files:
        values = read_rmsf(file, residues)
        for res in residues:
            if res in values:
                accumulated[res].append((file, values[res]))
                print(f"Residue {res} | File {file} | RMSF {values[res]:.4f} Å")

    print("\n--- Averages ---")
    for res in residues:
        if accumulated[res]:
            average = sum(v for _, v in accumulated[res]) / len(accumulated[res])
            print(f"Residue {res} | Average RMSF: {average:.4f} Å")
        else:
            print(f"Residue {res} | Not found in files")

if __name__ == "__main__":
    main()
