
# Gramática sencilla para sumas
from lark import Lark
grammar = """
    start: expr
    expr: expr "+" NUMBER  -> add
        | NUMBER
    %import common.NUMBER
    %import common.WS      
    %ignore WS             
"""         

"""
<suma>::- <num> <ope><num
<num>::- 1|2|3|4
"""

# Crear el parser
parser = Lark(grammar, parser='lalr')

# Analizar una expresión
tree = parser.parse("3 + 5")
print(tree.pretty())  # Imprime el árbol