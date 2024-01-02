# **Fall 2023 - CSE 708 Center for Computational Research Lab**

**Programming Knapsack algorithm using MPI in Python**

Code can run on any number of processors.
It supports multiple columns per processor.
The number of columns per processor will be dynamically adjusted by the code as per need.
Project Description:
For my semester-long parallel computing project, I implemented a solution to the knapsack problem using MPI in Python. My goal was to determine maximum profit/value given the items cost and value array with a W (knapsack weight). My approach divided the dynamic programming table into column groups, with each processor responsible for computations on one group. Through message passing, the processors shared intermediate results to collectively calculate final profit. By testing on large inputs and varying processor counts, I quantified speedup versus sequential execution and studied scaling behavior. This project allowed me to apply course concepts like parallel decomposition, load balancing, and communication overhead. Over the course of the project, I gained hands-on experience with parallel algorithm design, MPI programming, and performance analysis. This demonstrated my skills in practical parallel computing.

#
**Key Features**

Implemented parallel algorithm in Python to solve the knapsack algorithm, leveraging parallel processing with distributed memory for performance gains over sequential code execution.
Incorporated a feature to dynamically divide workload between MPI processes by adjusting column-wise decomposition of dynamic programming table at runtime to ensure optimal load balancing.
Quantified speedup versus sequential execution and studied scaling behavior by testing for different large inputs.
Streamlined testing by auto Slurm script submission for each test case via Shell script, reducing manual efforts.

# 
**To use the code as is (assuming access to parallel machines or a distributed system):**
1. Install  MPI
```python
pip install mpi4py
```
2. Run the slurm script
```bash
sbatch slurm.sh
```
#
**To use the code with custom input (assuming access to parallel machines or a distributed system):**
1. Clone the repo
```bash
git clone https://github.com/ShrishtiKarkera/Programming-Massively-Parallel-Systems.git
```
2. Install MPI in your bash
```python
pip install mpi4py
```
3. Provide your custom input of choice in the vanilla_knapsack.py or parallel_knapsack.py
4. Edit the slurm script by changing the name of the file, number of nodes/processors and the number of machines
5. Run the slurm script
```bash
sbatch slurm.sh
```
