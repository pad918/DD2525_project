import glob
import os
import sys
from Obfuscations import Obfuscation

DEBUG = False

def apply_obfuscation(root, obfuscation):
    type = Obfuscation.get_by_name(obfuscation)
    if(type == None):
        raise BaseException(f"Could not find obfuscation type: {obfuscation}")
    
    # Create object of type and apply
    obf = type()
    obf.apply(root)

def get_args(argv):
    if(len(argv)!=3):
        raise "Invalid arguemtns"
    return argv[1], argv[2] 

def get_debug_args(argv):
    return "AdvancedDeadCode", "E:\programmering\python 3\DD2525_project\examples2\Sandoku_copy"

"""
Usage: uv run apply_obfuscations.py <OBFUSCATION NAME> <FOLDER ROOT>

"""
if __name__ == "__main__":
    try:
        if(DEBUG):
            obf_name, path = get_debug_args(sys.argv)
        else:
            obf_name, path = get_args(sys.argv)
    except:
        print("Usage: uv run apply_obfuscations.py <OBFUSCATION NAME> <FOLDER ROOT>")
        sys.exit(1)

    try:
        apply_obfuscation(path, obf_name)
    except BaseException as e:
        raise e

    print(f"Applied the obfuscation {obf_name} sucessfully!")