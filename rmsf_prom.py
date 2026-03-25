#!/usr/bin/env python3
import sys

def leer_rmsf(archivo, residuos):
    valores = {}
    with open(archivo) as f:
        for linea in f:
            if linea.startswith(("#", "@")):
                continue
            partes = linea.split()
            if len(partes) < 2:
                continue
            try:
                res = int(partes[0])
                rmsf_nm = float(partes[1])   # valor en nm
                rmsf_ang = rmsf_nm * 10.0    # convertir a Å
                if res in residuos:
                    valores[res] = rmsf_ang
            except ValueError:
                continue
    return valores

def main():
    if len(sys.argv) < 3:
        print("Uso: python3 rmsf_avg.py rmsf*.xvg #res #res ...")
        sys.exit(1)

    archivos = []
    residuos = []
    for arg in sys.argv[1:]:
        if arg.endswith(".xvg"):
            archivos.append(arg)
        else:
            residuos.append(int(arg))

    acumulados = {res: [] for res in residuos}

    for archivo in archivos:
        valores = leer_rmsf(archivo, residuos)
        for res in residuos:
            if res in valores:
                acumulados[res].append((archivo, valores[res]))
                print(f"Residuo {res} | Archivo {archivo} | RMSF {valores[res]:.4f} Å")

    print("\n--- Promedios ---")
    for res in residuos:
        if acumulados[res]:
            promedio = sum(v for _, v in acumulados[res]) / len(acumulados[res])
            print(f"Residuo {res} | Promedio RMSF: {promedio:.4f} Å")
        else:
            print(f"Residuo {res} | No encontrado en archivos")

if __name__ == "__main__":
    main()

