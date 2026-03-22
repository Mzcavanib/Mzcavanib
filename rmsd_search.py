#!/usr/bin/env python3
import sys

def buscar_rmsd(archivo, tiempos_ns):
    resultados = {}
    with open(archivo) as f:
        for linea in f:
            if linea.startswith(("#", "@")):
                continue
            partes = linea.split()
            if len(partes) < 2:
                continue
            try:
                tiempo_ps = float(partes[0])        # tiempo en ps
                rmsd_nm = float(partes[1])          # RMSD en nm

                tiempo_ns = tiempo_ps / 1000.0      # convertir a ns
                rmsd_A = rmsd_nm * 10.0             # convertir a Å

                # comparación con los tiempos pedidos (en ns)
                for t in tiempos_ns:
                    if abs(tiempo_ns - t) < 1e-6:   # tolerancia por flotantes
                        resultados[t] = rmsd_A
            except ValueError:
                continue
    return resultados

def main():
    if len(sys.argv) < 3:
        print("Uso: python3 buscar_rmsd.py archivo.xvg tiempo1 tiempo2 ...")
        sys.exit(1)

    archivo = sys.argv[1]
    tiempos_ns = [float(t) for t in sys.argv[2:]]

    resultados = buscar_rmsd(archivo, tiempos_ns)

    for t in tiempos_ns:
        if t in resultados:
            print(f"Tiempo {t:.3f} ns | RMSD {resultados[t]:.4f} Å")
        else:
            print(f"Tiempo {t:.3f} ns | No encontrado en {archivo}")

if __name__ == "__main__":
    main()

