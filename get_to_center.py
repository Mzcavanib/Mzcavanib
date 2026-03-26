import subprocess
import os
os.environ["GMX_NO_X11"] = "1"
import sys

def run_command(command, description):
    print(f"\n{description}")
    print(f"Running: {command}")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print("Completed.")
        if result.stdout:
            print("STDOUT:", result.stdout.strip())
        if result.stderr:
            print("STDERR:", result.stderr.strip())
    except subprocess.CalledProcessError as e:
        print("Error while executing the command.")
        print("STDOUT:", e.stdout.strip() if e.stdout else "No output.")
        print("STDERR:", e.stderr.strip() if e.stderr else "No errors.")
        sys.exit(1)

def run_gromacs_pipeline():
    # Base files
    input_xtc = "md.xtc"
    tpr_file = "md.tpr"

    # Verify that the files exist
    for file in [input_xtc, tpr_file]:
        if not os.path.isfile(file):
            print(f"Error: Required file '{file}' not found in the current directory.")
            sys.exit(1)

    # Step 1: reconstruct complete molecule
    cmd1 = f"echo 1 | gmx_mpi trjconv -f {input_xtc} -s {tpr_file} -pbc whole -o whole.xtc"
    run_command(cmd1, "Step 1: reconstructing complete molecule with -pbc whole")

    # Step 2: request translation values
    try:
        x_trans = float(input("Enter translation value in x (e.g. -3.0): "))
        y_trans = float(input("Enter translation value in y (e.g. 0.0): "))
        z_trans = float(input("Enter translation value in z (e.g. 0.0): "))
    except ValueError:
        print("Error: Values must be real numbers.")
        sys.exit(1)

    # Step 2: compact and translate molecule with entered values
    cmd2 = (
        f"echo 1 | gmx_mpi trjconv -f whole.xtc -s {tpr_file} "
        f"-pbc mol -ur compact -trans {x_trans} {y_trans} {z_trans} -o mol.xtc"
    )
    run_command(cmd2, f"Step 2: compacting and translating molecule with -trans {x_trans} {y_trans} {z_trans}")

    # Step 3: fit trajectory
    cmd3 = f"echo 3 1 | gmx_mpi trjconv -f mol.xtc -s {tpr_file} -fit rot+trans -o final.xtc"
    run_command(cmd3, "Step 3: fitting trajectory with -fit rot+trans")

    print("\nProcess successfully finished. You can continue with the analysis of 'final.xtc'.")

if __name__ == "__main__":
    run_gromacs_pipeline()
