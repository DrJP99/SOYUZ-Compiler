# Compilador SOYUZ (Nombre Tentativo)

## Entregable #1

Durante esta primer semana de trabajo, primero decidí que estaré utilizando **PLY**, ya que durante los ejercicios hechos de tarea, fue la herramienta con la que me sentí más a gusto. Se realizaron primero los diagramas de flujo para las diferentes variables semánticas a papel. Usando estos diagramas como base, se realizó primero el léxico `myC_Lex.py` , y finalmente se realizó la gramática en `myC_Yacc.py`. Para probar que la gramática funcionara correctamente, hice un archivo `programTest.txt` y se arreglaron bugs en cuanto aparecían al probar con dicho archivo.

## Entregable #2

Durante la segunda semana, cree el directorio de funciones `functionDirectory.py` que contiene `DirFunc` que tiene el diccionario de funciones y variables ademas de varias funciones que facilitan la manipulación de dicho diccionario desde `myC_Yacc.py`; contiene también la clase `varAttributes` que facilita la creación de variables para agregar al diccionario. Se utilizaron estas funciones en `myC_Yacc.py` en los llamados _puntos neurálgicos_. Finalmente, hice el archivo `oracle.py` que contiene al oráculo `TIRESIAS` que utiliza un diccionario como cubo semántico para decirnos qué tipo tendrá el resultado de una operación de acuerdo a los tipos de sus operandos.