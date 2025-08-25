from lark import Lark, Transformer, Token
import re

class T(Transformer):
    def __init__(self):
        super(). __init__()
        self.variables = {}
        self.tableSymbol = {}

        self.dentroIf = False
        self.dentroElse = False
        self.Condicion = False

    #//////////Extras////////////
    def entero(self, valor):
        return int(valor[0])
    
    def decimal(self, valor):
        return float(valor[0])
    
    def booleano(self, valor):
        return valor[0] == "TRUE"
    
    def cadena(self, valor):
        return str(valor[0])
    
    def VARNAME(self, valor):
        return valor
    
    def bloque(self, valor):
        return valor
    
    def termino(self, valor):
       return valor
    # /////////////////////////


    #///////////// Métodos para manejar la gramática/////////
    def start(self, valor):
        return valor
    
    def printable(self, valor):
            print(" " * 37  + "TABLA ")
            print("-" * 80)
            print("name", " " * 16, "tipo", " " * 16,"valor", " " * 16, "linea", " " * 16)
            print("-" * 80)
            for item in self.tableSymbol.values():
                for val in item.values():
                    valor = 22 - len(str(val))
                    print(val," " * valor,end="")
                print()
            print("-" * 80)
        
    
    def instruccion(self, valor):
        print("print de instruccion->",valor)
        return valor[0]
    
    def TREE(self, valor):
        print(valor)

#tomar en cuenta que muchas veces no se necesita imprimir una variable sino solo un literal
    def impresion(self, valor):
        tipo = type(valor[0]) 
   
        print(self.dentroIf, self.Condicion, self.dentroElse)
        if self.dentroIf == True and self.Condicion == True and self.dentroElse == False:
            Impresion().ejecutar(self, valor)
        elif self.dentroIf == False and self.dentroElse == False:
            Impresion().ejecutar(self, valor)
        elif self.dentroIf == True and self.Condicion == False and self.dentroElse == True:
             Impresion().ejecutar(self, valor)
        
    def declarar(self, valor):
        tipo = str(valor[0])
        nombre = str(valor[1])
        
        try:
            if  self.tableSymbol[nombre]:
                print(f"Error linea-{ valor[0].line} La variable <{nombre}> ya ha sido declarada")
        except KeyError:
            if len(valor) > 2:
                variable = valor[2]
                self.tableSymbol[nombre] = (
                    {
                    "name": nombre,
                    "tipo": tipo,
                    "valor":  valor[2], 
                    "linea": valor[0].line
                    }
                )
            else:
                variable = None
                self.tableSymbol[nombre] = (
                    {
                    "name": nombre,
                    "tipo": tipo,
                    "valor":  None, 
                    "linea": valor[0].line
                    }
                )
            self.variables[nombre] = variable
        return valor
        
    
    def asignacion(self, valor):
        variable = valor[0]
        expresion = valor[1]
        
        variableType = self.tableSymbol[variable]
        tipo = variableType["tipo"]

        if variableType["tipo"] == "int" and isinstance(expresion, int): 
            self.variables[variable] = expresion
        elif variableType["tipo"] == "float" and isinstance(expresion, float):
            self.variables[variable] = expresion
        elif variableType["tipo"] == "string" and isinstance(expresion, str):
            self.variables[variable] = expresion
        elif variableType["tipo"] == "bool" and isinstance(expresion, bool):
            self.variables[variable] = expresion
        else:
            print(f"Error linea {valor[0].line} no se puede asignar \"{expresion}\" a la variable \"{variable}\"")
       
        return valor
    
    #///////////////////////////////hasta aqui funciona
    def decision(self, valor):
        return valor[0]
    
    def ciclo(self, valor):
        return valor[0]
    
    #////////////////////////////////////////////////////
    #metodo recursivo para imprimir las sentencias dentro del if
    def ifgrammar(self, valor):
        self.dentroIf = True

    # /////////////Métodos para manejar decisiones ////////////////
    def ifstatement(self, valor):
      return valor
    
    #esta parte no se ejecutara por los momentos
    def elifparte(self, valor):
        if not valor: # evitamos que guarde NONE y en cambio envíe una lista vacía
            print("DEBUG - ELIF: ", valor)
            return []
        resultado = []
        for i in range(0, len(valor), 2):
            condicion = valor[i]
            bloque = valor[i + 1]
            resultado.append((condicion, bloque))
        return resultado

    def elsegrammar(self, valor):
        if self.Condicion == False:
            self.dentroElse = True
        self.Condicion = False

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
        self.Condicion = resultado
        return resultado
    
    def expresion(self, valor):
       # print("expresion->" , valor)
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
       #validamos si existe el nombre de la variable y lo asignamos a la variable existen   
        return resultado

# //////////////////////////////////////////////////////////////
class Impresion(Transformer):
    """def __init__(self, valor):
        valor = valor
        self.variables = self
    """
    def ejecutar(selfNew, self, valor):
        tipo = type(valor[0]) 
        try:
            if str(valor[0]).find("\"")>=0:
                print("impresion cadena->",valor[0])
            elif tipo == int or tipo == float or tipo == bool:
                print("impresion numero->", valor[0])
            elif self.variables.get(valor[0]) != None:
                print("impresion variable->",self.variables.get(valor[0]))
            else:
                print(f"Error de impresion linea-{valor[0].line} la variable <{valor[0]}> no existe")
        except KeyError:
                print("La variable no ha sido declarada")
# //////////////////////////////////////////////////////////////

with open('../Gramatica/grammar.Lark', 'r') as f:
    grammar = f.read()

entrada ="""/* esto es un comentario */
    int edad = 3;
    out(edad);

    if(3<4){
        string name = "entre";
        out(name);
    }else{
        out(edad);
    };
    
    Tree()
    """
#$prinTable()$

parser = Lark(grammar, parser='lalr', transformer = T())
parser.parse(entrada)