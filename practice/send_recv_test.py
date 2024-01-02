from mpi4py import MPI
import numpy as np

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

# Create the array on rank 0
if rank == 0:
    array = np.empty(0, dtype = 'int')
    array = np.append(array, 6)
else:
    array = np.empty(1, dtype = 'int')

# Send and receive the array
if rank == 0:
    comm.Send(array, dest=1)
elif rank == 1:
    comm.Recv(array, source=0)

# Print the received array on each rank
print(f"Rank {rank}: {array}")