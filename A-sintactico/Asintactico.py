from lark import Lark, Transformer

class T(Transformer):
    def __init__(self):
        self.variables = {}
    # Métodos para transformar los nodos del árbol
    # Cada método corresponde a una regla de la gramática

    #//////////Extras////////////
    def NUMBER(self, valor):
        return int(valor)
    
    def expr(self, valor):
        return valor[0]
    
    def add(self, valor):
        left, right = valor
        return left + right
    def varname(self, valor):
      nombre = str(valor[0])
      return self.variables.get(nombre, 0)

    # /////////////////////////


    #///////////// Métodos para manejar la gramática/////////
    def start(self, valor):
        return valor
  
    def instruccion(self, valor):
        return valor[0]
    
    def impresion(self, valor):
        expresion = valor[0]
        print (expresion)
        return None
    
    def declarar(self, valor):
        tipovariable= valor[0]
        varname = valor[1]

        #Si hay un valor, lo asigno
        if len(valor) > 2:
            variable = valor[2]
        else:
            valor = None    

        self.variables[nombre] = valor
        return None
        
    
    def asignacion(self, valor):
        #Se lee de izq a der
        variable = valor[0]
        expresion = valor[1]
        #Creo un diccionario para almacenar las variables y sus valores
        self.variables[variable] = expresion
        return None
    
    def decision(self, valor):
      return valor[0]
    
       
    def ciclo(self, valor):
      return valor[0]
    
    #////////////////////////////////////////////////////


    
    # /////////////Métodos para manejar decisiones ////////////////
    def ifstatement(self, valor):
      condicion = valor[0]
      bloque_if = valor[1]
      elifparte = valor[2] if len(valor) > 2 else []
      elseparte = valor[3] if len(valor) > 3 else None

      if condicion:
        for instruccion in bloque_if:
            instruccion
      else:
        ejecutado = False
        for cond, bloque in elifparte:
            if cond:
                for instruccion in bloque:
                    instruccion
                ejecutado = True
                break
        if not ejecutado and elseparte:
            for instruccion in elseparte:
                instruccion
      return None
    
    def elifparte(self, items):
        resultado = []
        for i in range(0, len(items), 2):
            condicion = items[i]
            bloque = items[i + 1]
            resultado.append((condicion, bloque))
        return resultado

    def elseparte(self, items):
        return items[0]  
  #//////////////////////////////////////////////////////////////


  # //////////////Métodos para manejar ciclos///////////////////
    def forloop(self, valor):
      inicio = valor[0]
      condicion = valor[1]
      incremento = valor[2]
      bloque = valor[3]
      while condicion:
            for instruccion in bloque:
                instruccion
            incremento
            condicion = valor[1]  # reevaluar condición
      return None

    def whileloop(self, valor):
      condicion = valor[0]
      bloque = valor[1]
      while condicion:
            for instruccion in bloque:
                instruccion
            condicion = val[0]  # reevaluar condición
      return None

    def dowhile(self, valor):
      bloque = valor[0]
      condicion = valor[1]
      while True:
            for instruccion in bloque:
                instruccion
            if not condicion:
                break
      return None
    
# /////////////////////////////////////////////////////////////




with open('../Gramatica/grammar.Lark', 'r') as f:
    grammar = f.read()
    
programa = """
  int edad = 1;
  if (edad == 1) {
    out(" hola mundo ");
  };
"""



parser = Lark(grammar, parser='lalr', lexer='contextual', maybe_placeholders=False)

tree = parser.parse(programa)
print(tree.pretty())