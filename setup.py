import sys
import os
from cx_Freeze import setup, Executable
files = ["logo.ico", "configs/"]

target = Executable(
    script="main.py",
    base="Win32GUI",
    icon="logo.ico"
)

setup(
    name="UX-Vision",
    version="1.0.0",
    description="PFE Elbouchouki",
    author="Elbouchouki Ahmed - Hamza Oumadane",
    options={'build.exe': {'include_files': files}},
    executables=[target]
)
