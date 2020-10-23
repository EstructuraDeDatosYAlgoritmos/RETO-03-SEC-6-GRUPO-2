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
import config
from DISClib.ADT import list as lt
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import map as m
import datetime
assert config

"""
En este archivo definimos los TADs que vamos a usar,
es decir contiene los modelos con los datos en memoria
"""

# ==============================
# Funciones Estructurales
# ==============================

def newDataBase():
    """ Inicializa el analizador
    Crea una lista vacia para guardar todos los accidentes
        Estructura:
            accidents(Map): Corresponde a la informacion completa de los accidentes
            dateIndex(OrderedMap): Corresponde a un indice con los ids de los accidentes organizados por fecha
                severity(Map): Contiene la informacion dividida por severidad
                    timeIndex(OrderedMap): Organiza la informacion por hora
                        idList(List): Contiene los Ids 

        Retorna:
            dict: Corresponde al analizador inicializado.
    """
    dataBase = {
                'accidents': m.newMap(878756,109345121,'CHAINING',1.5,compareIds),
                'dateIndex': om.newMap('RBT',compareDates)
                }

    return dataBase

def newSeverity()->dict:
    """
    Crea una entrada en el indice de fechas.
        parametros:
            None
        retorna:
            Map: Esta entrada divide los accidentes por severidad.
    """

    dateEntry = m.newMap(4,7,'CHAINING',1.5,compareSeverities)
    return dateEntry

def newTimeIndex()->dict: 
    """
    Crea un indice de tiempo.
        parametros:
            None
        retorna:
            OrderMap: Esta entrada organiza los accidentes segun su hora inicial
    """

    timeIndex = om.newMap('RBT',compareTime)
    return timeIndex

def newIDList()->dict:
    """
    Crea una lista con los ids de los accidentes
        parametros:
            None
        retorna:
            List: Contiene los ids de los accidentes
    """
    idList = lt.newList('ARRAY_LIST', compareIds)
    return idList


# ==============================
# Funciones de Actualizacion
# ==============================


def updateDataBase(dataBase:dict, accident:dict)->None:
    """
        Añade un accidente a la base de datos
    Parametros:
        dataBase(dict): Representa a la base de datos
        accident(dict): Contiene los detalles acerca de un unico accidente
    Retorna:
        None
    """
    updateAccidents(dataBase['accidents'], accident)
    updateDateIndex(dataBase['dateIndex'], accident)
   
def updateAccidents(accidentsMap:dict, accident:dict):
    m.put(accidentsMap,accident['ID'], accident)

def updateDateIndex(dateMap:dict, accident:dict)->None:
    """
    Añade la informacion del accidente al indice de fechas de la base de datos
        parametros: 
            map(dict): Es el indice de fechas de la base de datos
            accident(dict): Contiene los detalles de un unico accidente
        Retorno:
            None
    """
   
    start_time = accident['Start_Time']
    accidentDate = datetime.datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')

    entryExist = om.contains(dateMap,accidentDate.date())

    if entryExist:
        dateEntry = om.get(dateMap,accidentDate.date())
        dateEntry = me.getValue(dateEntry)
    else:
        dateEntry = newSeverity()
        om.put(dateMap, accidentDate.date(), dateEntry)

    updateSeverity(dateEntry, accident, accidentDate)

def updateSeverity(dateEntry:dict, accident:dict, accidentDate: datetime)->None:
    """
    Actualiza las entradas Severity de la base de datos
        parametros:
            dateEntry(Map): Es la entrada que contiene los datos de severidad
            accident(dict): Contiene toda la informacion del accidente
        retorna:
            None
    """
    severity = accident['Severity']

    entryExist = m.contains(dateEntry, severity)
    if entryExist:
        severityEntry = m.get(dateEntry, severity)
        severityEntry = me.getValue(severityEntry)
    else:
        severityEntry = newTimeIndex()
        m.put(dateEntry, severity, severityEntry)

    updateTimeIndex(severityEntry,accident,accidentDate)

     


def updateTimeIndex(severityEntry:dict, accident:dict,accidentDate: datetime)->None:
    """
    Actualiza las entradas del indice Time.
        parametros:
            severityEntry(OrderedMap): Contiene un TimeIndex
            accident(dict): Contiene la informacion acerca del accidente

    """
    id = accident['ID']
    accidentTime = blockTime(accidentDate.time())

    entryExist = om.contains(severityEntry,accidentTime)
    if entryExist:
        timeEntry = om.get(severityEntry, accidentTime)
        timeEntry = me.getValue(timeEntry)
    else:
        timeEntry = newIDList()
        om.put(severityEntry,accidentTime,timeEntry)
    
    lt.addFirst(timeEntry,id)
        

# ==============================
# Funciones de consulta
# ==============================


def accidentSize(analyzer):
   
    return lt.size(analyzer['accidents'])


def indexHeight(analyzer):
    
    return om.height(analyzer['dateIndex'])


def indexSize(analyzer):
    
    return om.size(analyzer['dateIndex'])


def minKey(analyzer):
    
    return om.minKey(analyzer['dateIndex'])


def maxKey(analyzer):
   
    return om.maxKey(analyzer['dateIndex'])
    


def getAccidentsBySeverity(analyzer, initialDate, severity):
    accidentdate = om.get(analyzer['dateIndex'], initialDate)
    if accidentdate['key'] is not None:
        severitymap = me.getValue(accidentdate)['severityIndex']
        numseverities = m.get(severitymap, severity)
        if numseverities is not None:
            return m.size(me.getValue(numseverities)['lstseverities'])
        return 0

    

# ==============================
# Funciones de Comparacion
# ==============================


def compareIds(id1, id2):
    """
    Compara dos accidentes
    """
    id2 = me.getKey(id2)
    
    if (id1 == id2):
        return 0
    elif id1 > id2:
        return 1
    else:
        return -1


def compareDates(date1, date2):
    if (date1 == date2):
        return 0
    elif (date1 > date2):
        return 1
    else:
        return -1

def compareTime(time1, time2):
    if (time1 == time2):
        return 0
    elif (time1 > time2):
        return 1
    else:
        return -1


def compareSeverities(severity1, severity2):
    severity2 = me.getKey(severity2)
    if (severity1 == severity2):
        return 0
    elif (severity1 > severity2):
        return 1
    else:
        return -1
 

# ==============================
# Funciones auxiliares
# ==============================

def blockTime(accidentTime: datetime.time) -> datetime.time:
    """
    Define una entrada horaria en un bloque de media hora.
        Nota:
            Cada bloque abarca desde la hora retornada hasta 30 minutos despues
        parametros:
            accidentTime(Time): contiene la hora inicial del accidente
        retorna:
            time: Contiene la hora inicial del bloque al que fue asignado
    """
    if accidentTime.minute < 30:
        return datetime.time(hour=accidentTime.hour,minute=0)
    else:
        return datetime.time(hour=accidentTime.hour,minute=30)

