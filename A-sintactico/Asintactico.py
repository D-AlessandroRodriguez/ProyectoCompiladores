from lark import Lark, Transformer

with open('../Gramatica/grammar.Lark', 'r') as f:
    grammar = f.read()
    
programa = """
   numero = 2;
"""

parser = Lark(grammar, parser='lalr')
tree = parser.parse(programa)
print(tree.pretty())