# Used to bulid a project exe using a set of obfuscation techniques
from enum import Enum
from typing import List
import os
import shutil
import subprocess
from Obfuscations.Obfuscation import Obfuscation

def create_build_files(project_root):
    # copy all files into from root to /.generated
    generated_root = f"{project_root}/.generated"
    if os.path.exists(generated_root):
        shutil.rmtree(generated_root)
    os.makedirs(generated_root)

    for filename in os.listdir(project_root):
        if(generated_root in filename):
            continue

        # Skip venv and build folders
        if ("venv" in filename or "__pycache__" in filename):
            continue

        source_path = os.path.join(project_root, filename)
        destination_path = os.path.join(generated_root, filename)
        if os.path.isfile(source_path) and (filename.endswith('.py') or filename.endswith(".ps1")):
            print(f"Including file: {filename}")
            try:
                shutil.copy(source_path, destination_path)
            except Exception as e:
                raise BaseException(f"Could not move file: {filename}")

def apply_obfuscation(root, obfuscation):
    type = Obfuscation.get_by_name(obfuscation)
    if(type == None):
        raise BaseException(f"Could not find obfuscation type: {obfuscation}")
    
    # Create object of type and apply
    obf = type()
    obf.apply(root)


def build(project_path):
    if(not os.path.exists(f"{project_path}\\.generated\\build.ps1")):
        return -1
    os.chdir(f"{project_path}\\.generated")
    subprocess.Popen("powershell .\\build.ps1")

def build_project(project_path:str, obfuscations: List[str]) -> None:
    # Make a copy of the project files in .generated
    create_build_files(project_path)
    
    # Apply all the obfuscations in order
    for obf in obfuscations:
        apply_obfuscation(f"{project_path}\\.generated", obf)

    # Build the project
    build(project_path)

    # Upload the exe to VirusTotal
        # CALL YOUR CODE HERE


if __name__ == "__main__":
    build_project("E:\\programmering\\python 3\\test", ["Encode"])