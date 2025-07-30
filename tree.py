import ast

codigo = '2+2'

# Generar el AST
arbol = ast.parse(codigo)

# Imprimir el AST en formato texto
print(ast.dump(arbol, indent=4))