from lark import Lark, Transformer, Token
import re

class T(Transformer):
    def __init__(self):
        super(). __init__()
        self.variables = {}
        self.resultadoConcat = None
        self.esta_dentro_de_if = False
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
        return str(valor[0][1:-1])  # Eliminar comillas [1:-1]
    
    def VARNAME(self, valor):
        nombre = str(valor)
        return nombre
    
    def bloque(self, valor):
        #print("DEBUG - BLOQUE: ", valor)
        return valor
    
    def termino(self, valor):
       return valor[0]
    # /////////////////////////


    #///////////// Métodos para manejar la gramática/////////
    def start(self, valor):
        #print("DEBUG - START: ", valor)
        return valor
        
  
    def instruccion(self, valor):
        if isinstance(valor[0], Impresion):
            # Si estamos dentro de un if, marcamos como diferido
            if self.esta_dentro_de_if:  # ¡Necesitamos un flag para esto!
                valor[0].diferido = True
            valor[0].ejecutar()  # Las diferidas no se ejecutarán aquí
        return valor[0]
    
    def TREE(self, valor):
        print(valor)

    def impresion(self, valor):
            try:
             if(valor[0] in self.variables):
                print("1", self.variables[valor[0]])
             elif(not isinstance(valor[0], (int,float))):
                print("2", valor[0].replace('"', ''))
             else :
                if isinstance(valor[0], str):
                    print("3", valor[0].replace('"', ''))
                else:
                    print("4", valor[0])
            except KeyError:
                print("La variable no ha sido declarada")
            return Impresion(valor[0], self.variables, self.esta_dentro_de_if)
        
        #print("IMPRESION: ", valor[0])
        #return Impresion(valor[0]) #envia a la clase Impresion para guardar el valor y lo imprime solo cuando se solicita
        #print(valor[0]) 
        #return valor
    
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
        #print(valor)
        return valor[0]
    
    def ciclo(self, valor):
        return valor[0]
    
    #////////////////////////////////////////////////////
    #metodo recursivo para imprimir las sentencias dentro del if
    def recursividad_if(self, param):
        # Caso base: Si es una Impresion, ejecútala
        if isinstance(param, Impresion):
            param.ejecutar()
        
        # Caso recursivo: Si es una lista o iterable (pero no un string)
        elif isinstance(param, (list, tuple)) or (hasattr(param, '__iter__') and not isinstance(param, str)):
            for param1 in param:
                self.recursividad_if(param1)
        

    
    # /////////////Métodos para manejar decisiones ////////////////
    def ifstatement(self, valor):
      #print("DEBUG - valor: ", valor)
      
      condicion = valor[0]
      self.esta_dentro_de_if = True
      bloque_if = valor[1]
      elseparte = valor[2] if len(valor) > 2 and valor[2] is not None else []
      # elifparte = valor[2] if len(valor) > 2 and valor[2] is not None else []
      # elseparte = valor[3] if len(valor) > 3 and valor[3] is not None else []
      

      if bool(condicion):
        #print("DEBUG - TRUE")
        for instruccion in bloque_if:
           # print("DEBUG - instruccion: ", instruccion)
            if instruccion is not None:
                #print("DEBUG - si llegamos al if")
                #nos debería llevar a la funcion ejecutar de Impresion
                self.recursividad_if(instruccion)
            else:
                print("DEBUG - instrucción None dentro del if")
      else:
        #print("DEBUG - FALSE")
        for bloque in elseparte:
            self.recursividad_if(bloque)
      return valor
    
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

        resultado = evaluar(bool(valor))

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
        if valor[0] in self.variables and (isinstance(self.variables[valor[0]], int) or isinstance(self.variables[valor[0]], float)):
            resultado = self.variables[valor[0]]
        else: 
            resultado = valor[0]
        for i in range(1, len(valor), 2):
            operador = valor[i]
            termino = valor[i + 1]
            if termino in self.variables and (isinstance(self.variables[termino], int) or isinstance(self.variables[termino], float)):
                termino = self.variables[termino]
            if operador == "+":
                counter = 0
                for val in valor:
                    if re.fullmatch(r"((([1-9]([0-9]+)*)|0)\.([0-9]+))|\d+", str(val)) or re.fullmatch(r"\+|\-|\/|\*", str(val)):
                        counter = counter + 1
                    elif val in self.variables and (isinstance(self.variables[val], int) or isinstance(self.variables[val], float)):
                        counter = counter + 1
                        termino = self.variables[val]
                    else:
                        continue
                
                if (counter != len(valor)):
                    # valor tiene almacenado: [val1, "+", val2, "+", val3, ...]
                    resultado = ""        
                    for val in valor:
                        if isinstance(val, str) and val in self.variables:
                            val = self.variables[val]
                        elif(val == "+"):
                            continue
                        resultado += str(val)  # forzamos a string para concatenar

                else:
                    resultado = resultado + termino
            elif operador == "-":
                resultado = resultado - termino
            elif operador == "*":
                resultado = resultado * termino
            elif operador == "/":
                resultado = resultado / termino
        return resultado

#//////////////////////////////////////////////////////////////

# //////////////////////////////////////////////////////////////
class Impresion:
    def __init__(self, valor, dicc, diferido=False):
        self.valor = valor
        self.variables = dicc
        self.diferido = diferido
        #print("CLASE IMPRESION: ", dicc)

    def ejecutar(self):
        #print("CLASE IMPRESION EJECUTAR: ", self.valor)
        try:
            if not self.diferido:
             if( self.valor in self.variables) :
                print(self.variables[ self.valor])
             elif(not isinstance( self.valor, (int,float))):
                print( self.valor.replace('"', ''))
             else :
                if isinstance( self.valor, str):
                    print( self.valor.replace('"', ''))
                else:
                    print( self.valor)
        except KeyError:
                print("La variable no ha sido declarada")
