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
        # Dead code to insert
        self._dead_code_templates = [
            "import random",
            "temp_var_1 = 5 * 7",
            "is_prime_check = all(random.randint(1000,4671) % i != 0 for i in range(2, int(random.randint(1000,4671)**0.5) + 1))",
            "if is_prime_check: print('test')",
        ]

    def generate_dead_code_statements(self):
        statements = []
        repeat = 1
        # insert x times
        for _ in range(repeat):
            for template in self._dead_code_templates:
                parsed_module = cst.parse_module(template)
                statements.append(parsed_module.body[0])
        return statements

    def leave_Module(self, original_node, updated_node):
        dead_code_block_nodes = self.generate_dead_code_statements()
        new_body_statements = []
        for stmt in updated_node.body:
            new_body_statements.extend(dead_code_block_nodes)
            new_body_statements.append(stmt)

        return updated_node.with_changes(body=tuple(new_body_statements))

    def leave_FunctionDef(self, original_node, updated_node):
        original_function_stmts = updated_node.body.body
        dead_code_block_nodes = self.generate_dead_code_statements()
        new_function_body_stmts = []
        for stmt in original_function_stmts:
            new_function_body_stmts.extend(dead_code_block_nodes)
            new_function_body_stmts.append(stmt)

        new_function_body = updated_node.body.with_changes(
            body=tuple(new_function_body_stmts)
        )
        return updated_node.with_changes(body=new_function_body)


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
