#!/usr/bin/env python3
import sys
import matplotlib.pyplot as plt
import numpy as np
import os

def cargar_gyrate(path, columna=1):
    """Carga datos de radio de giro desde archivo .xvg, ignorando encabezados de GROMACS."""
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
    """Aplica suavizado gaussiano a la curva."""
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

    fig = plt.figure(figsize=(10, 6), constrained_layout=True)
    trazado = False

    for i, archivo in enumerate(archivos):
        if not os.path.isfile(archivo):
            print(f"Archivo no encontrado: {archivo}")
            continue

        x, y = cargar_gyrate(archivo, columna=1)
        if len(x) == 0 or len(y) == 0:
            print(f"Archivo vacío o ilegible: {archivo}")
            continue

        etiqueta = os.path.splitext(os.path.basename(archivo))[0]
        color = colores[i % len(colores)]

        plt.plot(x, y, label=etiqueta, color=color, alpha=0.2, linewidth=2.0)
        trazado = True

        x_suave, y_suave = suavizar_curva(x, y)
        if x_suave is not None and y_suave is not None:
            plt.plot(x_suave, y_suave, color=color, linewidth=2.8)

    if not trazado:
        print("No se pudo graficar ningún archivo válido.")
        sys.exit(1)

    plt.xlabel("Tiempo [ns]", fontsize=12)
    plt.ylabel("Radio de giro [Å]", fontsize=12)
    plt.title("Radio de giro durante la simulación", fontsize=14)
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.show()

if __name__ == "__main__":
    main()

