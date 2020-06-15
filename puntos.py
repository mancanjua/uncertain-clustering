from Entities import Point

# Ejemplo 1 Point(Dos circunferencias separadas sin intersección)
# "Solución" usada para generar los puntos:
#           Circunferencia de centro Point(9,5) y radio 2
#         y Circunferencia de centro Point(2,2) y radio 1
# Lista de puntos:
puntos0 = [Point (1,1.1), Point (-1.8,-1.1),Point (-1.5,1.3),Point (1.1,-1)]

puntos1 = [Point(9, 7), Point(7.7, 6.5), Point(7, 5), Point(11, 5), Point(9, 3), Point(10.3, 3.5), Point(7.3, 4), Point(10.3, 6.5), Point(3, 2), Point(2, 3), Point(1, 2),
           Point(2, 1), Point(1.2, 1.4), Point(1.2, 2.6), Point(2.7, 1.3), Point(2.8, 2.6)]

# Ejemplo 2 Point(Dos circunferencias concéntricas
#           y una tercera separada sin intersección)
# "Solución" usada para generar los puntos:
#           Circunferencia de centro Point(9,5) y radio 2
#           Circunferencia de centro Point(9,5) y radio 3
#         y Circunferencia de centro Point(20,18) y radio 6
# Lista de puntos:
puntos2 = [Point(9, 8), Point(7, 7.3), Point(6, 5), Point(12, 5), Point(9, 2), Point(11, 2.7), Point(6.4, 3.5), Point(11, 7.2), Point(11, 5), Point(9, 7), Point(7, 5), Point(9, 3),
           Point(7.4, 3.8), Point(7.4, 6.2), Point(10.4, 3.6), Point(10.6, 6.2), Point(20, 12), Point(20, 24), Point(22, 23.7), Point(24, 22.5), Point(24.4, 22),
           Point(25.6, 20.1), Point(26, 18), Point(25.6, 16), Point(24.4, 14), Point(24, 13.5), Point(22.1, 12.4), Point(17.9, 12.4), Point(15.9, 13.6),
           Point(15.2, 14.5), Point(14.3, 16), Point(14, 18), Point(14.4, 20), Point(15.5, 22), Point(16.3, 22.8), Point(25.2, 15), Point(14.8, 15), Point(19, 12.1),
           Point(23.3, 13), Point(25.9, 19), Point(14.1, 19.2), Point(14.1, 17), Point(15.1, 21.4), Point(17.4, 23.4), Point(18.6, 23.8), Point(21, 23.9),
           Point(23, 23.2), Point(24.9, 21.4), Point(25.4, 20.6), Point(6.2, 6), Point(6.6, 6.8), Point(8, 7.8), Point(9.9, 7.8), Point(10.5, 7.6), Point(11.2, 7),
           Point(11.6, 6.6), Point(11.7, 6.3), Point(11.8, 6), Point(11.9, 5.7), Point(12, 4.6), Point(11.9, 4.2), Point(11.8, 3.8), Point(11.6, 3.5),
           Point(10.5, 2.4), Point(8.2, 2.1), Point(7.4, 2.5), Point(6.1, 4.2), Point(8, 6.7), Point(7.2, 6), Point(7.1, 5.6), Point(7, 4.6), Point(7.1, 4.3),
           Point(7.7, 3.5), Point(8, 3.3), Point(8.3, 3.1), Point(9.5, 3.1), Point(10.8, 4.2), Point(10.8, 5.9), Point(9.8, 6.8)]

puntos1_modified = [Point(item.x+1.5, item.y+1.5) for item in puntos1]

puntos2_modified = [Point(item.x+1, item.y+10) for item in puntos2]

puntos3 = puntos1 + puntos1_modified

puntos4 = puntos2 + puntos2_modified


