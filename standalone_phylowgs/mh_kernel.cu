#include <cstdio>
#include <cuda_runtime.h>
#include <cmath>

__device__ double log_binomial_gpu(int a, int d, double mu) {
    mu = (mu <= 0.0) ? 1e-10 : ((mu >= 1.0) ? 1.0 - 1e-10 : mu);
    return a * log(mu) + (d - a) * log(1.0 - mu);
}

__global__ void likelihood_kernel(int* a, int* d, int n_data, int n_tp, double* results) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    if (idx < n_data) {
        double llh = 0.0;
        for (int tp = 0; tp < n_tp; ++tp) {
            llh += log_binomial_gpu(a[idx * n_tp + tp], d[idx * n_tp + tp], 0.5);
        }
        if (idx == 0) printf("Data[0]: a=%d, d=%d, llh=%f\n", a[0], d[0], llh); results[idx] = llh;
    }
}

extern "C" void launch_likelihood_kernel(int* a, int* d, int n_data, int n_tp, double* results) {
    likelihood_kernel<<< (n_data + 255)/256, 256 >>>(a, d, n_data, n_tp, results);
    cudaError_t err = cudaDeviceSynchronize(); if(err != cudaSuccess) printf("CUDA Error: %s\n", cudaGetErrorString(err));
}
