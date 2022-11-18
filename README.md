# Compilador SOYUZ

## Entregable #1

Durante esta primer semana de trabajo, primero decidí que estaré utilizando **PLY**, ya que durante los ejercicios hechos de tarea, fue la herramienta con la que me sentí más a gusto. Se realizaron primero los diagramas de flujo para las diferentes variables semánticas a papel. Usando estos diagramas como base, se realizó primero el léxico `myC_Lex.py` , y finalmente se realizó la gramática en `myC_Yacc.py`. Para probar que la gramática funcionara correctamente, hice un archivo `programTest.txt` y se arreglaron bugs en cuanto aparecían al probar con dicho archivo.

## Entregable #2

Durante la segunda semana, cree el directorio de funciones `functionDirectory.py` que contiene `DirFunc` que tiene el diccionario de funciones y variables ademas de varias funciones que facilitan la manipulación de dicho diccionario desde `myC_Yacc.py`; contiene también la clase `varAttributes` que facilita la creación de variables para agregar al diccionario. Se utilizaron estas funciones en `myC_Yacc.py` en los llamados _puntos neurálgicos_. Finalmente, hice el archivo `oracle.py` que contiene al oráculo `TIRESIAS` que utiliza un diccionario como cubo semántico para decirnos qué tipo tendrá el resultado de una operación de acuerdo a los tipos de sus operandos.

## Entregable #3

Durante la tercer semana, se creó el archivo `quadruples.py` que contiene las clases `QuadrupleTable` y `Quadruple`. Estas clases tienen diferentes métodos sirven para generar, modificar y sacar datos de los cuádruplos que se generarán durante la compilación. Se agregaron los _puntos neurálgicos_ en la gramática para generar los cuádruplos. Hasta ahora se generan correctamente los cuádruplos para las operaciones simples, incluyendo la asignación, `READ` y `WRITE` y con los condicionales `IF`, `ELSE IF` y `ELSE`. Las variables temporales que se generan no tienen espacio de memoria asignado.

## Entregable #4

Durante la cuarta semana, se creó el código para generar cuádruplos para los cyclos condicionales `WHILE` y no condicionales `FROM-TO` al igual que se agregaron los _puntos neurálgicos_ en la parte de la gramática.

## Entregable #5

Durante la quinta semana, se creó el código para generar los cuádruplos para las funciones (`GOSUB`, `ERA`, `ENDFUNC`) pero estas no son funcionales. Se creó `virtualMachine.py` que sirve para correr todo el código. Los cuádruplos de operaciones aritméticas ahora se ejecutan dentro de la máquina virtual al igual que los cuádruplos de saltos, por lo que también funcionan correctamente los ciclos y condicionales. Se aprovechó esta semana para arreglar algunos errores, principalmente los tipos `CHAR` y la impresión de constantes `STRING`.

## Entregable #6

Se generó el código para los arreglos en compliación, como los cuadruplos para revisar que los resultados de las expresiones estén dentro del rango del tamaño del arreglo o lista. Se finalizó el funcionamiento de los cuadruplos para funciones en la máquina virtual.

## Entregable #7

Se creó el código para ejecutar los cuádruplos de los arreglos y listas en la máquina virtual. Se hicieron los últimos cambios para arreglar errores y se finalizó el código para la aplicación particular. Se escribió la ducumentación.
