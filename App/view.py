  
"""
 * Copyright 2020, Departamento de sistemas y Computación
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 """

import sys
import config
from DISClib.ADT import map as m
from DISClib.ADT import list as lt
from App import controller
assert config

"""
La vista se encarga de la interacción con el usuario.
Presenta el menu de opciones  y  por cada seleccion
hace la solicitud al controlador para ejecutar la
operación seleccionada.
"""

# ___________________________________________________
#  Ruta a los archivos
# ___________________________________________________

accidentsfile = 'us_accidents_dis_2019.csv'

# ___________________________________________________
#  Menu principal
# ___________________________________________________

def mainMenu()->None:
    """
    Imprime el menu de opciones
    """
    print("\n")
    print("*******************************************")
    print("Bienvenido")
    print("1- Cargar información de accidentes")
    print("2- Consultar los accidentes en una fecha dada")
    print("3- Requerimiento 2")
    print("0- Salir")
    print("*******************************************")
"""
def alt():
    
    Menu principal
    
    while True:
        printMenu()
        inputs = input('Seleccione una opción para continuar\n>')

        if int(inputs[0]) == 1:
            print("\nInicializando....")
            # cont es el controlador que se usará de acá en adelante
            cont = controller.init()

        elif int(inputs[0]) == 2:
            print("\nCargando información de accidentes....")
            controller.loadData(cont, accidentsfile)
            print('\nAccidentes cargados: ' + str(controller.accidentsSize(cont)))
            print('Altura del arbol: ' + str(controller.indexHeight(cont)))
            print('Elementos en el arbol: ' + str(controller.indexSize(cont)))
            print('Menor Llave: ' + str(controller.minKey(cont)))
            print('Mayor Llave: ' + str(controller.maxKey(cont)))

        elif int(inputs[0]) == 3:
            initialDate = input("\nIngrese la fecha (YYYY-MM-DD): ")
            print("\nBuscando accidentes de " + initialDate + "....")
            severity1 = int(controller.getAccidentsBySeverity(cont, initialDate, '1'))
            severity2 = int(controller.getAccidentsBySeverity(cont, initialDate, '2'))
            severity3 = int(controller.getAccidentsBySeverity(cont, initialDate, '3'))
            severity4 = int(controller.getAccidentsBySeverity(cont, initialDate, '4'))
            totalseverities = severity1+severity2+severity3+severity4
            print("\nEn la fecha " + initialDate + " hubo " + str(totalseverities) + " accidentes. "
            "Hubo " + str(severity1) + " de severidad 1, " + str(severity2) + " de severidad 2, " + str(severity3) + " de severidad 3, " + str(severity4) +" de severidad 4. ")
        else:
            pass

"""
# ___________________________________________________
#  Init Function
# ___________________________________________________

def ejecutarSeverityByDate(dataBase)->None:
    initialDate = input("\nIngrese la fecha (YYYY-MM-DD): ")
    print("\nBuscando accidentes de " + initialDate + "....")
    print("Los resultados son:")
    data = controller.getSeverityByDate(dataBase,initialDate)
    count = len(data)
    total = lt.removeFirst(data)
    while count > 0:
        count -= 1
        result = lt.removeFirst(data)
        if result is not None:
            print(f"\tDe severidad {result[0]} se encontraron {result[1]} accidentes")

    print(f"con un total de {total} accidentes")
        





# ___________________________________________________
#  Main Function
# ___________________________________________________

def main():
    """
    Método principal del programa, se encarga de manejar todos los metodos adicionales creados
        Parametros: 
            None
        Returna: 
            None 
    """
    dataReady = False
    dataBase = None

    while True:
        mainMenu() #imprimir el menu de opciones en consola
        inputs = input('Seleccione una opción para continuar\n') #leer opción ingresada
        
        if len(inputs)>0 and (dataReady or int(inputs[0])<=1):
            if int(inputs[0]) == 1:  #opcion 1
                del dataBase
                dataBase = controller.loadData(accidentsfile)
                dataReady = True

            elif int(inputs[0]) == 2:  #opcion 2
                ejecutarSeverityByDate(dataBase)
                
            elif int(inputs[0])==0: #opcion 0, salir
                sys.exit(0)
                
        else:
            print("Porfavor, cargue datos")

if __name__ == "__main__":
    main()