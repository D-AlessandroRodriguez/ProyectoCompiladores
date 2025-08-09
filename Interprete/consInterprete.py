from lark import Lark
from Interprete.transformer import T
from treeLibraries.Asintactico import Tree
import os

class Interpretador:
    def __init__(self, grammar,programa):
        self.Sentence = []
        self.grammar = grammar
        self.programa = programa
        self.transformer = T()
        self.parserTree = Lark(self.grammar, parser='lalr', lexer='contextual', maybe_placeholders=False)
        self.parser = Lark(self.grammar, parser='lalr', transformer=self.transformer)

    def ejecutar_programa(self, programa):
        self.ejecutar(programa)
        self.printTable(self.programa)
    
    def printTable(self,program):
        try:
            lexer = self.parserTree.lex(program)
            print("\n TABLA ")
            print("====================")
            print(f"{'Línea':<10}{'Token':<15}{'Valor':<20}{'Columna':<10}")
            print("-" * 60)
            for token in lexer:
                print(f"{token.line:<10}{token.type:<15}{str(token.value):<20}{token.column:<10}")
        except Exception as e:
            print(" Error al analizar léxicamente:", e)
      
    def ejecutar_linea(self, linea):
       try:
        if linea != "Tree()":
            self.parser.parse(linea)
            self.Sentence.append(linea)
        else:
            programaComplete = " ".join(self.Sentence)
            tree = self.parserTree.parse(programaComplete)

            print(" ARBOL SINTÁCTICO")
            print("====================")
            print(tree.pretty())

          
            self.printTable(programaComplete)
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
        
            
            
        
            