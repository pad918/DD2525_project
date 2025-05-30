

class Obfuscation:
    
    # Registered obfuscations
    __registered = {}

    def __init__(self):
        pass

    def apply(self, root):
        pass

    def get_by_name(obf_name):
        return Obfuscation.__registered.get(obf_name)
    
    def register(obf_name, class_name):
        Obfuscation.__registered[obf_name] = class_name
        print(f"Registered: {obf_name}")
    
