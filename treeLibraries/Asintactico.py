from lark import Lark, Transformer

class Tree():
    def __init__(self):
        with open("../Gramatica/grammar.Lark", 'r') as f:
            self.grammar = f.read()
        self.parser = Lark(self.grammar, parser='lalr', lexer='contextual', maybe_placeholders=False)
    
    # imprimir arbol cuado se carga un programa
    def printTree(self):
        with open('../Ejemplos_lenguaje/programas.txt', 'r') as d:
            programa = d.read()

        
        tree = self.parser.parse(programa)
        print(tree.pretty())
    
    # imprimir arbol cuado solo da sentencias
    def printTree(self, entrada):
        print(entrada)
        tree = self.parser.parse(entrada)
        print(tree.pretty())