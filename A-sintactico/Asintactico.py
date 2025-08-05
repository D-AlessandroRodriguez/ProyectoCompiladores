from lark import Lark, Transformer

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
  
    def instruccion(self, valor):
        return valor[0]
    
    def impresion(self, valor):
        
        print = valor[0]
        expresion = valor[1]
        #impresion: PRINT "(" expresion ")" ";"
        return f"Impresion: {expresion}"
    
    def declarar(self, valor):
        tipovariable= valor[0]
        varname = valor[1]

        #Si hay un valor, lo asigno
        if len(valor) > 2:
            variable = valor[2]
        else:
            valor = None    
        
        #Si hay un valor, lo imprimo
        if variable is None:
          return f"Declara: {tipovariable} {varname}"
        else:
          return f"Declara: {tipovariable} {varname} = {variable}"
    
    def asignacion(self, valor):
        #Se lee de izq a der
        variable = valor[0]
        expresion = valor[1]
        #Creo un diccionario para almacenar las variables y sus valores
        self.variables[variable] = expresion
        return f"Asignar: {variable} = {expresion}"
    
    def decision(self, valor):
        #Se lee de arriba hacia abajo
        ifstatement = valor[0]
        condicion = valor[1]
        bloque = valor[2]
        elifparte = valor[3] if len(valor) > 3 else []
        elseparte = valor[4] if len(valor) > 4 else None
        return f"Decisión: {ifstatement} {condicion} {bloque}"
        #Tengo que ver como se manejan los bloques de codigo con elif y else
    
    def ciclo(self, valor):
        return f"Ciclo: {valor[0]} {valor[1]} {valor[2]}"




with open('../Gramatica/grammar.Lark', 'r') as f:
    grammar = f.read()
    
programa = """
  int edad = 1;
"""



parser = Lark(grammar, parser='lalr', lexer='contextual', maybe_placeholders=False)

tree = parser.parse(programa)
print(tree.pretty())