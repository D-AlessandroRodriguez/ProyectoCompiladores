from lark import Lark, Transformer

with open('../Gramatica/grammar.Lark', 'r') as f:
    grammar = f.read()
    
programa = """
  if(TRUE){
    int edad;
  };
"""

parser = Lark(grammar, parser='lalr', lexer='contextual', maybe_placeholders=False)

tree = parser.parse(programa)
print(tree.pretty())