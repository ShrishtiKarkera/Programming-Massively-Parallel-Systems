from mpi4py import MPI

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

if rank == 0:
   data = [(x+1)**x for x in range(size)]
   print('we will be scattering:', data)
else:
   data = None
   
data = comm.scatter(data, root=0)
data += 1
print('rank', rank, 'has data:', data)

# Only the scatterer can gather data, if we put root=1, we get the gathered data as None
newData = comm.gather(data, root=0)

if rank == 0:
   print('master:', newData)