import libcst as cst
import libcst.metadata as metadata
from Obfuscations.Obfuscation import Obfuscation
import glob
import os
import random

# Repeat = # times code added per line
# Works by inserting statements for each lines of code in original file
def get_ast(file_path):
    with open(file_path, "rt", encoding="utf-8") as f:
        python_code = f.read()
        return cst.parse_module(python_code)


class DeadCodeInsertionTransformer(cst.CSTTransformer):

    def __init__(self):
        super().__init__()
        self.primes = [
            31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
            73, 79, 83, 89, 97, 101, 103, 107, 109, 113,
            127, 131, 137, 139, 149, 151, 157, 163, 167, 173,
            179, 181, 191, 193, 197, 199, 211, 223, 227, 229,
            233, 239, 241, 251, 257, 263, 269, 271, 277, 281,
            283, 293, 307, 311, 313, 317, 331, 337, 347, 349,
            353, 359, 367, 373, 379, 383, 389, 397, 401, 409,
            419, 421, 431, 433, 439, 443, 449, 457, 461, 463,
            467, 479, 487, 491, 499, 503, 509, 521, 523, 541,
            547, 557, 563, 569, 571, 577, 587, 593, 599, 601,
            607, 613, 617, 619, 631, 641, 643, 647, 653, 659,
            661, 673, 677, 683, 691, 701, 709, 719, 727, 733,
            739, 743, 751, 757, 761, 769, 773, 787, 797, 809,
            811, 821, 823, 827, 829, 839, 853, 857, 859, 863,
            877, 881, 883, 887, 907, 911, 919, 929, 937, 941,
            947, 953, 967, 971, 977, 983, 991, 997
        ]

    """
    Add the is_prime function in the start of EACH module
    """
    def leave_Module(self, original_node, updated_node):
        
        is_prime = cst.parse_statement(
"""
def is_prime(x):
    for i in range(2, (x+1)//2):
        if(x%i==0):
            return False
    return True
"""
        )

        new_body = (is_prime,) + updated_node.body
        return updated_node.with_changes(body=new_body)
    

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
            test = cst.parse_expression(f"is_prime({random.choice(self.primes)})"),
            body=body,
            leading_lines=[]
        )
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