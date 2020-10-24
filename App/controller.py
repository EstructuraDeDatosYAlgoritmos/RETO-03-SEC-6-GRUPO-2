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

import config as cf
from App import model
from time import process_time as crono
import datetime
import csv

"""
El controlador se encarga de mediar entre la vista y el modelo.
Existen algunas operaciones en las que se necesita invocar
el modelo varias veces o integrar varias de las respuestas
del modelo en una sola respuesta.  Esta responsabilidad
recae sobre el controlador.
"""



# ___________________________________________________
#  Constantes
# ___________________________________________________
DEV = 100000
# ___________________________________________________
#  Inicializacion del catalogo
# ___________________________________________________


def init():
    dataBase = model.newDataBase()
    return dataBase


# ___________________________________________________
#  Funciones para la carga de datos y almacenamiento
#  de datos en los modelos
# ___________________________________________________

def loadData (data_link, sep=","):
    
    accidentsFile = cf.data_dir + data_link
    dataBase = init()

    print("Cargando archivo ....")
    
    startCrono = crono()  #tiempo inicial 
    loadCSVFiles(accidentsFile,dataBase,sep)
    stopCrono = crono()  #tiempo final
    print("Tiempo de ejecución ", stopCrono - startCrono, " segundos")
    
def loadCSVFiles(link, dataBase, sep=";"):
    dialect = csv.excel()
    dialect.delimiter = sep
    with open(link, encoding="utf-8") as csvfile:
        buffer = csv.DictReader(csvfile, dialect=dialect)
        cont = 0
        for accident in buffer:
            cont += 1
            model.updateDataBase(dataBase,accident)
            if cont == DEV:
                pass
        print(cont)

# ___________________________________________________
#  Funciones para consultas
# ___________________________________________________


def accidentsSize(analyzer):
    
    return model.accidentSize(analyzer)


def indexHeight(analyzer):
    """
    Altura del indice (arbol)
    """
    return model.indexHeight(analyzer)


def indexSize(analyzer):
    """
    Numero de nodos en el arbol
    """
    return model.indexSize(analyzer)


def minKey(analyzer):
    """
    La menor llave del arbol
    """
    return model.minKey(analyzer)


def maxKey(analyzer):
    """
    La mayor llave del arbol
    """
    return model.maxKey(analyzer)
  

def getAccidentsBySeverity(analyzer, initialDate, severity):
    initialDate = datetime.datetime.strptime(initialDate, '%Y-%m-%d')
    return model.getAccidentsBySeverity(analyzer, initialDate.date(), severity)
    
def getAccidentsByRangeofDates(analyzer, initialDate, finalDate):
    initialDate = datetime.datetime.strptime(initialDate, '%Y-%m-%d')
    finalDate = datetime.datetime.strptime(finalDate, '%Y-%m-%d')
    return model.getAccidentsByRange(analyzer, initialDate.date(), finalDate.date() )