from lark import Lark, Transformer

class T(Transformer):
    def __init__(self):
        self.variables = {}
    # Métodos para transformar los nodos del árbol
    # Cada método corresponde a una regla de la gramática

    #//////////Extras////////////
    def entero(self, valor):
        return int(valor[0])
    def decimal(self, valor):
        return float(valor[0])
    def booleano(self, valor):
        return valor[0] == "TRUE"
    def cadena(self, valor):
        return tipo(valor[0][1:-1])  # Eliminar comillas
    def nombre(self, valor):
      nombre = str(valor[0])
      return self.variables.get(nombre, nombre)
    def bloque(self, valor):
        return valor
    def termino(self, valor):
       return valor[0]
    # /////////////////////////


    #///////////// Métodos para manejar la gramática/////////
    def start(self, valor):
         for instruccion in valor:
            if instruccion is not None:
                instruccion  # Ejecutar cada instrucción
  
    def instruccion(self, valor):
        return valor[0]
    
    def impresion(self, valor):
        expresion = valor[0]
        print (expresion)
        return None
    
    def declarar(self, valor):
        tipo= valor[0]
        nombre = valor[1]

        #Si hay un valor, lo asigno
        if len(valor) > 2:
            variable = valor[2]
        else:
            variable = None    

        self.variables[nombre] = variable
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
    
    def elifparte(self, valor):
        resultado = []
        for i in range(0, len(valor), 2):
            condicion = valor[i]
            bloque = valor[i + 1]
            resultado.append((condicion, bloque))
        return resultado

    def elseparte(self, valor):
        return valor[0]  
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
    

# ////////////////Metodos de condiciones y operaciones logicas////////////////
    def condicion(self, valor):
        resultado = valor[0]
        i = 1
        while i < len(valor):
            operador = valor[i]
            derecho = valor[i + 1]
            if operador == "==":
                resultado = resultado == derecho
            elif operador == "!=":
                resultado = resultado != derecho
            elif operador == "<":
                resultado = resultado < derecho
            elif operador == ">":
                resultado = resultado > derecho
            elif operador == "<=":
                resultado = resultado <= derecho
            elif operador == ">=":
                resultado = resultado >= derecho
            elif operador in ("&&", "AND"):
                resultado = resultado and derecho
            elif operador in ("||", "OR"):
                resultado = resultado or derecho
            i += 2
        return resultado

    def expresion(self, valor):
        resultado = valor[0]
        for i in range(1, len(valor), 2):
            operador = valor[i]
            termino = valor[i + 1]
            if operador == "+":
                resultado = resultado + termino
            elif operador == "-":
                resultado = resultado - termino
            elif operador == "*":
                resultado = resultado * termino
            elif operador == "/":
                resultado = resultado / termino
        return resultado

# //////////////////////////////////////////////////////////////



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