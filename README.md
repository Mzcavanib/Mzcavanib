Hi, I’m @Mzcavanib

How to reach me maurizio.cavani.b@upch.pe

I develop programs designed to automate molecular dynamics with GROMACS and the analysis of trajectory results. 

These Python programs are designed on matplotlib to analyze molecular dynamics trajectories generated with GROMACS. They cover four key metrics: RMSD, RMSF, SASA, and radius of gyration. Each script produces color-coded plots and supports the simultaneous analysis of up to 10 datasets. If more datasets are needed, additional color codes can be added manually.

All scripts are executed using Python 3 from the Linux terminal with a consistent syntax. For example:

```bash
./rmsd.py rmsd1.xvg rmsd2.xvg ...
./rmsf.py rmsf1.xvg rmsf2.xvg ...
./sasa.py sasa1.xvg sasa2.xvg ...
./gyrate.py gyrate1.xvg gyrate2.xvg ...
```

Each analysis script follows the same execution pattern.

The `md.py` script automates the molecular dynamics setup in two main stages: selection of force field and water model, followed by ion addition via `gmx genion`, including solvent specification. The simulation box is cubic, with a 2 Å buffer between the molecule and the nearest box face.

This script is configured for use with the `gmx_mpi` binary but can be easily adapted to run with `gmx`. Execution is straightforward:

```bash
./md.py proteinX.pdb
```

where `proteinX.pdb` is any curated structure obtained from the Protein Data Bank.

The script also requires a set of .mdp parameter files to be present in a specific location. These files—ions.mdp, minim.mdp, nvt.mdp, npt.mdp, and md.mdp—must be stored in a folder named MDPs, located one directory level above the folder where md.py is executed.

For example:
```bash
Código
project-root/
├── MDPs/
│   ├── ions.mdp
│   ├── minim.mdp
│   ├── nvt.mdp
│   ├── npt.mdp
│   └── md.mdp
└── simulations/
    └── md.py
```
These .mdp files are authored specifically for the simulations of the Gamma variant and wild-type systems over 100 ns, and are located in the Gamma-variant-and-WT-100ns-MD-simulations repository.

The `get_to_center.py` script provides a robust, automated wrapper around a three-step GROMACS preprocessing workflow designed to prepare molecular dynamics (MD) trajectories for downstream structural analysis. It is particularly useful for researchers working with periodic boundary conditions (PBC) and trajectory alignment, ensuring that the molecular system is physically coherent and analytically tractable across frames. The script is written for use in high-performance computing environments where GROMACS is compiled with MPI support (gmx_mpi), and it disables graphical output (GMX_NO_X11=1) to ensure compatibility with headless systems.
The pipeline begins by validating the presence of two essential input files in the working directory: `md.xtc` (the trajectory file) and `md.tpr` (the portable binary run input file containing topology and simulation parameters). If either file is missing, the script halts with a clear error message, preserving reproducibility and preventing silent failures.

Once validated, the script executes three sequential GROMACS trjconv commands:

Whole Molecule Reconstruction (-pbc whole) This step removes artifacts introduced by periodic boundary conditions by reconstructing molecules that may have been split across box boundaries. It ensures that each molecule is represented as a contiguous entity throughout the trajectory. The output is saved as `whole.xtc`.

Molecule Centering and Compacting (-pbc mol -ur compact -trans) The second step centers the molecule in the simulation box and applies a compact representation of the unit cell. A translation vector (-3 0 0) is applied to shift the system, which can be useful for visualization or alignment purposes. The result is stored in `mol.xtc`.

Trajectory Fitting (-fit rot+trans) Finally, the script performs rotational and translational fitting of the trajectory to a reference structure. This alignment is crucial for RMSD, RMSF, and other structural analyses, as it removes global motions and isolates internal conformational changes. The fitted structure is exported as `md.xtc`, a format compatible with most visualization and analysis tools.

Output Files

- `whole.xtc`: Trajectory with molecules reconstructed across PBC boundaries.

- `mol.xtc`: Centered and compacted trajectory with applied translation.

- `md.xtc`: Final fitted trajectory ready for structural and energetic analysis.

Execution Notes

All the programs use gmx_mpi but can be easily adapted to run with `gmx`.
