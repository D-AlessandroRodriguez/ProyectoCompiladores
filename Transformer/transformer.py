from lark import Lark, Transformer, Token
# self.variables.get(nombre, nombre)

class T(Transformer):
    def __init__(self):
        super(). __init__()
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
        return str(valor[0])  # Eliminar comillas [1:-1]
    
    def VARNAME(self, valor):
        nombre = str(valor)
        return nombre
    
    def bloque(self, valor):
        print("DEBUG - BLOQUE: ", valor)
        return valor
    
    def termino(self, valor):
       return valor[0]
    # /////////////////////////


    #///////////// Métodos para manejar la gramática/////////
    def start(self, valor):
        print("DEBUG - START: ", valor)
        return valor
        
  
    def instruccion(self, valor):
        print("INSTRUCCION: ", valor)
        return valor[0] if valor else None
    
    def impresion(self, valor):
        try:
            print("\"cesar\"".split("\"").len())
            print(self.variables[valor[0]])
        except KeyError:
            print("La variable no ha sido declarada")

        #Impresion(valor[0]) envia a la clase Impresion para guardar el valor y lo imprime solo cuando se solicita
        #print(valor[0])
        return valor
    
    def declarar(self, valor):
        tipo= valor[0]
        nombre = valor[1]
        
        #print(valor)
        #Si hay un valor, lo asigno
        if len(valor) > 2:
            variable = valor[2]
        else:
            variable = None

        self.variables[nombre] = variable
        return valor
        
    
    def asignacion(self, valor):
        #Se lee de izq a der
        variable = valor[0]
        expresion = valor[1]
        
       # print(valor)
        #Creo un diccionario para almacenar las variables y sus valores
        self.variables[variable] = expresion
        return valor
    
    #///////////////////////////////hasta aqui funciona
    def decision(self, valor):
        print(valor)
        return valor[0]
    
    def ciclo(self, valor):
        return valor[0]
    
    #////////////////////////////////////////////////////


    
    # /////////////Métodos para manejar decisiones ////////////////
    def ifstatement(self, valor):
      print("DEBUG - valor: ", valor)
      condicion = valor[0]
      bloque_if = valor[1]
      elifparte = valor[2] if len(valor) > 2 and valor[2] is not None else []
      elseparte = valor[3] if len(valor) > 3 and valor[3] is not None else []
      
      if condicion:
        for instruccion in bloque_if:
            print("DEBUG - instruccion: ", instruccion)
            if instruccion is not None:
                print("DEBUG - si llegamos al if")
                instruccion.ejecutar() #nos debería llevar a la funcion ejecutar de Impresion
            else:
                print("DEBUG - instrucción None dentro del if")
      else:
        ejecutado = False
        for cond, bloque in elifparte:
            if cond:
                for instruccion in bloque:
                    instruccion.ejecutar()
                ejecutado = True
                break
        if not ejecutado and elseparte:
            for instruccion in elseparte:
                instruccion.ejecutar()
      return None
    
    def elifparte(self, valor):
        if not valor: # evitamos que guarde NONE y en cambio envíe una lista vacía
            print("DEBUG - ELIF: ", valor)
            return []
        resultado = []
        for i in range(0, len(valor), 2):
            condicion = valor[i]
            bloque = valor[i + 1]
            resultado.append((condicion, bloque))
        print("DEBUG - ELIF del for: ", valor)
        return resultado

    def elseparte(self, valor):
        if not valor or valor[0] is None: #evitamos que guarde NONE y en cambio envíe una lista vacía
            return []
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
            condicion = valor[0]  # reevaluar condición
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
        def evaluar(v):
            if isinstance(v, Token):
                nombre = str(v)
                return self.variables.get(nombre, nombre)
            return v

        resultado = evaluar(self.variables[valor[0]])

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

class Impresion:
    def __init__(self, valor):
        self.valor = valor
    def ejecutar(self):
        print(self.valor)



with open('../Gramatica/grammar.Lark', 'r') as f:
    grammar = f.read()
"""
with open('../Ejemplos_lenguaje/programas.txt', 'r') as d:
    programa = d.read()
"""

programa = """
    /* esto es un comentario */
    int edad = 17; 
    bool esMayor = FALSE;
    string name = "cesar";

    out("name");
"""

#Crear transformer
trans = Lark(grammar, parser='lalr', transformer=T())
# Transformar el árbol
trans.parse(programa)
