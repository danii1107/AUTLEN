import ast

class ASTNestedIfCounter(ast.NodeVisitor):
    def __init__(self):
        self.max_depth = 0
        self.current_depth = 0

    def generic_visit(self, node):
        for field_name, field_value in ast.iter_fields(node):
            if isinstance(field_value, list):
                for item in field_value:
                    if isinstance(item, ast.AST):
                        self.visit(item)
            elif isinstance(field_value, ast.AST):
                self.visit(field_value)
        return self.max_depth

    def visit_If(self, node):
        self.current_depth += 1
        self.max_depth = max(self.max_depth, self.current_depth)

        # Cambio aquí para asegurarse de que se visite el cuerpo del if
        self.generic_visit(node)

        self.current_depth -= 1
        

class ASTDotVisitor(ast.NodeVisitor):

    idcounter: int

    def generic_visit(self, node: ast.AST) -> None:
        self.idcounter = 0
        print("digraph {")
        self.visit_node(node)
        print("}")

    def visit_node(self, node: ast.AST) -> None:
        nodeid = self.idcounter
        print('s{}[label="{}({})", shape=box]'.
              format(nodeid, type(node).__name__, self.my_vars(node)))

        for field, value in ast.iter_fields(node):
            if isinstance(value, list) and value:
                for item in value:
                    self.visit_child_node(field, item, nodeid)
            elif isinstance(value, ast.AST):
                self.visit_child_node(field, value, nodeid)

    def visit_child_node(self, field: str, node: ast.AST, parentid: int) -> None:
        self.idcounter += 1
        print(f's{parentid} -> s{self.idcounter}[label="{field}"]')
        self.visit_node(node)

    def my_vars(self, obj: ast.AST) -> str:
        return ", ".join(
            f"{key}='{value}'"
            for key, value in ast.iter_fields(obj)
            if not isinstance(value, (ast.AST, list))
        )