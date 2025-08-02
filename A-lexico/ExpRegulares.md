Documento donde se validara en un archivo .py si el texto tiene un formato valido esto es opcional debido a que Lark hace directamente el analisis sintactico y lexico. Pero para hacer la tabla de simbolos identificar cada token imprimir es valido.

EXPRESIONES REGULARES
Definiciones básicas:
Dígito: [0-9]
Operador: \+|\-|\/|\*
Operador comparación: >=|<=|==|!=|<|>
Operador lógico: &|\||OR|AND

Tipos de variables:
Caracter: [A-z]
Tipo de dato: int, string, bool, float
int: [0-9]+
bool: True|False
float: (([1-9]([0-9]+)*)|0)\.([0-9]+)
string: "[^"\n]"

Variables y expresiones:
Nombre de la variable: [A-z]([A-z]|[0-9])*

Condicionales:
if: if
else: else
elif: elif

Ciclos:
while: while
for: for
doWhile: do

Impresión y comentarios:
Impresión: out
Comentario: \/\*[\s\S]*?\*\/      o        \/\*.*?\*\/ si usamos re.DOTALL
