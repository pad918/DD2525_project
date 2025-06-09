from typing import List
import os
import shutil
import subprocess
from Virustotal.virustotal_scripts import upload_file, update_database_uploads
from Obfuscations.Obfuscation import Obfuscation
import json
import tqdm
import time
import shutil
import libcst
import stat
import zipfile

def create_build_files(project_root):
    project_root = os.path.abspath(project_root)

    # copy all files into from root to /.generated
    generated_root = f"{project_root}/.generated"
    if os.path.exists(generated_root):
        shutil.rmtree(generated_root, onerror=rm_error)
    shutil.copytree(project_root, generated_root)

def rm_error(func, path, exc_info):
    # Is the error an access error?
    if not os.access(path, os.W_OK):
        os.chmod(path, stat.S_IWUSR)
        func(path)
    else:
        raise


def apply_obfuscation(root, obfuscation):
    type = Obfuscation.get_by_name(obfuscation)
    if(type == None):
        raise BaseException(f"Could not find obfuscation type: {obfuscation}")
    
    # Create object of type and apply
    obf = type()
    obf.apply(root)

def zip_project(project_path:str, zip_destination:str):
    if os.path.exists(zip_destination):
        os.remove(zip_destination)
    def zipdir(path, ziph):
        for root, dirs, files in os.walk(project_path):
            for file in [f for f in files if f.endswith(".py")]:
                ziph.write(os.path.join(root, file), 
                           os.path.relpath(os.path.join(root, file), 
                                           os.path.join(path, '..')))

    with zipfile.ZipFile(zip_destination, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipdir(project_path, zipf)


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
    
    obuscated_project_root = f"{project_path}\\.generated"
    
    # Apply all the obfuscations in order
    for obf in obfuscations:
        apply_obfuscation(obuscated_project_root, obf)

    # Get project name: 
    proj_zip_name = os.path.split(project_path)[-1] + ".zip"

    # Zip the poject
    zip_project(obuscated_project_root, proj_zip_name)
    
    # Upload the exe to VirusTotal
    upload_file(proj_zip_name, obfuscations)


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
            # Fetch data from uploaded files
            print("Sleeping for 15s, and fetching data")
            time.sleep(15)

        except libcst._exceptions.ParserSyntaxError as e:
            print(f"FAILED TO TEST PROJECT: {project_path}")
            print(f"\tERROR! PARSE ERROR, incorrect syntax, maybe python 2?")
        except BaseException as e:
            print(f"Failed to test: {test}")
            raise e
    time.sleep(120)
    update_database_uploads()
    print("DONE!")