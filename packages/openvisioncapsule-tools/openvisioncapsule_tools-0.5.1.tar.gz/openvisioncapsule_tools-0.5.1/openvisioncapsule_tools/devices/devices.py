#
# Copyright (c) 2024 AOTU, Inc.  All rights reserved. Contains Proprietary Information. RESTRICTED COMPUTER SOFTWARE.  LIMITED RIGHTS DATA.
#
from openvisioncapsule_tools.command_utils import command
import logging
import sys
logging.basicConfig(format='[ %(levelname)s ] %(message)s', level=logging.INFO, stream=sys.stdout)

import os
import subprocess
import platform
import re

logging.info(f"import vcap ... ...")
from vcap import __version__ as vcap_version
from vcap.device_mapping import DeviceMapper, get_all_devices
logging.info(f"call vcap get_all_devices ... ...")
all_devices = get_all_devices()

logging.info(f"import openvino ... ...")
import openvino as ov

logging.info(f"import torch ... ...")
import torch

logging.info(f"import tensorflow ... ...")
import tensorflow as tf
logging.info(f"import tensorflow device_lib ... ...")
from tensorflow.python.client import device_lib
logging.info(f"call tensorflow list_local_devices ... ...")
local_device_protos = device_lib.list_local_devices()
logging.info(f"call tensorflow list_logical_devices ... ...")
logical_devices = tf.config.list_logical_devices()

logging.info(f"import pynvml ... ...")
try:
    from pynvml import __version__ as nvml_version
    from pynvml import nvmlInit, nvmlDeviceGetCount, nvmlDeviceGetHandleByIndex, nvmlShutdown, nvmlDeviceGetName
    pynvml_available = True
except Exception as e:
    pynvml_available = False
    logging.info(f"pynvml not available")
import ctypes

logging.info(f"import end.")


def tf_physical_device_details(devices):
    for device in devices:
        try:
            device_details = tf.config.experimental.get_device_details(device)
            logging.info(f'    {device.name}     : {device_details}')
        except Exception as e:
            logging.info(f'    {device.name}     : {e}')


def tf_devices():
    cuda_version = tf.sysconfig.get_build_info().get('cuda_version', None)

    local_devices = [x.name for x in local_device_protos]
    logging.info(f'tensorflow {tf.__version__}')
    logging.info(f'built-in CUDA: {cuda_version}')
    logging.info(f'local devices {local_devices}')
    for device in local_device_protos:
        device_name = device.name.replace("/device:", "")
        logging.info(f"    {device_name}                   : {device.device_type}")

    physical_devices = tf.config.list_physical_devices()
    logging.info(f'    phsical devices         : {physical_devices}')
    # tf_physical_device_details(physical_devices)

    logging.info(f'    logical devices         : {logical_devices}')


def torch_devices():
    if torch.cuda.is_available():
        cuda_version = torch.version.cuda
    else:
        cuda_version = None

    logging.info(f"torch {torch.__version__}")
    logging.info(f"built-in CUDA:{cuda_version}")
    if torch.cuda.is_available():
        for i in range(torch.cuda.device_count()):
            logging.info(f"    GPU:{i}                   : {torch.cuda.get_device_name(i)}")
        logging.info(f"    Current device          : {torch.cuda.current_device()}")
    

def ctypes_get_cuda_driver_version():
    try:
        lib = ctypes.CDLL('libcuda.so')  # For Linux
        # lib = ctypes.windll.LoadLibrary('nvcuda.dll')  # For Windows
    except Exception as e:
        logging.info(f"ctypes CUDA Driver {e}")
        return None

    version = ctypes.c_int()
    lib.cuDriverGetVersion(ctypes.byref(version))
    return version.value


def nv_devices():
    driver_version = ctypes_get_cuda_driver_version()
    if driver_version:
        logging.info(f"ctypes CUDA Driver Version {driver_version // 1000}.{(driver_version % 1000) // 10}")

    if pynvml_available:
        nvmlInit()
        deviceCount = nvmlDeviceGetCount()
        logging.info(f"pynvml {nvml_version}")
        for i in range(deviceCount):
            handle = nvmlDeviceGetHandleByIndex(i)
            logging.info(f"    GPU:{i}                   : {nvmlDeviceGetName(handle)}")
        nvmlShutdown()
    else:
        logging.info(f"pynvml not available")


def get_package_version(package_name):
    try:
        result = subprocess.run(
            ["dpkg-query", "-W", "-f=${Version}", package_name],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        if result.returncode == 0:
            return result.stdout.strip()
        return f"{package_name} not installed"
    except Exception as e:
        return f"Error: {e}"


def openvino_device_name(device):
    core = ov.Core()

    if device.startswith('MULTI:'):
        # Extract individual devices from MULTI
        devices = device[6:].split(',')
        for individual_device in devices:
            openvino_device_name(individual_device)  # Recursive call for each device
        return

    property_key = 'FULL_DEVICE_NAME'
    try:
        property_val = core.get_property(device, property_key)
        logging.info(f'    {device:5}                   : {property_val}')
    except Exception as e:
        logging.info(e)


def ov_devices():
    # Below is same as
    # python3 -c "from openvino.runtime import Core; print(Core().available_devices)"
    available_devices = ov.runtime.Core().available_devices
    logging.info(f'Openvino {ov.__version__}')
    logging.info(f'intel-opencl-icd {get_package_version("intel-opencl-icd")}')
    logging.info(f'Available devices {available_devices}')
    for device in available_devices:
        openvino_device_name(device)


def vcap_devices():
    all_gpus = DeviceMapper.map_to_all_gpus().filter_func(all_devices)
    single_cpu = DeviceMapper.map_to_single_cpu().filter_func(all_devices)
    openvino_devices = DeviceMapper.map_to_openvino_devices().filter_func(all_devices)

    devices_by_priority = os.environ.get("OPENVINO_DEVICE_PRIORITY", "CPU,HDDL").split(",")

    logging.info(f'vcap {vcap_version}')
    logging.info(f'tensorflow & none-CPU Openvino devices {all_devices}')
    logging.info(f'    OPENVINO_DEVICE_PRIORITY {devices_by_priority}')
    logging.info(f'    map_to_all_gpus         : {all_gpus}')
    logging.info(f'    map_to_single_cpu       : {single_cpu}')
    logging.info(f'    map_to_openvino_devices : {openvino_devices}')


def get_ubuntu_version():
    try:
        with open('/etc/os-release') as f:
            lines = f.readlines()
            for line in lines:
                if "VERSION=" in line:
                    version = line.strip()
    except Exception as e:
        return "/etc/os-release: {e}"

    version_number = version.split('=')[1].strip('"')
    return version_number


def parse_intel_generation(model_name):
    gen_match = re.search(r'(\d+)(?:th|st|nd|rd)?\s*Gen', model_name, re.IGNORECASE)
    if gen_match:
        return int(gen_match.group(1))

    model_match = re.search(r'i[357]-(\d{4,5})', model_name)
    if model_match:
        model_number = int(model_match.group(1))
        return int(str(model_number)[0]) if model_number > 13 else model_number

    return None


def get_cpu_model():
    try:
        with open('/proc/cpuinfo', 'r') as f:
            cpu_info = f.read()

        model_name = re.search(r'model name\s*:\s*(.*)', cpu_info).group(1)
        gen_number = parse_intel_generation(model_name)

        if gen_number:
            gen_names = {
                3: "Ivy Bridge", 4: "Haswell", 5: "Broadwell", 6: "Skylake",
                7: "Kaby Lake", 8: "Coffee Lake", 9: "Coffee Lake Refresh",
                10: "Comet Lake or Ice Lake", 11: "Rocket Lake or Tiger Lake",
                12: "Alder Lake", 13: "Raptor Lake"
            }

            gen_name = gen_names.get(gen_number, "Unknown")

            cpu_model = f"{model_name}, {gen_number}th Gen {gen_name}"
        else:
            cpu_model = f"{model_name}"

    except Exception as e:
        cpu_model = {"error": f"{e}"}

    return cpu_model


def get_nv_gpu_model():
    try:
        gpu_model = subprocess.check_output(["nvidia-smi", "--query-gpu=gpu_name", "--format=csv,noheader"]).decode('utf-8').strip()
    except Exception as e:
        gpu_model = 'Not found'
    return gpu_model


def get_platform_info():
    platform_info = {
        "Node": platform.node(),
    }

    platform_info["CPU"] = get_cpu_model()

    if hasattr(platform, "cpu_count"):
        platform_info["CPU Count"] = platform.cpu_count()

    platform_info["NVidia GPU"] = get_nv_gpu_model()

    if hasattr(platform, "python_compiler"):
        platform_info["Python Compiler"] = platform.python_compiler()

    return platform_info


@command("devices")
def devices_main():
    logging.info("")
    platform_info = get_platform_info()
    for key, value in platform_info.items():
        logging.info(f"{key}: {value}")
    logging.info(f"Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    logging.info(f"Ubuntu {get_ubuntu_version()}")
    kernel_version = os.uname().release
    logging.info(f"Kernel {kernel_version}")
    logging.info("")

    nv_devices()
    logging.info("")
    ov_devices()
    logging.info("")
    torch_devices()
    logging.info("")
    tf_devices()
    logging.info("")
    vcap_devices()

    logging.info(f"Done.")

if __name__ == "__main__":
    # devices_main()
    by_name["devices"]()

