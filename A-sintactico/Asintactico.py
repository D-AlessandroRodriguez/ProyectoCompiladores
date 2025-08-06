from lark import Lark, Transformer



with open('../Gramatica/grammar.Lark', 'r') as f:
    grammar = f.read()
    
programa = """
    int contador = 0; 
    bool activo = TRUE; 

    while(activo){ 
        out("Contador: " + contador);
        contador = contador + 1; 
        if(contador >= 5){ 
            activo = FALSE;  
        }; 
    };
"""



parser = Lark(grammar, parser='lalr', lexer='contextual', maybe_placeholders=False)

tree = parser.parse(programa)
print(tree.pretty())