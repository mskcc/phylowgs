from setuptools import setup, Extension
import pybind11

ext_modules = [
    Extension(
        "phylowgs_mh",
        ["mh_extension.cpp"],
        extra_objects=["mh_kernel.o"],
        include_dirs=[pybind11.get_include(), "/usr/local/cuda/include"],
        library_dirs=["/usr/lib/aarch64-linux-gnu", "/usr/local/cuda/lib64"],
        libraries=["gsl", "gslcblas", "m", "cudart"],
        extra_compile_args=['-std=c++17'],
    ),
]

setup(name="phylowgs_mh", ext_modules=ext_modules)
