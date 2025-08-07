from lark import Lark, Transformer



with open('../Gramatica/grammar.Lark', 'r') as f:
    grammar = f.read()
    
programa = """
    /* esto es un comentario */
    int edad = 1;
    if (edad == 1) {
        out("hola mundo");
    };

"""



parser = Lark(grammar, parser='lalr', lexer='contextual', maybe_placeholders=False)

tree = parser.parse(programa)
print(tree.pretty())