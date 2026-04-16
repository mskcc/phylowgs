#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <cuda_runtime.h>
#include <vector>
#include <cmath>
#include <algorithm>
#include <iostream>

namespace py = pybind11;

// CUDA Kernel Declaration
extern "C" void launch_likelihood_kernel(int* a, int* d, int n_data, int n_tp, double* results);

struct Node {
    int id;
    std::vector<double> pi;
};

struct Datum {
    int id;
    std::vector<int> a;
    std::vector<int> d;
};

// Host likelihood function (CPU fallback)
double compute_likelihood_cpu(const std::vector<Datum>& data) {
    double total_llh = 0.0;
    for (const auto& datum : data) {
        for (size_t tp = 0; tp < datum.a.size(); ++tp) {
            double mu = 0.5;
            double diff = (mu <= 0.0) ? 1e-10 : ((mu >= 1.0) ? 1.0 - 1e-10 : mu);
            total_llh += datum.a[tp] * std::log(diff) + (datum.d[tp] - datum.a[tp]) * std::log(1.0 - diff);
        }
    }
    return total_llh;
}

// Full likelihood with GPU support
double compute_likelihood(const std::vector<Datum>& data, bool use_gpu) {
    if (!use_gpu) return compute_likelihood_cpu(data);

    int n_data = data.size();
    int n_tp = data[0].a.size();
    
    std::vector<int> h_a, h_d;
    for(const auto& d : data) { h_a.insert(h_a.end(), d.a.begin(), d.a.end()); h_d.insert(h_d.end(), d.d.begin(), d.d.end()); }

    int *d_a, *d_d;
    double *d_results;
    cudaMalloc(&d_a, n_data * n_tp * sizeof(int));
    cudaMalloc(&d_d, n_data * n_tp * sizeof(int));
    cudaMalloc(&d_results, n_data * sizeof(double));

    cudaMemcpy(d_a, h_a.data(), n_data * n_tp * sizeof(int), cudaMemcpyHostToDevice);
    cudaMemcpy(d_d, h_d.data(), n_data * n_tp * sizeof(int), cudaMemcpyHostToDevice);

    std::cout << "DEBUG: Launching kernel with n_data=" << n_data << ", n_tp=" << n_tp << std::endl; launch_likelihood_kernel(d_a, d_d, n_data, n_tp, d_results);

    std::vector<double> h_results(n_data);
    cudaMemcpy(h_results.data(), d_results, n_data * sizeof(double), cudaMemcpyDeviceToHost);

    double total = 0.0;
    for(double r : h_results) total += r;

    cudaFree(d_a); cudaFree(d_d); cudaFree(d_results);
    return total;
}

PYBIND11_MODULE(phylowgs_mh, m) {
    py::class_<Datum>(m, "Datum").def(py::init<>()).def_readwrite("a", &Datum::a).def_readwrite("d", &Datum::d).def_readwrite("id", &Datum::id);
    m.def("compute_likelihood", &compute_likelihood);
}
