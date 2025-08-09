

from Interprete.consInterprete import Interpretador

"""
    Main donde se llamaa a la clase Interpretador
"""
with open('Gramatica/grammar.Lark', 'r') as f:
    grammar = f.read()

with open('Ejemplos_lenguaje/programas.txt', 'r') as d:
    programa = d.read()

interprete = Interpretador(grammar,programa)
options = input("Como desea programar:\n1. Desde consola\n2. cargar un programa .txt\n3. salir\n>> ")
while(True):
    if options == "1":
            interprete.consola_interactiva()
    elif options == "2":
        interprete.ejecutar_programa(programa)
        options = input("Como desea programar:\n1. Desde consola\n2. cargar un programa .txt\n3. salir\n>> ")
    elif options == "3":
        exit()
    else:
        print("-----------------Opción no válida.-----------------")
        options = input("Como desea programar:\n1. Desde consola\n2. cargar un programa .txt\n3. salir\n>> ")

