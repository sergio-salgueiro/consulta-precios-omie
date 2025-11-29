import json
import requests
from datetime import datetime, date, timezone, timedelta


# -------------------------------------------------------------------
# Funciones auxiliares
# -------------------------------------------------------------------

def formatear_fecha_hora(year: int, month: int, day: int, hour: int) -> str:
    """
    Recibe año, mes, día y hora (de 1 a 24) y devuelve una cadena
    con la fecha/hora en formato ISO 8601 con zona horaria UTC.

    En los ficheros de OMIE la hora 24 se considera las 00:00 del día siguiente,
    así que aquí hacemos esa conversión.
    """
    if hour == 24:
        hour = 0
        fecha = datetime(year, month, day, hour, tzinfo=timezone.utc) + timedelta(days=1)
    else:
        fecha = datetime(year, month, day, hour, tzinfo=timezone.utc)

    return fecha.strftime("%Y-%m-%dT%H:%M:%S.%f%z")


def descargar_fichero_omie(fecha: date) -> str | None:
    """
    Descarga el fichero marginalpdbc_YYYYMMDD.1 de OMIE para la fecha indicada.
    Devuelve el contenido del fichero como texto o None si hay error.
    """
    fecha_str = fecha.strftime("%Y%m%d")
    url = (
        "https://www.omie.es/es/file-download"
        "?parents%5B0%5D=marginalpdbc"
        f"&filename=marginalpdbc_{fecha_str}.1"
    )

    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.text
        else:
            print(f"Error en la descarga para {fecha_str}. Código de estado: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error de conexión al descargar el fichero para {fecha_str}: {e}")
        return None


def parsear_omie(contenido: str) -> list[dict]:
    """
    Parsea el contenido de un fichero OMIE (marginalpdbc_*.1).

    Devuelve una lista de diccionarios con:
    - fecha (ISO 8601)
    - precio_espana (value2 en el fichero original)
    """
    lineas = contenido.splitlines()
    registros = []

    for linea in lineas:
        values = linea.split(";")

        if len(values) == 7:
            try:
                year, month, day, hour, value1, value2 = map(float, values[:-1])
                fecha_iso = formatear_fecha_hora(int(year), int(month), int(day), int(hour))

                registros.append(
                    {
                        "fecha": fecha_iso,
                        "precio_espana": value2
                    }
                )
            except ValueError:
                continue

    return registros


# -------------------------------------------------------------------
# Punto de entrada del script
# -------------------------------------------------------------------

def main():
    """
    Define las fechas que se van a consultar y llama a las funciones de descarga y parseo.

    Ahora mismo está configurado para obtener los datos de OMIE de:
      - AYER (día completo)
      - HOY (día completo)

    Es decir, se descargan dos ficheros:
      - marginalpdbc_YYYYMMDD.1 correspondiente a ayer
      - marginalpdbc_YYYYMMDD.1 correspondiente a hoy

    Puedes cambiar estas fechas a las que quieras modificando las variables `ayer` y `hoy`.
    """
    # Fecha y hora actuales
    ahora = datetime.now()

    # Día de hoy (solo la parte de fecha, sin hora)
    hoy = ahora.date()

    # Día de ayer: restamos 1 día a la fecha actual
    ayer = (ahora - timedelta(days=1)).date()

    # Recorremos las dos fechas que queremos consultar: AYER y HOY
    for etiqueta, fecha in (("AYER", ayer), ("HOY", hoy)):
        print(f"\n================= DATOS OMIE {etiqueta} ({fecha}) =================")

        # Descargamos el fichero marginalpdbc_YYYYMMDD.1 para la fecha indicada
        contenido = descargar_fichero_omie(fecha)
        if contenido is None:
            print("No se pudieron obtener datos para esta fecha.")
            continue

        # Parseamos el contenido del fichero a una lista de registros (fecha + precio_espana)
        registros = parsear_omie(contenido)

        # Imprimimos el resultado como JSON formateado
        print(json.dumps(registros, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
