"""Shamboflow : a Tensorflow competitor

A state of the art machine learning library with blazing fast speeds and GPU support
"""

# Startup checks and constants here

IS_CUDA = False
"""Constant to decide whether to use GPU for computations."""
try :
    import cupy as cp
    IS_CUDA = cp.cuda.is_available()

    if IS_CUDA :
        print("CUDA enabled GPU found")
        print("-----------------------")

        _cuda_version = cp.cuda.runtime.runtimeGetVersion()
        _driver_version = cp.cuda.runtime.driverGetVersion()

        print(f"CUDA Version: {_cuda_version // 1000}.{(_cuda_version % 1000) // 10}")
        print(f"CUDA Driver Version: {_driver_version // 1000}.{(_driver_version % 1000) // 10}")

        _props = cp.cuda.runtime.getDeviceProperties(0)
        print(f"Name: {_props['name'].decode()}")
        print(f"Compute Capability: {_props['major']}.{_props['minor']}")
        print(f"Total Memory: {_props['totalGlobalMem'] / 1e9:.2f} GB")
        print("\n-----------------------------------------------\n")
except :
    pass

# Add Colorama fixes to terminal
from colorama import just_fix_windows_console
just_fix_windows_console()

from shamboflow import models
from shamboflow import layers
from shamboflow import callbacks