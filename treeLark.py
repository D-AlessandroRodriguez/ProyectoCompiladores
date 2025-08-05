
# Gramática sencilla para sumas
from lark import Lark, Transformer

# Definición de la clase Transformer
class T(Transformer):
    # Métodos para transformar los nodos del árbol
    # Cada método corresponde a una regla de la gramática
    def NUMBER(self, valor):
        return int(valor)
    def expr(self, valor):
        return valor[0]
    def add(self, valor):
        left, right = valor
        return left + right
    def start(self, valor):
        return valor[0]
        


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

suma = "3 + 5"

# Analizar una expresión
tree = parser.parse(suma)
print(tree.pretty())  # Imprime el árbol


#Crear transformer
trans = Lark(grammar, parser='lalr',transformer=T())
# Transformar el árbol
resultado = trans.parse(suma)

print("Resultado:", resultado)  # Imprime: Resultado: 8

