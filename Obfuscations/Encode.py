from Obfuscations.Obfuscation import Obfuscation
import base64
import glob
import os
import shutil
import subprocess
import sys

class Encode(Obfuscation):
    
    
    def apply(self, root):

        project_root = root
        files = glob.glob(f"{project_root}/**py", recursive=True)
        for file in files:
            self._encode_single(file)

    # Replace single program with python encoded version
    def _encode_single(self, file):
        if "__pycache__" in file or "venv" in file:
                return

        # Encode file contents
        with open(file, "rb") as f:
            file_bytes = f.read()

        # B64 encode to string
        encoded_file = base64.b64encode(file_bytes).decode("utf-8")

        # Write to file with exec function
        with open(file, "wt") as f:
            file_text = f"""
import base64
exec(base64.b64decode("{encoded_file}").decode("utf-8"))"""
            f.write(file_text)