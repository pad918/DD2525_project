from enum import Enum
from typing import List
import os
import shutil
import subprocess
import glob
from Virustotal.virustotal_scripts import upload_file
from Obfuscations.Obfuscation import Obfuscation
import json
import tqdm

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
    # Save old dir
    prev_dir = os.getcwd()

    abs_path = os.path.abspath(project_path)
    build_script_path = os.path.join(abs_path, ".generated", "build.ps1")
    if(not os.path.exists(build_script_path)):
        return -1
    os.chdir(f"{project_path}\\.generated")
    process = subprocess.Popen("powershell .\\build.ps1")
    process.wait()
    # Return to original dir
    os.chdir(prev_dir)

def test_obfuscations(project_path:str, obfuscations: List[str]) -> None:
    # Make a copy of the project files in .generated
    create_build_files(project_path)
    
    # Apply all the obfuscations in order
    for obf in obfuscations:
        apply_obfuscation(f"{project_path}\\.generated", obf)

    # Build the project
    build(project_path)
    exe_search_pattern = os.path.join(os.path.abspath(project_path), ".generated", "*.exe")
    files = glob.glob(exe_search_pattern)
    if (len(files)==1):
        exe_path = files[0]
    else:
        raise BaseException("Build failed, no exe found")

    print(f"Found the new exe at: {exe_path}")
    
    # Upload the exe to VirusTotal
    upload_file(exe_path, obfuscations)


if __name__ == "__main__":
    with open("settings.json", "rb") as f:
        settings = json.load(f)
    for test in tqdm.tqdm(settings):
        try:
            project_path = test["project_folder"]
            obfuscations = test["obfuscations"]
            if(project_path==None or obfuscations==None):
                print(f"Invalid parameters for test: {test}")
                continue
            test_obfuscations(project_path, obfuscations)
        except BaseException as e:
            print(f"Failed to test: {test}")
            raise e