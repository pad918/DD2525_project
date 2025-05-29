# Obfuscate constants!
from Obfuscations.Obfuscation import Obfuscation
import glob
import libcst as cst
import libcst.metadata as metadata
import os

def get_ast(file_path):
    with open(file_path, "rt", encoding="utf-8") as f:
        python = f.read()
        return cst.parse_module(python)

class ConstantObfuscationTransformer(cst.CSTTransformer):
    METADATA_DEPENDENCIES = [metadata.ScopeProvider]

    def __init__(self):
        super().__init__()

    # Template för att obfuscata strängar (andra konstanter borde kunna göra på samma sätt typ)
    def leave_SimpleString(self, original_node, updated_node):
        if("\\" in updated_node.value):
            return updated_node
        quote_type = updated_node.quote
        new_expr = cst.parse_expression(f"{quote_type}{updated_node.raw_value[::-1]}{quote_type}[::-1]")
        return new_expr
    
    # Simple integer obfuscation
    def leave_Integer(self, original_node, updated_node):
        # Special case base16
        if(updated_node.value.lower().startswith("0x")):
            new_expr = cst.parse_expression(f"int({int(updated_node.value, base=16)-100}+100)")
        # Special case for octal (does it exist in python???)
        elif(updated_node.value.lower().startswith("0")):
            new_expr = cst.parse_expression(f"int({int(updated_node.value, base=8)-100}+100)")
        # Normal case
        else:
            new_expr = cst.parse_expression(f"int({int(updated_node.value)-100}+100)")
        return new_expr

class ConstSub(Obfuscation):

    def apply(self, root):
        project_root = root
        files = glob.glob(os.path.join(root, "**", "*.py"), recursive=True)
        for file in files:
            self._apply_single(file)

    def _apply_single(self, py_file_path):
        tree = get_ast(py_file_path)
        wrapper = cst.metadata.MetadataWrapper(tree)

        transformer = ConstantObfuscationTransformer()

        modified_tree = wrapper.visit(transformer)
        with open(py_file_path, "wt", encoding="utf-8") as f:
            f.write(modified_tree.code) 
