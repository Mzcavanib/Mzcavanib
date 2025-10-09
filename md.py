#!/usr/bin/env python3
import subprocess
import sys
import os

# Desactivar X11 en todo el entorno
os.environ["GMX_NO_X11"] = "1"
os.environ["DISPLAY"] = ""

def run_command(command, description):
    print(f"\n{description}")
    print(f"Ejecutando: {command}")
    env = os.environ.copy()
    try:
        subprocess.run(command, shell=True, check=True, env=env)
    except subprocess.CalledProcessError as e:
        print("Error al ejecutar el comando.")
        sys.exit(1)

def main():
    if len(sys.argv) != 2 or not sys.argv[1].endswith(".pdb"):
        print("Uso: ./md_sim.py archivo.pdb")
        sys.exit(1)

    pdb_file = sys.argv[1]
    base_name = os.path.splitext(pdb_file)[0]

    # Paso 1: pdb2gmx (interactivo)
    print("\nPaso 1: Selecciona manualmente el campo de fuerza y el modelo de agua cuando se te solicite.")
    cmd1 = f"gmx_mpi pdb2gmx -f {pdb_file} -o {base_name}.gro"
    run_command(cmd1, "Generando topología con pdb2gmx")

    # Paso 2: editconf
    cmd2 = f"gmx_mpi editconf -f {base_name}.gro -o box.gro -c -d 2.0 -bt cubic"
    run_command(cmd2, "Paso 2: Definiendo caja con editconf")

    # Paso 3: solvate
    cmd3 = f"gmx_mpi solvate -cp box.gro -cs spc216.gro -o solv.gro -p topol.top"
    run_command(cmd3, "Paso 3: Solvatando con spc216")

    # Paso 4: grompp para iones
    cmd4 = f"gmx_mpi grompp -f ../MDPs/ions.mdp -c solv.gro -p topol.top -o ions.tpr"
    run_command(cmd4, "Paso 4: Preparando sistema para inserción de iones")

    # Paso 5: genion (interactivo)
    print("\nPaso 5: Selecciona manualmente el grupo 'SOL' cuando se te solicite.")
    cmd5 = f"gmx_mpi genion -s ions.tpr -o ions.gro -p topol.top -pname NA -nname CL -neutral"
    run_command(cmd5, "Insertando iones con genion")

    # Paso 6: grompp para minimización
    cmd6 = f"gmx_mpi grompp -f ../MDPs/minim.mdp -c ions.gro -p topol.top -o em.tpr"
    run_command(cmd6, "Paso 6: Preparando minimización energética")

    # Paso 7: mdrun minimización
    cmd7 = f"gmx_mpi mdrun -v -deffnm em"
    run_command(cmd7, "Paso 7: Ejecutando minimización energética")

    # Paso 8: grompp para NVT
    cmd8 = f"gmx_mpi grompp -f ../MDPs/nvt.mdp -c em.gro -r em.gro -p topol.top -o nvt.tpr"
    run_command(cmd8, "Paso 8: Preparando simulación NVT")

    # Paso 9: mdrun NVT
    cmd9 = f"gmx_mpi mdrun -deffnm nvt -v -nb gpu -bonded gpu -pme gpu -pin on -update gpu"
    run_command(cmd9, "Paso 9: Ejecutando simulación NVT")

    # Paso 10: grompp para NPT
    cmd10 = f"gmx_mpi grompp -f ../MDPs/npt.mdp -c nvt.gro -r nvt.gro -t nvt.cpt -p topol.top -o npt.tpr"
    run_command(cmd10, "Paso 10: Preparando simulación NPT")

    # Paso 11: mdrun NPT
    cmd11 = f"gmx_mpi mdrun -deffnm npt -v -nb gpu -bonded gpu -pme gpu -pin on -update gpu"
    run_command(cmd11, "Paso 11: Ejecutando simulación NPT")

    # Paso 12: grompp para producción MD
    cmd12 = f"gmx_mpi grompp -f ../MDPs/md.mdp -c npt.gro -t npt.cpt -p topol.top -o md.tpr"
    run_command(cmd12, "Paso 12: Preparando simulación de producción MD")

    # Paso 13: mdrun producción MD
    cmd13 = f"gmx_mpi mdrun -deffnm md -v -nb gpu -bonded gpu -pme gpu -pin auto -update gpu"
    run_command(cmd13, "Paso 13: Ejecutando simulación de producción MD")

    print("\nSimulación completada exitosamente. Archivos finales: md.xtc, md.gro, md.log")

if __name__ == "__main__":
    main()

