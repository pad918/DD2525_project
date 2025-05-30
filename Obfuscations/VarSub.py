from Obfuscations.Obfuscation import Obfuscation
import libcst as cst
import libcst.metadata as metadata
import random
import glob
import os

def get_ast(file_path):
    with open(file_path, "rt", encoding="utf-8") as f:
        python = f.read()
        return cst.parse_module(python)


class RenamingTransformer(cst.CSTTransformer):
    # Declare the metadata dependencies for this transformer
    METADATA_DEPENDENCIES = [metadata.ScopeProvider]

    def generate_random_name():
        cringabet = "αβγΔεζηΘικλμνΞοπρΣτυΦχψωあいうえおアイウエオ가나다라마你好世界的您好世界的åäöз"
        return "".join([cringabet[random.randint(0, len(cringabet)-1)] for r in range(10)])

    def __init__(self):
        super().__init__()
        self._name_map = {}
        self._current_class = None
        self._curr_function = None

    def visit_ClassDef(self, node: cst.ClassDef) -> bool:
        self._current_class = node
        return True

    def leave_ClassDef(
        self, original_node: cst.ClassDef, updated_node: cst.ClassDef
    ) -> cst.ClassDef:

        self._current_class = None
        return updated_node

    # Remove all comments
    def leave_Comment(self, original_node: cst.Comment, updated_node: cst.Comment):
        return updated_node.deep_remove(updated_node)

    def leave_Name(
        self, original_node: cst.Name, updated_node: cst.Name
    ) -> cst.Name:

        # Get the scope associated with this Name node
        try:
            scope = self.get_metadata(metadata.ScopeProvider, original_node)
            #t = self.get_metadata(metadata.FullyQualifiedNameProvider, original_node)
        except BaseException as e:
            return updated_node # The library is kind of shit
        
        # Do not rename any methods
        if isinstance(scope, metadata.ClassScope): # Apparently methods are "function scope!"
            return updated_node

        # Do not rename built in variables / functions
        names = scope.get_qualified_names_for(original_node)

        name_key = None
        # Test if the name is defined in builtin scope!
        if(len(names)==1):
            for n in names:
                if(n.source.name == 'BUILTIN' or n.source.name == 'IMPORT'):
                    return updated_node
                name_key = (n.name, original_node.value)

        # Check if we've already generated a new name for this variable in this scope
        if name_key not in self._name_map:
            # If not, generate a new random name
            new_name = RenamingTransformer.generate_random_name()
            # Store the mapping
            self._name_map[name_key] = new_name
        else:
            # If we have a mapping, retrieve the existing new name
            new_name = self._name_map[name_key]

        # Return a new Name node with the updated value (the random name)
        return updated_node.with_changes(value=new_name)



class VarSub(Obfuscation):
    
    def __init__(self):
        pass

    def apply(self, root):
        # Find all python files
        files = glob.glob(os.path.join(root, "**", "*.py"), recursive=True)
        for file in files:
            self._apply_single(file)
        
    def _apply_single(self, py_file_path):
        try:
            tree = get_ast(py_file_path)
        except BaseException as e:
            print(f"Could not parse file: {py_file_path}")
            return

        wrapper = cst.metadata.MetadataWrapper(tree)

        transformer = RenamingTransformer()

        modified_tree = wrapper.visit(transformer)
        with open(py_file_path, "wt", encoding="utf-8") as f:
            f.write(modified_tree.code)