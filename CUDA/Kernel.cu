__global__ Kernel_Sample(size_t numberOfThreads)
{
	size_t threadid = blockIdx.x * blockDim.x + threadIdx.x;
	if (threadid > numberOfInputPoints - 1) return;  
}

void Calling(size_t numberOfThreads)
{
    	int mingridsize;
    	int threadblocksize;
    	checkCudaErrors(cudaOccupancyMaxPotentialBlockSize(&mingridsize, &threadblocksize, Kernel_Sample, 0, 0));
    	auto gridsize = (numberOfThreads - 1) / threadblocksize;
    
	Kernel_Sample << <gridsize, threadblocksize, 0, stream >> > ();
}
