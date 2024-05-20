class AST:
    def __init__(self, value):
        self.value = value
        self.parent = None
        self.children = []

    def set_parent(self, ast_node):
        self.parent = ast_node
        ast_node.children.append(self)

    def get_AST(self, depth):
        ast_code = ""
        if depth == 0:
            ast_code = f"{self.value}\n"
        else:
            ast_code = "|" + "-" * (depth * 5 - 1) + f"{self.value}\n"
        for child in self.children:
            ast_code += child.get_AST(depth + 1)
        return ast_code