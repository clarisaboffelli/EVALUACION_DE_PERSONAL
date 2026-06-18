import csv


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


if __name__ == "__main__":
    resultados = cargar_resultados_evaluacion()
    print(resultados)
