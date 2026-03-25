#!/usr/bin/env python3
import numpy as np
import glob

# Buscar todos los archivos .xvg
archivos = glob.glob("*.xvg")

for archivo in archivos:
    # Cargar datos, ignorando comentarios
    data = np.loadtxt(archivo, comments=["@", "#"])
    
    # Primera columna: tiempo en ps → convertir a ns
    tiempo_ns = data[:, 0] / 1000.0
    
    # Segunda columna: RMSD en nm → convertir a Å
    rmsd_ang = data[:, 1] * 10.0
    
    # Estadísticos
    mean = np.mean(rmsd_ang)
    std = np.std(rmsd_ang, ddof=1)  # desviación estándar muestral
    sem = std / np.sqrt(len(rmsd_ang))  # error estándar
    
    print(f"Archivo: {archivo}")
    print(f"  Promedio RMSD: {mean:.4f} Å")
    print(f"  Desviación estándar: {std:.4f} Å")
    print(f"  Error estándar: {sem:.4f} Å")
    print(f"  Tiempo inicial: {tiempo_ns[0]:.2f} ns | Tiempo final: {tiempo_ns[-1]:.2f} ns")
    print("-" * 50)
