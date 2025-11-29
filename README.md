# consulta-precios-omie

Script en Python para descargar y consultar los precios del mercado diario OMIE a partir de los ficheros oficiales `marginalpdbc_YYYYMMDD.1`.  
El script obtiene los datos de **ayer** y **hoy**, los procesa y los muestra por pantalla en formato JSON.

Actualmente el script:

- Descarga el fichero `marginalpdbc_YYYYMMDD.1` de OMIE para **ayer**.
- Descarga el fichero `marginalpdbc_YYYYMMDD.1` de OMIE para **hoy**.
- Parsea las líneas relevantes del fichero.
- Muestra una lista JSON con:
  - `fecha` (en formato ISO 8601, UTC)
  - `precio_espana` (precio correspondiente a España, value2 en el fichero original)

El fichero principal del proyecto es `omie.py`.

## Requisitos

- Python 3.8 o superior
- Acceso a internet

### Librerías de Python

Las dependencias se gestionan con `pip` mediante `requirements.txt`:

- `requests`

## Instalación

1. Clona el repositorio:

   ```bash
   git clone https://github.com/tu-usuario/consulta-precios-omie.git
   cd consulta-precios-omie
   ```

2. (Opcional pero recomendado) Crea y activa un entorno virtual:

   ```bash
   python -m venv venv
   # En Linux / macOS
   source venv/bin/activate
   # En Windows
   venv\Scripts\activate
   ```

3. Instala las dependencias:

   ```bash
   pip install -r requirements.txt
   ```

## Uso

Dentro de la carpeta del proyecto, ejecuta:

```bash
python omie.py
```

Por defecto, el script:

- Calcula las fechas de **ayer** y **hoy**.
- Descarga los ficheros `marginalpdbc_YYYYMMDD.1` correspondientes a esas fechas.
- Parsea los datos de cada fichero.
- Imprime por pantalla, para cada día, una lista JSON con la fecha y el precio de España (`precio_espana`).

Ejemplo de salida (simplificado):

```json
[
  {
    "fecha": "2025-01-01T00:00:00.000000+0000",
    "precio_espana": 80.5
  },
  {
    "fecha": "2025-01-01T01:00:00.000000+0000",
    "precio_espana": 78.3
  }
]
```

## Personalización de las fechas

Si quieres cambiar las fechas que se consultan (por ejemplo, solo un día concreto o un rango diferente), puedes editar la función `main()` en `omie.py`:

```python
from datetime import datetime, timedelta

def main():
    # Ejemplo: consultar solo un día concreto
    fecha_concreta = datetime(2025, 1, 1).date()

    for etiqueta, fecha in (("DIA_CONCRETO", fecha_concreta),):
        print(f"\n================= DATOS OMIE {etiqueta} ({fecha}) =================")
        contenido = descargar_fichero_omie(fecha)
        if contenido is None:
            print("No se pudieron obtener datos para esta fecha.")
            continue

        registros = parsear_omie(contenido)
        print(json.dumps(registros, indent=2, ensure_ascii=False))
```

Modifica las fechas según tus necesidades y vuelve a ejecutar:

```bash
python omie.py
```

## Estructura del proyecto

```text
consulta-precios-omie/
├── omie.py            # Script principal
├── requirements.txt   # Dependencias del proyecto
└── README.md          # Este archivo
```

## Notas

- El script se basa en el formato actual de los ficheros `marginalpdbc_YYYYMMDD.1` publicados por OMIE. Si el formato cambia, puede ser necesario adaptar el parseo.
