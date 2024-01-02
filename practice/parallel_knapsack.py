from mpi4py import MPI
import numpy as np

# rows = 5
# cols = 0
# value = [60, 100, 120]
# weight = [1, 2, 3]
# W = 6

rows = 5
cols = 0
value = [4, 5, 8]
weight = [3, 4, 7]
W = 7

min_col_per_node =  1

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# Determining number of columns per processor

if min_col_per_node * size - 1 >= W:
    cols = min_col_per_node
else:
    result = W + 1
    while result % size != 0:
        result += 1
    cols = result // size
    
memory = []
for i in range(rows):
    memory.append([0]*cols)

# ===========================================INITIALISATION===========================================    

# Initialize 0th Row
for j in range(cols):
    memory[0][j] = j + (cols * rank)

# Initialize 1st Row
# if rank == 0:
#     for i in range(1,rows):
#         if j == 0:
#             memory[1][j] = 1
#         else:
#             memory[1][j] = 0
# else:
#     for j in range(cols):
#         memory[1][j] = 0
    
# # Initialize Remaining Rows
# for i in range(2, rows):
#     for j in range(cols):
#         memory[i][j] = -1

# print("my rank", rank, "and mem is", memory)

# =============================================EXECUTION=============================================    
# Row Wise Iteration
for i in range(2, rows):
    # send phase
    destination_Rank1 = -1
    destination_Rank2 = -1        
    sendBufferSize1 = 0
    sendBufferSize2 = 0

    for j in range(cols):
        if memory[0][j] < (size * cols) - weight[i-2]:
            destination = memory[0][j] + weight[i-2]
            factor = cols
            destination_Rank = destination // factor
            if destination_Rank1 == -1 or destination_Rank1 == destination_Rank:
                destination_Rank1 = destination_Rank
                sendBufferSize1 += 1
            else:
                destination_Rank2 = destination_Rank
                sendBufferSize2 += 1
    
    if rank == 0:
        print("printing in send", sendBufferSize1, sendBufferSize2)

    # firstSendBuffer = np.empty(sendBufferSize1)
    firstSendBuffer = np.empty(0, dtype = 'int')
    # secondSendBuffer = np.empty(sendBufferSize2) 
    secondSendBuffer = np.empty(0, dtype = 'int')
        
    sizeFlag = 0
    bufferFlag = 1
    for i in range(cols):
        if bufferFlag == 1:
            if sizeFlag < sendBufferSize1:
                # firstSendBuffer[sizeFlag] = memory[i-1][j]
                firstSendBuffer = np.append(firstSendBuffer, memory[i-1][j])
                sizeFlag += 1
                if sizeFlag == sendBufferSize1:
                    sizeFlag = 0
                    bufferFlag = 2
        elif bufferFlag == 2:
            if sizeFlag < sendBufferSize2:
                # secondSendBuffer[sizeFlag] = memory[i-1][j]
                secondSendBuffer = np.append(secondSendBuffer, memory[i-1][j])
                sizeFlag += 1
        
    if destination_Rank1 != -1:
        comm.Send(firstSendBuffer, dest = destination_Rank1)
    
        
    if destination_Rank2 != -1:
        comm.Send(secondSendBuffer, dest = destination_Rank2)
        
# Receive Phase ..........................................................................
    source_Rank1 = -1
    source_Rank2 = -1
    recieveBufferSize1 = 0
    recieveBufferSize2 = 0
    
    for i in range(cols-1, -1, -1):
        if memory[0][j] == weight[i-2] or memory[0][j] > weight[i-2]:
            source = memory[0][j] - weight[i-2]
            factor = cols
            source_Rank = source // factor
            if source_Rank == -1 or source_Rank1 == source_Rank:
                source_Rank1 = source_Rank
                recieveBufferSize1 += 1
            else:
                source_Rank2 = source_Rank
                recieveBufferSize2 += 1
    
    firstRecieveBuffer = np.empty(recieveBufferSize1, dtype = 'int')
    secondRecieveBuffer = np.empty(recieveBufferSize2, dtype = 'int')


    
    if source_Rank1 != -1:
        firstRecieveBuffer = comm.Recv(firstRecieveBuffer, source = source_Rank1)    
    
    if source_Rank2 != -1:
        secondRecieveBuffer = comm.Recv(secondRecieveBuffer, source = source_Rank2)

# Compute Phase ...........................................................................
    for j in range(cols):
        memory[i][j] = memory[i-1][j]
    
    firstBufferPointer = -1
    secondBufferPointer = -1
    if recieveBufferSize1 > 0:
        firstBufferPointer = recieveBufferSize1 - 1
    
    if recieveBufferSize2 > 0:
        secondBufferPointer = recieveBufferSize2 - 1

    if rank == 0:
        print("Reached here", recieveBufferSize1, recieveBufferSize2, firstBufferPointer, secondBufferPointer)
    
    for j in range(cols-1, -1, -1):
        if weight[i-2] <= memory[0][j]:
            if firstBufferPointer > -1:
                print(memory)
                memory[i][j] = max(value[i-2] + firstRecieveBuffer[firstBufferPointer], memory[i][j])
                firstBufferPointer -= 1

            elif secondBufferPointer > -1:
                print(memory)
                memory[i][j] = max(value[i-2] + secondRecieveBuffer[secondBufferPointer], memory[i][j])
                secondBufferPointer -= 1
# print(memory)
# The main for loop ends here
    
# ===============================================PRINT===============================================
    
answer_Rank = W // cols
if rank == answer_Rank:
    for j in range(cols):
        # Print Final Answer
        if memory[0][j] == W:
            print("Input", weight, value, row-2)
            print("Target Weight:", W)
            print("Number of rows in each processor:", rows)
            print("Number of processors:", size)
            print("Number of columns used per processor:", cols)
            print("2D Matrix Size:", rows, size, cols, rows, size * cols)
            print("Knapsack Count:", memory[rows-1][j])

# Print Memory Array
print("Rank", rank, "Memory Array")
for i in range(rows):
    for j in range(cols):
        print(memory[i][j])