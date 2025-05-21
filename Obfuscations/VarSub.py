from Obfuscations.Obfuscation import Obfuscation


class VarSub(Obfuscation):
    
    def __init__(self):
        pass

    def apply(self, root):
        print(f"Applying varsub obfuscation to: <{root}>")