#!/bin/bash

#SBATCH --nodes=60
#SBATCH --ntasks-per-node=5
#SBATCH --constraint=IB|OPA
#SBATCH --time=00:10:00
#SBATCH --partition=general-compute
#SBATCH --qos=general-compute
#SBATCH --job-name="knapsack-60node-5core"
#SBATCH --output=final-output.txt
#SBATCH --exclusive

module load intel
module load python

export I_MPI_PMI_LIBRARY=/opt/software/slurm/lib64/libpmi.so
srun pip install numpy mpi4py > /dev/null 2>&1

srun -n 300 python parallel_knapsack.py
