# Compilador SOYUZ (Nombre Tentativo)

## Entregable #1

Durante esta primer semana de trabajo, primero decidí que estré utilizando **PLY**, ya que durante los ejercicios hechos de tarea, fue la herramienta con la que me sentí más agusto. Se realizaron primero los diagramas de flujo para las diferentes variables semanticas a papel. Usando estos diagramas como base, se realizó primero el lexico `myC_Lex.py` , y finalmente se realizó la gramatica en `myC_Yacc.py`. Para probar que la gramatica funcionara correctamente, hice un archivo `programTest.txt` y se arreglaron bugs en cuanto aparecían al provar con dicho archivo.

## Entregable #2

Durante la segunda semana, cree el directorio de funciones `functionDirectory.py` que contiene `DirFunc` que tiene el diccionario de funciones y variables ademas de varias funciones que facilitan la manipulación de dicho diccionario desde `myC_Yacc.py`; contiene también la clase `varAttributes` que facilita la creción de variables para agregar al diccionnario. Se utilizaron estas funciones en `myC_Yacc.py` en los llamados _puntos neuralgicos_. Finalmente, hice el archivo `oracle.py` que contiene al oraculo `TIRESIAS` que utiliza un diccionario como cubo semántico para decirnos qué tipo tendrá el resultado de una operación de acuerdo a los tipos de sus operandos.