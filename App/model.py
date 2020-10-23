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
                'accidents': m.newMap(878756,878777,'CHAINING',1.5,compareIds),
                'dateIndex': om.newMap('RBT',compareDates),
                'size': 0
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

    dateEntry = {
        'severityIndex':m.newMap(4,7,'CHAINING',1.5,compareSeverities),
        'size':0
        }
    return dateEntry

def newTimeIndex()->dict: 
    """
    Crea un indice de tiempo.
        parametros:
            None
        retorna:
            OrderMap: Esta entrada organiza los accidentes segun su hora inicial
    """

    timeIndex = {
        'timeIndex':om.newMap('RBT',compareTime),
        'size': 0
        }
    return timeIndex

def newIDList()->dict:
    """
    Crea una lista con los ids de los accidentes
        parametros:
            None
        retorna:
            List: Contiene los ids de los accidentes
    """
    idList = {
        'idList': lt.newList('ARRAY_LIST', compareIds),
        'size': 0
        }
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
    updateAccidents(dataBase, accident)
    updateDateIndex(dataBase['dateIndex'], accident)
   
def updateAccidents(dataBase:dict, accident:dict):
    m.put(dataBase['accidents'],accident['ID'], accident)
    dataBase['size'] += 1


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

    updateSeverity(dateEntry['severityIndex'], accident, accidentDate)
    dateEntry['size'] += 1


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

    updateTimeIndex(severityEntry['timeIndex'],accident,accidentDate)
    severityEntry['size'] += 1
     


def updateTimeIndex(severityEntry:dict, accident:dict,accidentDate: datetime, )->None:
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
    
    lt.addFirst(timeEntry['idList'],id)
    timeEntry['size'] += 1
        

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
 
def getSeverityByDate (dataBase, date):
    data = getDataSeverity(getIndex(dataBase,date),dataBase)
    return data


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

def getIndex(dataBase, initialDate, finalDate=None):
    indexDate = dataBase['dateIndex']
    index = lt.newList()
    if finalDate is None:
        indexExist = om.contains(indexDate,initialDate)
        if indexExist:
            element = om.get(indexDate,initialDate)
            element = me.getValue(element)
            lt.addFirst(index,element)
    else:
        pass

    return index

def getDataSeverity (index, dataBase):
    severityMap = newSeverity()
    entry1 = lt.size(index)
    while entry1 > 0:
        entry1 -= 1

        dateEntry = lt.removeFirst(index)
        dateKeys = m.keySet(dateEntry['severityIndex'])
        severityMap['size'] += dateEntry['size']
        
        entry2 = lt.size(dateKeys)
        while entry2 > 0:
            entry2 -= 1
            severityKey = lt.removeFirst(dateKeys)
            if severityKey is not None:
                severityEntry = m.get(dateEntry['severityIndex'],severityKey)
                severityEntry = me.getValue(severityEntry)
                
                m.put(severityMap['severityIndex'],severityKey, severityEntry['size'])
            
    return severityMap
                
def getDataTime (timeLo, timeHi, dataBase):
    severityMap = newSeverity()
    index = om.valueSet(dataBase['dateIndex'])
    entry1 = lt.size(index)
    while entry1 > 0:
        entry1 -= 1

        dateEntry = lt.removeFirst(index)
        dateKeys = m.keySet(dateEntry)
        
        entry2 = lt.size(dateKeys)
        while entry2 > 0:
            entry2 -= 1
            severityKey = lt.removeFirst(dateKeys)
            severityEntry = m.get(dateEntry,severityKey)
            severityEntry = me.getValue(severityEntry)
            severityEntry = om.values(dateEntry,timeLo,timeHi)
            
            entry3 = lt.size(severityEntry)
            while entry3 > 0:
                entry3 -= 1
                timeEntry = lt.removeFirst(severityEntry)
                entry4 = lt.size(timeEntry)
                while entry4 > 0:
                    entry4 -= 1
                    idEntry = lt.removeFirst(timeEntry)
                    idEntry = getAccident(dataBase, idEntry)

                    lt.addFirst(severityList,idEntry)
                    
            m.put(severityMap, severityKey, severityList)
    return severityMap
                


def getAccident(dataBase, id):
    accident = m.get(dataBase['accidents'], id)
    accident = me.getValue(accident)
    return accident