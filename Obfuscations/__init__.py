from Obfuscations.Obfuscation import Obfuscation
from Obfuscations.VarSub import VarSub

# Register all existing obfuscations here
import sys, inspect
for name, obj in inspect.getmembers(sys.modules[__name__]):
    if inspect.isclass(obj):
        Obfuscation.register(name, obj)
        print(f"Added: {obj}")