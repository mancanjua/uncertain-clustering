//Estructura del código

Las definiciones de las estructuras de datos están contenidos en el archivo Entities.py. A su vez, todos los métodos relacionados con el algoritmo de clústering están contenidos en el archivo Methods.py, mientras que los métodos auxiliares para las pruebas están en el archivo Test.py. Por último, se cuenta con el archivo "graphics.py", el cual se trata de la librería gráfica externa utilizada para mostrar los resultados.

El método "test" del archivo Test.py ejecuta el algoritmo una vez, y muestra en una ventana la nube de puntos y, al finalizar, los clústeres resultantes y, por consola, los valores de cada iteración y el tiempo que tarda en finalizar.
Este método tiene como entrada los parámetros "points" (una lista de puntos), "solution" (una lista de clústeres solución, opcional), "max_iterations" (condición de parada) y "method" (una de tres variables definidas en el archivo Method).
Los parámetros "points" y "solutions" pueden obtenerse tanto del archivo puntos, en el que se definen puntos1 y puntos2 como una tupla de nube de puntos y solución, o utilizando el método de nube de puntos aleatorios, el cual tiene como parámetros de entrada "number_of_circles", que define el número de circunferencias a crear, "noise", que define el valor de ruido en los puntos, "min_val" y "max_val", que definen el rango en que se generarán los puntos, y "points_per_circle", que define la media de puntos que poseerá cada circunferencia.

El método "test_efficiency" del archivo Test.py ejecuta el algoritmo tantas veces como se le indique, y al acabar, muestra algunos valores sobre los errores medios de todas las iteraciones.
Este método "test_efficiency" tiene como entrada los mismos parámetros que el método "test", además del parámetro "times", el cual define cuantas veces se realiza el algoritmo.

Para definir otros casos de prueba, se debe seguir la estructura previamente mencionada (una lista de puntos y una lista de clústeres) que utilicen las estructuras de datos definidas en la clase Entities.py, cuyos constructores son Point(float x, float y) y Clúster (Point center, float radio).

Al final del archivo Test.py están preparados casos de prueba para ambos métodos ("test" y "test_efficiency"), con diversos parámetros de entrada comentados para facilitar su uso.
