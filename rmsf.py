#!/usr/bin/env python3
import sys
import matplotlib.pyplot as plt
import numpy as np
import os

def cargar_rmsf(path):
    """Carga datos RMSF desde un archivo .xvg, ignorando encabezados de GROMACS."""
    x, y = [], []
    with open(path, 'r') as f:
        for line in f:
            if line.startswith(('#', '@')):
                continue
            parts = line.strip().split()
            if len(parts) == 2:
                x.append(int(parts[0]))           # Residuo
                y.append(float(parts[1]) * 10.0)  # RMSF en Ångström
    return np.array(x), np.array(y)

def main():
    if len(sys.argv) < 2:
        print("Uso: ./plot.py archivo1.xvg archivo2.xvg ...")
        sys.exit(1)

    archivos = sys.argv[1:]
    colores = plt.cm.tab10.colors  # Paleta de 10 colores distintos

    plt.figure(figsize=(10, 6))
    for i, archivo in enumerate(archivos):
        if not os.path.isfile(archivo):
            print(f"Archivo no encontrado: {archivo}")
            continue

        x, y = cargar_rmsf(archivo)
        etiqueta = os.path.splitext(os.path.basename(archivo))[0]
        color = colores[i % len(colores)]
        plt.plot(x, y, label=etiqueta, color=color, linewidth=1.5)  # ← grosor ajustado

    plt.xlabel("Residuo", fontsize=12)
    plt.ylabel("RMSF (Å)", fontsize=12)  # ← unidad corregida
    plt.title("Comparación de fluctuaciones RMSF", fontsize=14)
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()

