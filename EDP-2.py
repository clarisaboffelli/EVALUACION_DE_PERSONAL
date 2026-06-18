def cargar_fechas_capacitacion(ruta_csv="Fechas_capacitacion.csv"):
    """
    Lee el archivo Fechas_capacitacion.csv y devuelve un diccionario por fecha de capacitación.

    Parametros:
        ruta_csv (str): Ruta del archivo CSV que contiene las fechas de capacitación.
    Retorna:
        fechas (dict): Diccionario con la información de las capacitaciones por fecha.
    """
    fechas = {}

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
                    cupos = cupos_texto

                fechas[fecha] = {
                    "hora": hora,
                    "lugar": lugar,
                    "cupos": cupos,
                }

    except FileNotFoundError:
        print(f"No se encontró el archivo: {ruta_csv}")
    except PermissionError:
        print(f"No se puede acceder al archivo: {ruta_csv}")
    except Exception as error:
        print(f"Error al procesar {ruta_csv}: {error}")

    return fechas
