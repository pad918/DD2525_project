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
        self.is_in_concatenated_string = False

    # Template för att obfuscata strängar (andra konstanter borde kunna göra på samma sätt typ)
    def leave_SimpleString(self, original_node, updated_node):
        if(self.is_in_concatenated_string):
            return original_node
        if("\\" in updated_node.value):
            return updated_node
        if(original_node in self.concatenated_strings):
            print("FOUND IT")
            return original_node

        quote_type = updated_node.quote
        new_str = f"{quote_type}{updated_node.raw_value[::-1]}{quote_type}[::-1]"
        new_expr = cst.parse_expression(new_str)
        print(f"{updated_node.value} --> {new_str}")
        return new_expr
    
    # Concatenated strings
    def visit_ConcatenatedString(self, node):
        self.is_in_concatenated_string = True
        return super().visit_ConcatenatedString(node)

    def leave_ConcatenatedString(self, original_node, updated_node):
        self.is_in_concatenated_string = False
        return updated_node 
    
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
        try:
            print(f"LOOKING AT FILE: {py_file_path}")
            tree = get_ast(py_file_path)
            wrapper = cst.metadata.MetadataWrapper(tree)

            transformer = ConstantObfuscationTransformer()

            modified_tree = wrapper.visit(transformer)
            with open(py_file_path, "wt", encoding="utf-8") as f:
                f.write(modified_tree.code)
        except BaseException as e:
            print(f"Could not apply ConstSub to file: {py_file_path}: {e}")
            raise e
