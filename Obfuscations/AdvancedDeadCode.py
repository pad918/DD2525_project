import libcst as cst
import libcst.metadata as metadata
from Obfuscations.Obfuscation import Obfuscation
import glob
import os

# Repeat = # times code added per line
# Works by inserting statements for each lines of code in original file
def get_ast(file_path):
    with open(file_path, "rt", encoding="utf-8") as f:
        python_code = f.read()
        return cst.parse_module(python_code)


class DeadCodeInsertionTransformer(cst.CSTTransformer):

    def __init__(self):
        super().__init__()

    """
    Replace each line with a condition that is always true like
    
        Input: 
            x = cool_func()

        Output:
            if(is_prime(23)):
                x = cool_func()

    """
    def leave_SimpleStatementLine(self, original_node, updated_node):

        body = cst.IndentedBlock(
            body = [updated_node]
        )
        
        if_statement = cst.If(
            test = cst.Name("True"),
            body=body,
            leading_lines=[]
        )
        # Add node to the if block 
        print(if_statement)
        print("----------")
        print(updated_node)
        return if_statement

class AdvancedDeadCode(Obfuscation):
    def apply(self, root):
        files = glob.glob(os.path.join(root, "**", "*.py"), recursive=True)
        print(f"Found {len(files)} Python files to obfuscate.")
        for file_path in files:
            print(f"Processing file: {file_path}")
            self.apply_single(file_path)
        print("Dead code insertion complete.")

    def apply_single(self, file_path):
        try:
            tree = get_ast(file_path)
            wrapper = cst.metadata.MetadataWrapper(tree)
            transformer = DeadCodeInsertionTransformer()
            modified_tree = wrapper.visit(transformer)

            with open(file_path, "wt", encoding="utf-8") as f:
                f.write(modified_tree.code)
            print(f"Successfully inserted dead code into {file_path}")
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
            print(e)