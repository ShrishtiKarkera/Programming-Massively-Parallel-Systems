from mpi4py import MPI

# Initialize
rows = 3
cols = 1

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# value = [4,5,7,5,10] 
# weight = [5,7,9,8,2] 
# W = 29

value = [4, 5, 8]
weight = [3, 4, 7]
W = 7

memory = []
for i in range(rows):
    memory.append([0]*cols)
start_time = MPI.Wtime()
# For each column --> through rows
for i in range(1, rows):
    # send data 
    if rank < size - weight[i-1]:
        comm.send(memory[i-1][0], dest = rank + weight[i-1])
    # receive data
    if rank >= weight[i-1]:
        fetchedValue = comm.recv(source = rank - weight[i-1])
    # compute 
    if weight[i-1] > rank:
	    memory[i][0] = memory[i-1][0]
    else:
	    memory[i][0] = max(value[i-1] + fetchedValue, memory[i-1][0])

    comm.Barrier()
end_time = MPI.Wtime()
if rank == size-1:
    print("Knapsack profit is ", memory[rows-1][0])
if rank == 0:
        print("Average result time: " + str(end_time-start_time))
comm.Barrier()

# Print Memory Array

# printf("Rank ", rank, "Memory Array")
# for i in range(rows):
#     print(memory[i][0])




