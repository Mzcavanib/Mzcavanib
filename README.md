- 👋 Hi, I’m @Mzcavanib
- 👀 I’m interested in molecular dynamics
- 📫 How to reach me maurizio.cavani.b@upch.pe

I develop programs designed to automate molecular dynamics with GROMACS and the analysis of trajectory results. 

These Python programs are designed to analyze molecular dynamics trajectories generated with GROMACS. They cover four key metrics: RMSD, RMSF, SASA, and radius of gyration. Each script produces color-coded plots and supports the simultaneous analysis of up to 10 datasets. If more datasets are needed, additional color codes can be added manually.

All scripts are executed using Python 3 from the Linux terminal with a consistent syntax. For example:

```bash
./rmsd.py rmsd1.xvg rmsd2.xvg ...
```

Each analysis script follows the same execution pattern.

The `md.py` script automates the molecular dynamics setup in two main stages: selection of force field and water model, followed by ion addition via `gmx genion`, including solvent specification. The simulation box is cubic, with a 2 Å buffer between the molecule and the nearest box face.

This script is configured for use with the `gmx_mpi` binary but can be easily adapted to run with `gmx`. Execution is straightforward:

```bash
./md.py proteinX.pdb
```

where `proteinX.pdb` is any curated structure obtained from the Protein Data Bank.

The `get_to_center.py` script performs three steps to remove periodic boundary conditions and center the molecule within the simulation box, preventing artificial jumps in RMSD analysis. To use it, simply copy the script into the simulation directory, ensuring the trajectory and topology files are named `md.xtc` and `md.tpr`, respectively. The output will be a new trajectory file named `final.xtc`.

The default centering coordinates are set to `-3 0 0`, but these can be modified as needed depending on the molecule’s position within the box.
