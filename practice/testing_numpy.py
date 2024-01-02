from mpi4py import MPI
import numpy as np

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

buffer = np.empty(3, dtype='int')

buffer[0] = 1
buffer[1] = 2

# buffer = np.append(buffer, values)

if rank == 0:
    comm.Send(buffer, dest=1)
elif rank == 1:
    comm.Recv(buffer, source=0)

print(f"Process {rank}: {buffer}")