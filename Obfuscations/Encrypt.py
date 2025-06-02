from Obfuscations.Obfuscation import Obfuscation
import glob
import os
from cryptography.fernet import Fernet


class Encrypt(Obfuscation):

    def apply(self, root):

        files = glob.glob(os.path.join(root, "**", "*.py"), recursive=True)
        for file in files:
            self._encode_single(file)

    # Replace single program with python encrypted version
    def _encode_single(self, file):
        if "__pycache__" in file or "venv" in file:
            return

        # Encode file contents
        with open(file, "rb") as f:
            file_bytes = f.read()

        # Get key & init fernet
        key = Fernet.generate_key()
        fernet = Fernet(key)

        # Encrypt
        encrypted_file = fernet.encrypt(file_bytes).decode("utf-8")

        # Write to file with exec function
        with open(file, "wt") as f:
            file_text = f"""
from cryptography.fernet import Fernet
fernet = Fernet({key})
exec(fernet.decrypt("{encrypted_file}").decode("utf-8"))"""
            f.write(file_text)
