#!/usr/bin/env python3
import sys
import matplotlib.pyplot as plt
import numpy as np
import os

def cargar_gyrate(path, columna=1):
    x, y = [], []
    with open(path, 'r') as f:
        for line in f:
            if line.startswith(('#', '@')):
                continue
            parts = line.strip().split()
            if len(parts) > columna:
                try:
                    tiempo_ps = float(parts[0])
                    rg_nm = float(parts[columna])
                    x.append(tiempo_ps / 1000.0)     # ns
                    y.append(rg_nm * 10.0)           # Å
                except ValueError:
                    continue
    return np.array(x), np.array(y)

def suavizar_curva(x, y, degree=35):
    window = degree * 2 - 1
    if len(y) < window:
        return None, None
    weight = np.array([1.0] * window)
    weight_gauss = [1 / np.exp((4 * ((i - degree + 1) / float(window)) ** 2)) for i in range(window)]
    weight *= np.array(weight_gauss)
    y_suave = [sum(np.array(y[i:i+window]) * weight) / sum(weight) for i in range(len(y) - window)]
    x_suave = x[degree:(-1)*(degree-1)]
    return np.array(x_suave), np.array(y_suave)

def main():
    if len(sys.argv) < 2:
        print("Uso: ./gyrate.py archivo1.xvg archivo2.xvg ...")
        sys.exit(1)

    archivos = sys.argv[1:]
    colores = plt.cm.tab10.colors

    plt.figure(figsize=(10, 6))
    trazado = False

    for i, archivo in enumerate(archivos):
        if not os.path.isfile(archivo):
            print(f"Archivo no encontrado: {archivo}")
            continue

        x, y = cargar_gyrate(archivo, columna=1)  # ← usa columna 1: radio de giro total
        if len(x) == 0 or len(y) == 0:
            print(f"Archivo vacío o ilegible: {archivo}")
            continue

        etiqueta = os.path.splitext(os.path.basename(archivo))[0]
        color = colores[i % len(colores)]

        plt.plot(x, y, label=etiqueta, color=color, alpha=0.4, linewidth=1.5)
        trazado = True

        x_suave, y_suave = suavizar_curva(x, y)
        if x_suave is not None and y_suave is not None:
            plt.plot(x_suave, y_suave, color=color, linewidth=2.2)

    if not trazado:
        print("No se pudo graficar ningún archivo válido.")
        sys.exit(1)

    plt.xlabel("Tiempo [ns]", fontsize=12)
    plt.ylabel("Radio de giro [Å]", fontsize=12)
    plt.title("Radio de giro durante la simulación", fontsize=14)
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()


