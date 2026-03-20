import numpy as np
import glob

archivos = glob.glob("*.xvg")

for archivo in archivos:
    # Carga los datos, ignorando comentarios
    data = np.loadtxt(archivo, comments=["@", "#"])
    
    # Segunda columna (RMSD)
    rmsd = data[:, 1]
    
    # Estadísticos
    mean = np.mean(rmsd)
    std = np.std(rmsd, ddof=1)  # desviación estándar muestral
    sem = std / np.sqrt(len(rmsd))  # error estándar
    
    
    print(f"Archivo: {archivo}")
    print(f"  Promedio RMSD: {mean:.4f}")
    print(f"  Desviación estándar: {std:.4f}")
    print(f"  Error estándar: {sem:.4f}")
    print("-" * 40)


