from lark import Lark
from Interprete.transformer import T
from treeLibraries.Asintactico import Tree
import os

class Interpretador:
    def __init__(self, grammar):
        self.Sentence = []
        self.grammar = grammar
        self.transformer = T()
        self.parserTree = Lark(self.grammar, parser='lalr', lexer='contextual', maybe_placeholders=False)
        self.parser = Lark(self.grammar, parser='lalr', transformer=self.transformer)

    def ejecutar_programa(self, programa):
        self.ejecutar(programa)

    def ejecutar_linea(self, linea):
        try:
            if not linea == "Tree()":
                self.parser.parse(linea)
                self.Sentence.append(linea)
            else:
                programaComplete = " ".join(self.Sentence)
                tree = self.parserTree.parse(programaComplete)
                print(tree.pretty())
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