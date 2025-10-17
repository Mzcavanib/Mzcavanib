import subprocess
import os
os.environ["GMX_NO_X11"] = "1"
import sys

def run_command(command, description):
    print(f"\n{description}")
    print(f"Ejecutando: {command}")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print("Completado.")
        if result.stdout:
            print("STDOUT:", result.stdout.strip())
        if result.stderr:
            print("STDERR:", result.stderr.strip())
    except subprocess.CalledProcessError as e:
        print("Error al ejecutar el comando.")
        print("STDOUT:", e.stdout.strip() if e.stdout else "Sin salida.")
        print("STDERR:", e.stderr.strip() if e.stderr else "Sin errores.")
        sys.exit(1)

def run_gromacs_pipeline():
    # Archivos base
    input_xtc = "md.xtc"
    tpr_file = "md.tpr"

    # Verifica que los archivos existan
    for file in [input_xtc, tpr_file]:
        if not os.path.isfile(file):
            print(f"Error: No se encontró el archivo requerido '{file}' en el directorio actual.")
            sys.exit(1)

    # Paso 1: reconstruir molécula completa
    cmd1 = f"echo 1 | gmx_mpi trjconv -f {input_xtc} -s {tpr_file} -pbc whole -o whole.xtc"
    run_command(cmd1, "Paso 1: reconstruyendo molécula completa con -pbc whole")

    # Paso 2: solicitar valores de traslación
    try:
        x_trans = float(input("Ingresa el valor de traslación en x (ej. -3.0): "))
        y_trans = float(input("Ingresa el valor de traslación en y (ej. 0.0): "))
        z_trans = float(input("Ingresa el valor de traslación en z (ej. 0.0): "))
    except ValueError:
        print("Error: Los valores deben ser números reales.")
        sys.exit(1)

    # Paso 2: compactar y trasladar molécula con valores ingresados
    cmd2 = (
        f"echo 1 | gmx_mpi trjconv -f whole.xtc -s {tpr_file} "
        f"-pbc mol -ur compact -trans {x_trans} {y_trans} {z_trans} -o mol.xtc"
    )
    run_command(cmd2, f"Paso 2: compactando y trasladando molécula con -trans {x_trans} {y_trans} {z_trans}")

    # Paso 3: ajustar trayectoria
    cmd3 = f"echo 3 1 | gmx_mpi trjconv -f mol.xtc -s {tpr_file} -fit rot+trans -o final.xtc"
    run_command(cmd3, "Paso 3: ajustando trayectoria con -fit rot+trans")

    print("\nProceso finalizado correctamente. Puedes continuar con el análisis de 'final.xtc'.")

if __name__ == "__main__":
    run_gromacs_pipeline()
