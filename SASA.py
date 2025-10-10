#!/usr/bin/env python3
import sys
import matplotlib.pyplot as plt
import numpy as np
import os

def cargar_sasa(path):
    """Carga datos SASA desde un archivo .xvg, ignorando encabezados de GROMACS."""
    x, y = [], []
    with open(path, 'r') as f:
        for line in f:
            if line.startswith(('#', '@')):
                continue
            parts = line.strip().split()
            if len(parts) == 2:
                tiempo_ps = float(parts[0])
                sasa_nm2 = float(parts[1])
                x.append(tiempo_ps / 1000.0)       # Tiempo en ns
                y.append(sasa_nm2 * 100.0)         # SASA en Å²
    return np.array(x), np.array(y)

def suavizar_curva(y, degree=35):
    """Aplica suavizado gaussiano a una curva."""
    window = degree * 2 - 1
    weight = np.array([1.0] * window)
    weight_gauss = [1 / np.exp((4 * ((i - degree + 1) / float(window)) ** 2)) for i in range(window)]
    weight *= np.array(weight_gauss)
    smoothed = [sum(np.array(y[i:i+window]) * weight) / sum(weight) for i in range(len(y) - window)]
    return np.array(smoothed)

def main():
    if len(sys.argv) < 2:
        print("Uso: ./sasa.py sasa1.xvg sasa2.xvg ...")
        sys.exit(1)

    archivos = sys.argv[1:]

    # Colores para superposición y accesibilidad
    colores = [
        (31/255, 119/255, 180/255),  # Azul profundo
        (214/255, 39/255, 40/255),   # Rojo carmín    
        (148/255, 103/255, 189/255), # Púrpura oscuro
        (140/255, 86/255, 75/255),   # Marrón tierra
        (23/255, 190/255, 207/255),  # Cian claro
        (44/255, 160/255, 44/255),   # Verde vibrante
        (255/255, 127/255, 14/255),  # Naranja intenso
        (227/255, 119/255, 194/255), # Rosa fuerte
        (127/255, 127/255, 127/255), # Gris medio
        (188/255, 189/255, 34/255)   # Amarillo dorado
    ]

    plt.figure(figsize=(10, 6))
    for i, archivo in enumerate(archivos):
        if not os.path.isfile(archivo):
            print(f"Archivo no encontrado: {archivo}")
            continue

        x, y = cargar_sasa(archivo)
        etiqueta = os.path.splitext(os.path.basename(archivo))[0]
        color = colores[i % len(colores)]  # uso cíclico de paleta optimizada

        # Curva original con transparencia más tenue y línea más intensa
        plt.plot(x, y, label=etiqueta, color=color, alpha=0.2, linewidth=1.5)

        # Curva promedio suavizada con línea más gruesa
        degree = 35
        if len(y) > degree * 2:
            y_suave = suavizar_curva(y, degree)
            x_suave = x[degree:(-1)*(degree-1)]
            plt.plot(x_suave, y_suave, color=color, linewidth=2.8)

    plt.xlabel("Tiempo [ns]", fontsize=12)
    plt.ylabel("SASA [Å²]", fontsize=12)
    plt.title("Área accesible al solvente (SASA)", fontsize=14)
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()

