
# Gramática sencilla para sumas
from lark import Lark, Transformer

class T(Transformer):
    def NUMBER(self, tok):
        return int(tok)
    def expr(self, items):
        return items[0]
    def add(self, items):
        left, right = items
        return left + right
    def start(self, items):
        return items[0]
        


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


#Crear transformer
trans = Lark(grammar, parser='lalr',transformer=T())
# Transformar el árbol
resultado = trans.parse("3 + 5")

print("Resultado:", resultado)  # Imprime: Resultado: 8

