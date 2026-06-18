"""
Programa: EVALUACION DE PERSONAL
Descripción: El programa EVALUACIÓN DE PERSONAL permite a los empleados de la empresa MAINTECH.SA consultar los resultados de la evaluación de personal realizada por el responsable de su área. El ingreso al sistema se realiza a través del número de legajo del empleado -compuesto por 4 números- lo que permite al usuario visualizar el puntaje obtenido. Si el puntaje no es suficiente para los estándares buscados, se solicita al usuario la conformidad con dicho resultado. Si da conformidad, el usuario programa la fecha de capacitación. Si no da conformidad, se le solicita que concurra a RRHH para una reunión.
El programa obtiene la información de dos archivos:
Resultados_evaluacion.csv: contiene la información de identificación de los empleados sometidos a evaluación con la estructura legajo;nombre;puntuación. Este archivo es suministrado por el evaluador.
Fechas_capacitacion.csv: contiene la información de las fechas de capacitación y los cupos disponibles organizados con el siguiente orden: fecha;hora;lugar;cupos. Este archivo es suministrado por RRHH.
Autor: Clarisa Boffelli - 
Fecha: 16 de junio de 2026
Versión: 1.0
"""

