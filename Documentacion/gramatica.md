# Definiciones básicas 

letraMayuscula = "A" | "B" | "C" | "D" | "E" | "F" | "G" | "H" | "I" | "J" | "K" | "L" | "M" | "N" | "O" | "P" | "Q" | "R" | "S" | "T" | "U" | "V" | "W" | "X" | "Y" | "Z" ; 

letraMinuscula = "a" | "b" | "c" | "d" | "e" | "f" | "g" | "h" | "i" | "j" | "k" | "l" | "m" | "n" | "o" | "p" | "q" | "r" | "s" | "t" | "u" | "v" | "w" | "x" | "y" | "z" ; 

digito = "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9" ; 

operador = "+" | "-" | "/" | "*" ; 

operadorComparacion = ">" | "<" | ">=" | "<=" | "==" | "!=" ; 

operadorLogico = "|" | "&" | "OR" | "AND" ; 

  
# Tipos de variables

letra = letraMayuscula | letraMinuscula ; 

caracter = letra ; 

tipoVariable = "int" | "string" | "bool" | "float" ; 

int = digito+ ; 

bool = "True" | "False"  

float = digito+ "." digito+ ; 

string = '"' ( caracter | digito | " " | "." | "," | ";" | ":" | "?" )+ '"' ; 

# Variables y expresiones 

nombreVariable = caracter ( caracter | digito )* ; 

valor = cadena | flotante | entero | bool ; 

termino = nombreVariable | valor | "(" expresion ")" | expresion ; 

expresion = termino ( operador termino )* ; 

# Condiciones,asignaciones y bloque

condicion = termino ( (operadorLogico | operadorComparacion) termino )* | bool ; 

asignacion = nombreVariable "=" termino ; 

bloque = "{" instruccion "}" ; 

instruccion = declararVariable | asignacion | decision | ciclo | impresion ; 

declararVariable = tipoVariable nombreVariable ; 

  
 
# Condicionales

decision = ifStatement ; 

ifStatement = "if" "(" condicion ")" bloque elifParte? elseParte? ; 

elifParte = ("elif" "(" condicion ")" bloque)* ; 

elseParte = "else" bloque ; 

# Ciclos

ciclo = forLoop | whileLoop | doWhile ; 

forLoop = "for" "(" asignacion "," asignacion "," asignacion ")" bloque ; 

whileLoop = "while" "(" condicion ")" bloque ; 

doWhile = "do" bloque "while" "(" condicion ")" ; 

# Impresión y comentarios

impresión = "out(" termino ")" ; 

comentario = "/* "  (caracter | digito | " " | "." | ":" | "?" | "\n" | "\t")*  " */" ; 



 

 

 

 