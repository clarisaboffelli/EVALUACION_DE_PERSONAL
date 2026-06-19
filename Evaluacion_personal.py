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

import csv
import sys
from enum import Enum


def cargar_resultados_evaluacion(ruta_csv="Resultados_evaluacion.csv"):
    """
    Lee el archivo Resultados_evaluacion.csv y devuelve un diccionario por legajo.

    Parametros:
        ruta_csv (str): Ruta del archivo CSV que contiene los resultados de evaluación.
    Retorna:
        resultados (dict): Diccionario con la información de los empleados evaluados.
    """
    resultados = {}

    try:
        with open(ruta_csv, encoding="utf-8", newline="") as archivo:
            lector = csv.reader(archivo, delimiter=";")
            for linea_num, fila in enumerate(lector, start=1):
                if not fila or len(fila) < 3:
                    continue

                legajo = fila[0].strip()
                nombre = fila[1].strip()
                puntuacion_texto = fila[2].strip()

                if not legajo:
                    continue

                try:
                    puntuacion = int(puntuacion_texto)
                except ValueError:
                    try:
                        puntuacion = float(puntuacion_texto)
                    except ValueError:
                        puntuacion = puntuacion_texto

                resultados[legajo] = {
                    "nombre": nombre,
                    "puntuacion": puntuacion,
                }

    except FileNotFoundError:
        print(f"No se encontró el archivo: {ruta_csv}")
    except PermissionError:
        print(f"No se puede acceder al archivo: {ruta_csv}")
    except Exception as error:
        print(f"Error al procesar {ruta_csv}: {error}")

    return resultados

def cargar_fechas_capacitacion(ruta_csv="Fechas_capacitacion.csv"):
    """
    Lee el archivo Fechas_capacitacion.csv y devuelve una lista de fechas de capacitación.

    Parametros:
        ruta_csv (str): Ruta del archivo CSV que contiene las fechas de capacitación.
    Retorna:
        fechas (list): Lista con la información de las capacitaciones.
    """
    fechas = []

    try:
        with open(ruta_csv, encoding="utf-8", newline="") as archivo:
            lector = csv.reader(archivo, delimiter=";")
            for linea_num, fila in enumerate(lector, start=1):
                if not fila or len(fila) < 4:
                    continue

                fecha = fila[0].strip()
                hora = fila[1].strip()
                lugar = fila[2].strip()
                cupos_texto = fila[3].strip()

                if not fecha:
                    continue

                try:
                    cupos = int(cupos_texto)
                except ValueError:
                    continue

                fechas.append({
                    "fecha": fecha,
                    "hora": hora,
                    "lugar": lugar,
                    "cupos": cupos,
                })

    except FileNotFoundError:
        print(f"No se encontró el archivo: {ruta_csv}")
    except PermissionError:
        print(f"No se puede acceder al archivo: {ruta_csv}")
    except Exception as error:
        print(f"Error al procesar {ruta_csv}: {error}")

    return fechas


def resultado_por_legajo(resultados):
    """
    Pide el legajo del usuario, comprueba si existe en resultados y mantiene el programa en ejecución
    hasta que se ingrese un legajo registrado o el usuario elija finalizar.

    Parametros:
        resultados (dict): Diccionario de resultados por legajo.
    
    Retorna:
        puntuacion (int/float/str): Puntuación obtenida por el usuario, o None si se finaliza el programa.
    """
    while True:
        legajo = input("\nIngrese su número de legajo (* para salir): ").strip()
        if not legajo:
            print("\nEl legajo no puede estar vacío.")
            continue

        if legajo == "*":
            print("\nFinalizando el programa.")
            return

        if not legajo.isdigit():
            print("\nEl legajo no puede contener letras ni caracteres no numéricos.")
            continue

        registro = resultados.get(legajo)
        if registro is None:
            print("\nEl legajo no se encuentra en los resultados. Inténtelo de nuevo o ingrese * para salir.")
            continue

        nombre = registro.get("nombre")
        puntuacion = registro.get("puntuacion")
        print(f"\nUsuario: {nombre}")
        print(f"\nPuntuación en la evaluación de personal: {puntuacion}")
        return puntuacion


class EstadoEvaluacion(Enum):
    SUFICIENTE = "SUFICIENTE"
    INSUFICIENTE = "INSUFICIENTE"


PUNTUACION = 6


def pedir_conformidad_insuficiente():
    """Solicita conformidad para el estado insuficiente y devuelve True/False."""
    opciones_validas = {
        "SI": True,
        "S": True,
        "NO": False,
        "N": False,
    }

    while True:
        respuesta = input("\n¿Está conforme con el resultado? (Si/No): ").strip().upper()
        if respuesta in opciones_validas:
            return opciones_validas[respuesta]
        print("Respuesta inválida. Ingrese Si o No.")


def evaluar_estado_puntuacion(puntuacion):
    """Evalúa la puntuación y maneja los estados SUFICIENTE e INSUFICIENTE."""
    if not isinstance(puntuacion, (int, float)):
        print("Puntuación inválida. No se puede determinar el estado.")
        return None, None

    if puntuacion >= PUNTUACION:
        estado = EstadoEvaluacion.SUFICIENTE
    else:
        estado = EstadoEvaluacion.INSUFICIENTE

    if estado == EstadoEvaluacion.SUFICIENTE:
        print("\nAprobó la evaluación de personal. Su compromiso con el crecimiento de esta empresa es altamente valorado.\nRecibirá una bonificación económica en su próxima liquidación.")
        sys.exit(0)

    conformidad = pedir_conformidad_insuficiente()
    return estado, conformidad


def evaluar_resultado_por_legajo(resultados):
    """Obtiene la puntuación por legajo y aplica la máquina de estados de evaluación."""
    puntuacion = resultado_por_legajo(resultados)
    if puntuacion is None:
        return None, None

    return evaluar_estado_puntuacion(puntuacion)


def mostrar_opciones_capacitacion(fechas):
    if not fechas:
        print("\nNo hay capacitaciones disponibles en este momento.")
        return
    print("\nDebido a que su evaluación de desempeño rebeló algunas carencias, ponemos a su disposición las siguientes capacitaciones que le aydarán a mejorar su desempeño.")
    print("\nCapacitaciones disponibles:")
    for indice, opcion in enumerate(fechas, start=1):
        estado_cupos = opcion["cupos"] if isinstance(opcion["cupos"], int) else "N/A"
        print(
            f"{indice}. Fecha: {opcion['fecha']} | Hora: {opcion['hora']} | Lugar: {opcion['lugar']} | Cupos: {estado_cupos}"
        )


def confirmar_seleccion():
    opciones_validas = {
        "SI": True,
        "S": True,
        "NO": False,
        "N": False,
    }

    while True:
        respuesta = input("\nConfirma esta seleccion? (Si/No): ").strip().upper()
        if respuesta in opciones_validas:
            return opciones_validas[respuesta]
        print("Respuesta inválida. Ingrese Si o No.")


def seleccionar_capacitacion(fechas):
    if not fechas:
        return None

    while True:
        mostrar_opciones_capacitacion(fechas)
        seleccion = input("\nIngrese el número de la capacitación que desea elegir (* para cancelar): ").strip()
        if seleccion == "*":
            print("\nSelección cancelada.")
            return None

        if not seleccion.isdigit():
            print("Entrada inválida. Ingrese un número válido.")
            continue

        indice = int(seleccion) - 1
        if indice < 0 or indice >= len(fechas):
            print("Número de capacitación inválido. Intente nuevamente.")
            continue

        opcion = fechas[indice]
        if not isinstance(opcion["cupos"], int) or opcion["cupos"] <= 0:
            print("La capacitación seleccionada no tiene cupos disponibles. Elija otra opción.")
            continue

        print(
            f"\nSeleccionó:\n Fecha: {opcion['fecha']}\n Hora: {opcion['hora']}\n Lugar: {opcion['lugar']}\n Cupos disponibles: {opcion['cupos']}"
        )

        if confirmar_seleccion():
            opcion["cupos"] -= 1
            print(
                f"\nReserva confirmada. Cupos restantes para esta capacitación: {opcion['cupos']}"
            )
            return opcion

        print("\nNo se confirmó la selección. Puede elegir otra capacitación o cancelar.")


# PROGRAMA PRINCIPAL-----------------------------------------------

resultados = cargar_resultados_evaluacion()
fechas_capacitacion = cargar_fechas_capacitacion()
print("EVALUACION DE PERSONAL - MAINTECH.SA")
print("Bienvenido al sistema de notificaciones de MAINTECH.SA")

estado, conformidad = evaluar_resultado_por_legajo(resultados)
if estado == EstadoEvaluacion.INSUFICIENTE:
    if conformidad:
        seleccion = seleccionar_capacitacion(fechas_capacitacion)
        if seleccion is not None:
            print(
                f"\nSeleccion confirmada: Fecha {seleccion['fecha']}, Hora {seleccion['hora']}, Lugar {seleccion['lugar']}. "
                f"Se ha reducido el cupo disponible a {seleccion['cupos']}"
            )
    else:
        print("\nLos resultados de la evaluación de personal no te parecen aceptables. Por favor, comunicate con RRHH para una saber como seguir con el procedimiento.")