from mpi4py import MPI

rows = 5
cols = 1

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

input = [3,3,3,3]
sum = 6
memory = []
for i in range(rows):
    memory.append([0]*cols)

# Initialize
if rank == 0:
    for i in range(rows):
        memory[i][0] = 1
    
# Row Wise Iteration
for i in range(1, rows):
    # send phase
    if rank < size - input[i-1]:
        comm.send(memory[i-1][0], dest = rank + input[i-1])
    # receive phase
    if rank >= input[i-1]:
        fetchedValue = comm.recv(source = rank - input[i-1])
    # compute phase
    if input[i-1] > rank:
	    memory[i][0] = memory[i-1][0]
    else:
	    memory[i][0] = memory[i-1][0] + fetchedValue

    comm.Barrier()

#  Print Final Answer

if rank == size-1:
    print("Subset Sum Count ", memory[rows-1][0])

comm.Barrier()

# Print Memory Array

print("Rank ", rank, "Memory Array")
for i in range(rows):
    print(memory[i][0])