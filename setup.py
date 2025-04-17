import os
import glob
import sys
from setuptools import setup, find_packages
import torch
from torch.utils.cpp_extension import BuildExtension, CUDAExtension, CppExtension

def get_extensions():
    sources = glob.glob(os.path.join("rspmm", "source", "*.cpp"))

    use_cuda = os.getenv("RSPMM_WITH_CUDA", "0") == "1"
    if use_cuda:
        sources += glob.glob(os.path.join("rspmm", "source", "*.cu"))

    extra_compile_args = {"cxx": ["-Ofast"]}
    if use_cuda:
        extra_compile_args["nvcc"] = ["-O3"]
        extra_compile_args["cxx"].append("-DCUDA_OP")

    if not torch.backends.openmp.is_available() or sys.platform.startswith("darwin"):
        extra_compile_args["cxx"].append("-DAT_PARALLEL_NATIVE")
    else:
        extra_compile_args["cxx"].extend(["-fopenmp", "-DAT_PARALLEL_OPENMP"])

    Extension = CUDAExtension if use_cuda else CppExtension

    return [
        Extension(
            name="rspmm_ext",
            sources=sources,
            include_dirs=[os.path.abspath(os.path.join("rspmm", "source"))],
            extra_compile_args=extra_compile_args,
        )
    ]

setup(
    name="rspmm",
    version="0.2.0",
    packages=find_packages(),
    install_requires=["torch"],
    ext_modules=get_extensions(),
    cmdclass={"build_ext": BuildExtension},
    zip_safe=False,
)
