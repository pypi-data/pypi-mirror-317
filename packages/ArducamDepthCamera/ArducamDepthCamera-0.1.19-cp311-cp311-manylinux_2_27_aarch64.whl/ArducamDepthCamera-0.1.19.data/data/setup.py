import os
import sys
from skbuild import setup
from setuptools import find_packages

# src/debian/changelog
is_win = os.name == "nt"
workdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
change_log = os.path.join(workdir, "src", "debian", "changelog")
data_files = ["ArducamDepthCamera.pyi"]
with open(change_log, "r") as f:
    lines = f.readlines()
    while lines[0].strip() == "":
        lines.pop(0)
    title = lines[0].strip()
    # like "arducam-tof-sdk-dev (0.1.4) UNRELEASED; urgency=medium"
    version = title.split(" ")[1]
    # remove the parentheses
    version = version[1:-1]
    # check if the version is \d+\.\d+\.\d+
    if not version.replace(".", "").isdigit():
        raise ValueError("Invalid version in changelog")
    if version.count(".") != 2:
        raise ValueError("Invalid version in changelog")
if is_win:
    dll_dir = os.path.join(workdir, "tof_sdk", "bin")
    to = os.path.join(workdir, "python", "ArducamDepthCamera")
    # cp $dll_dir/*.dll exclude start with ArducamDepthCamera to $to
    for dll in os.listdir(dll_dir):
        if dll.startswith("ArducamDepthCamera"):
            continue
        with open(os.path.join(dll_dir, dll), "rb") as f:
            with open(os.path.join(to, dll), "wb") as t:
                t.write(f.read())
        data_files += [dll]

WITH_CSI = 'OFF' if is_win else 'ON'
cmake_args = [
    "-DLOG_WARN:BOOL=OFF",
    "-DLOG_INFO:BOOL=OFF",
    "-DWITH_CSI:BOOL=" + WITH_CSI,
    "-DWITH_USB:BOOL=ON",
    "-DONLY_PYTHON:BOOL=ON",
    "-DVERSION_INFO:STRING=" + version,
]
if sys.version_info < (3, 7):
    cmake_args += ["-DWITH_OLD_PYBIND11:BOOL=ON"]

setup(
    name="ArducamDepthCamera",
    version=version,
    description="Driver development kit for arducam tof camera",
    author="Arducam <support@arducam.com>",
    packages=find_packages(),
    cmake_args=cmake_args,
    cmake_source_dir="..",
    cmake_install_dir="ArducamDepthCamera",
    package_data={"ArducamDepthCamera": data_files},
    include_package_data=True,
)
