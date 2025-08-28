from lark import Lark
from Analizadores.transformer import T
"""
    Módulo que hace uso del transfor para ejecutar las instrucciones    
"""
class Interpretador:
    def __init__(self, grammar):
        self.Sentence = []
        self.parserTree = Lark(grammar, parser='lalr', lexer='contextual', maybe_placeholders=False)
        self.parser = Lark(grammar, parser='lalr', transformer = T())

    def ejecutar_programa(self, programa):
        lineaPrograma = str(programa).split("\n")
        for item in lineaPrograma:
            self.ejecutar_linea(item.replace(" ", ""))
      
    def ejecutar_linea(self, linea):
       try:
        if linea != "Tree()":
            self.parser.parse(linea)
            self.Sentence.append(linea)
        else:
            programaComplete = " ".join(self.Sentence)
            tree = self.parserTree.parse(programaComplete)
            print("====================")
            print(tree.pretty())
            print("====================")
       except Exception as e:
        print("Error al interpretar:", e)

    def ejecutar(self, texto):
        try:
            searchTree = texto.find("Tree()")
            if searchTree >= -1:
                self.parser.parse(texto)
            else:
                newText = texto.replace("Tree()", "")
                self.parser.parse(newText)
                tree = self.parserTree.parse(newText)
                
                print(" \nARBOL SINTÁCTICO")
                print("====================")
                print(tree.pretty())

        except Exception as e:
            print("Error al interpretar el programa:", e)

    def consola_interactiva(self):
        print("Modo consola interactiva (escribe 'salir' para terminar)")
        while True:
            linea = input(">> ").strip()
            if linea.lower() == "salir":
                print("Saliendo de la consola...")
                exit()
            if linea == "":
                continue  # evita intentar ejecutar líneas vacías
            
            self.ejecutar_linea(linea)
        
            
            
        
            