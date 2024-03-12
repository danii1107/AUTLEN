import ast
import inspect
import sys
from ast_utils import ASTNestedIfCounter, ASTDotVisitor

def fun1(p):
    a = 1
    b = 2
    if a == 1:
        print(a)
    if b == 1:
        print(b)

def fun2(p):
    a = 1
    if a == 1:
        print(a)
    if True:
        if True:
            if a == 1:
                print(a)

def main() -> None:
    counter = ASTNestedIfCounter()

    # Prueba para fun1
    source_fun1 = inspect.getsource(fun1)
    my_ast_fun1 = ast.parse(source_fun1)
    print("fun1: máximo número de if anidados:", counter.visit(my_ast_fun1))

    # Redirigir la salida a un archivo DOT
    with open('fun1.dot', 'w') as dot_file:
        sys.stdout = dot_file
        # Crear una instancia de ASTDotVisitor y visualizar el AST de fun1
        dot_visitor_fun1 = ASTDotVisitor()
        dot_visitor_fun1.generic_visit(my_ast_fun1)

    # Restaurar la salida estándar al terminal
    sys.stdout = sys.__stdout__

    # Prueba para fun2
    source_fun2 = inspect.getsource(fun2)
    my_ast_fun2 = ast.parse(source_fun2)
    print("fun2: máximo número de if anidados:", counter.visit(my_ast_fun2))

    # Redirigir la salida a un archivo DOT
    with open('fun2.dot', 'a') as dot_file:
        sys.stdout = dot_file
        # Crear una instancia de ASTDotVisitor y visualizar el AST de fun2
        dot_visitor_fun2 = ASTDotVisitor()
        dot_visitor_fun2.generic_visit(my_ast_fun2)

    # Restaurar la salida estándar al terminal
    sys.stdout = sys.__stdout__

if __name__ == "__main__":
    main()
