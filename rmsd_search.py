#!/usr/bin/env python3
import sys

def buscar_rmsd(archivo, tiempos):
    resultados = {}
    with open(archivo) as f:
        for linea in f:
            if linea.startswith(("#", "@")):
                continue
            partes = linea.split()
            if len(partes) < 2:
                continue
            try:
                tiempo = float(partes[0])
                rmsd = float(partes[1])
                if tiempo in tiempos:
                    resultados[tiempo] = rmsd
            except ValueError:
                continue
    return resultados

def main():
    if len(sys.argv) < 3:
        print("Uso: python3 buscar_rmsd.py archivo.xvg tiempo1 tiempo2 ...")
        sys.exit(1)

    archivo = sys.argv[1]
    tiempos = [float(t) for t in sys.argv[2:]]

    resultados = buscar_rmsd(archivo, tiempos)

    for t in tiempos:
        if t in resultados:
            print(f"Tiempo {t:.3f} ns | RMSD {resultados[t]:.4f} Å")
        else:
            print(f"Tiempo {t:.3f} ns | No encontrado en {archivo}")

if __name__ == "__main__":
    main()

