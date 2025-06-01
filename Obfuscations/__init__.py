from Obfuscations.Obfuscation import Obfuscation
from Obfuscations.VarSub import VarSub
from Obfuscations.Encode import Encode
from Obfuscations.ConstSub import ConstSub
from Obfuscations.DeadCode import DeadCode
from Obfuscations.Encrypt import Encrypt
from Obfuscations.AdvancedDeadCode import AdvancedDeadCode

# Register all existing obfuscations here
import sys, inspect
for name, obj in inspect.getmembers(sys.modules[__name__]):
    if inspect.isclass(obj):
        Obfuscation.register(name, obj)
        print(f"Added: {obj}")