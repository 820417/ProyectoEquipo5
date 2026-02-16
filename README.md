# ProyectoEquipo5

# Proyecto Clean CSV

## Descripción del proyecto

**Proyecto Clean CSV** consiste en un pipeline de lectura, procesamiento y reporte de un fichero CSV que incluye validación, limpieza y transformación de datos. Está diseñado para manejar archivos CSV de cualquier tamaño

### Características Principales

**Arquitectura**
- Selección automática de tipo de lectura del archivo según su tamaño
- Sistema de logging detallado
- Configuración externa mediante JSON
- Testing

**Validación**
- Detección de valores nulos
- Identificación de registros duplicados
- Verificación de tipos de datos

**Limpieza**
- Eliminación de duplicados configurable
- Imputación de valores numéricos basados en relaciones matemáticas entre columnas
- Relleno de valores nulos según estrategia definida
- Conversión automática de tipos de datos

**Transformaciones**
- Cálculo del trimistre anual en base a la fecha
- Cálculo del dia de la semana en que se produce la venta
- Clasificación por categoría de los productos vendidos

**Reportes y exportaciones**
- Exportación de CSV limpio
- Generación de gráficos de estadísticas de ventas
- Registro de cambios aplicados durante la limpieza

---

## Arquitectura del Proyecto

```
proyecto_clean_csv/
├── main.py                          # Punto de entrada que llama al orquestador
├── schema_generator.py              # Fichero que genera un esquema de la arquitectura del proyecto
├── pyproject.toml                   # Configuración del proyecto y dependencias
├── examples/                        # Archivos CSV de ejemplo
│   ├── retail_store_sales.csv
│   └── ventas_cafe.csv
├── generated/                       # Carpeta donde se guardan los archivos generados por el pipeline
│   ├── plots/                       # Carpeta para los gráficos generados
├── src/module/
│   ├── cleaners/                    # Módulo de limpieza de datos
│   │   ├── cleaners.py              # Funciones de limpieza
│   │   └── cleaner_dispatcher.py    # Dispatcher para aplicar limpiezas
│   ├── data_models/
│   │   ├── config.json              # Configuración de limpieza
│   │   └── schema.py                # Definición de esquema y constantes
│   ├── pipelines/
│   │   └── orchestrator.py          # Orquestador principal del pipeline
│   ├── read/                        # Módulo de lectura de archivos
│   │   ├── csv_reader_selector.py   # Selector de estrategia de lectura en base al tamaño del archivo
│   │   └── reader.py                # Implementación de los distintos lectores
│   ├── reports/                     # Sistema de reportes y logging
│   │   ├── decorators.py            # Decoradores para tracking
│   │   ├── logging_config.py        # Configuración de logging
│   │   ├── clean_csv_exporter.py    # Función para exportar CSV limpio
│   │   ├── plot_generator.py        # Funciones para generar gráficos
│   │   └── app_log.txt              # Fichero de logs
│   ├── transforms/                  # Transformaciones de datos
│   │   ├── item.py                  # Cálculo de categoría del producto en una nueva columna
│   │   ├── weekday.py               # Cálculo del día de la semana en base a la fecha
│   │   └── year_third.py            # Cálculo del trimestre anual en base a la fecha
│   └── validators/                  # Validadores de datos
│       ├── base_validator.py        # Definicion del protocolo de validación
│       └── specific_validators.py   # Validadores específicos que implementan el protocolo
└── tests/                           # Carpeta en la que se encuentran los tests del proyecto
    └── test_validators.py
```

---

## Flujo del Pipeline

```mermaid
graph TD
    A[CSV Input] --> B[Lector CSV]

    B --> C{Tamaño < 2MB?}
    C -->|Sí| C1[Pandas Reader]
    C -->|No| C2[Generator Reader]

    C1 --> D[Validación]
    C2 --> D

    D --> D1[Null Validator]
    D --> D2[Duplicate Validator]
    D --> D3[Type Validator]

    D1 --> E[Reporte de Errores]
    D2 --> E
    D3 --> E

    E --> F[Cleaner Dispatcher]
    F --> G[Limpieza de Datos]

    G --> H{Errores de Duplicados?}
    H -->|Sí| H1[Eliminar Duplicados]
    H -->|No| I[Conversión de Tipos]
    H1 --> I

    I --> J[Imputación de Valores]
    J --> T[Tratamiento de Nulos]

    T --> K{Nulos en Columnas Críticas?}
    K -->|Sí| K1[Eliminar Filas]
    K -->|No| L{Nulos en Columnas Opcionales?}
    K1 --> L

    L -->|Sí| L1[Rellenar con Valor Definido]
    L -->|No| M[Transformaciones]
    L1 --> M

    M --> M1[Quarter]
    M --> M2[Day of Week]
    M --> M3[Category]

    M1 --> N[Reporte de Cambios]
    M2 --> N
    M3 --> N

    N --> O[DataFrame Limpio]
    O --> P[Exportar CSV Limpio]
    P --> Q[Generar Gráficos]
```

---

### Dependencias

**Principales:**
- python >= 3.11
- pandas >= 3.0.0
- matplotlib>=3.10.8

**Desarrollo:**
- pytest >= 9.0.2
- pytest-cov >= 7.0.0
- ruff >= 0.15.1

---

## Uso

### Ejecución Básica

```bash
python main.py
```

El script ejecutará el pipeline sobre el archivo configurado en `main.py` (por defecto `examples/ventas_cafe.csv`).

## Configuración

El archivo `src/module/data_models/config.json` permite configurar el comportamiento del pipeline:

```json
{
    "validations":{
        "validate_duplicates": true,
        "validate_nulls": true,
        "validate_types": true
    },
    "duplicates": {
        "apply": true,
        "keep": "last",
        "columns": ["Transaction ID"]
    },
    "types": {
        "apply": true
    },
    "imputation": {
        "apply_amounts": true,
        "apply_category": true
    },
    "nulls": {
        "apply": true,
        "fill_value": "NO_PROPORCIONADO",
        "columns": ["Category", "Payment Method"]
    }

}
```

### Parámetros de Configuración

#### Validaciones (`validations`)
- `validate_duplicates` (bool): Activar/desactivar la validación de elementos duplicados
- `validate_nulls` (bool): Activar/desactivar la validación de valores nulos
- `validate_types` (bool): Activar/desactivar la validación de tipos de datos

#### Duplicados (`duplicates`)
- `apply` (bool): Activar/desactivar eliminación de duplicados
- `keep` (str): Estrategia para mantener duplicados
  - `"first"`: Mantener primera ocurrencia
  - `"last"`: Mantener última ocurrencia
  - `false`: Eliminar todas las ocurrencias
- `columns` (list): Columnas para identificar duplicados

#### Conversión de tipos (`types`)
- `apply` (bool): Activar/desactivar la conversión forzada de tipos de datos según el esquema definido en schema.py (fechas, enteros Int64 y decimales Float64).

#### Imputación inteligente (`imputacion`)
- `apply_amounts` (bool): Activar/desactivar el cálculo automático de valores faltantes en columnas numéricas relacionadas (Quantity, Price Per Unit, Total Spent).
- `apply_category` (bool): Activar/desactivar la deducción de la categoría del producto basada en el mapeo ITEM_TO_CATEGORY.

#### Valores Nulos (`nulls`)
- `apply` (bool): Activar/desactivar el relleno de valores nulos para columnas no críticas.
- `fill_value` (any): El valor que se insertará en los huecos (ej. "NO_PROPORCIONADO").
- `columns` (list): Lista específica de columnas donde se permite aplicar el relleno de nulos.

---

## Esquema de Datos

El proyecto maneja datos con el siguiente esquema (definido en `schema.py`):

| Columna            | Tipo     | Nullable | Descripción                    |
|--------------------|----------|---------|---------------------------------|
| Transaction ID     | str      | No      | Identificador único             |
| Item               | str      | No      | Producto vendido                |
| Quantity           | int      | No      | Cantidad de unidades            |
| Price Per Unit     | float    | No      | Precio unitario                 |
| Total Spent        | float    | No      | Importe total de la transacción |      
| Payment Method     | str      | Si      | Método de pago                  |
| Location           | str      | Si      | Para tomar o para llevar        |
| Transaction Date   | datetime | No      | Fecha de la transacción         |

**Columnas No Nullables**: Si contienen valores nulos después de la imputación, se eliminan las filas completas.

**Columnas Opcionales**: Los valores nulos se rellenan con el valor configurado.

---

### Estructura de Tests

El proyecto incluye tests para:
- Lectura (get_csv_reader, ReaderCSVPandas y ReaderCSVGenerator)
- Validadores (NULL_VALUES, DUPLICATED_VALUES, TYPE_ERROR)
- Limpiadores (remove_duplicate, fill_null, impute_amounts, drop_null, apply_schema_types)
- Transformadores
- Exportación del csv

---

## Funcionalidades

### 1. Lectura de CSV
Se selecciona automáticamente la implementación de lectura según el tamaño del archivo:
- **< 2 MB**: Se utiliza ReaderCSVPandas para cargar el archivo completo en memoria.
- **≥ 2 MB**: Se utiliza ReaderCSVGenerator, que lee fila a fila el archivo y luego construye el DataFrame.


### 2. Validación de Datos

#### - NullValidator
Detecta si hay valores nulos en cualquier columna del DataFrame y, en caso de haber, devuelve un diccionario con las columnas que contienen nulos y el tipo de error NULL_VALUES_ERROR.

#### - DuplicateValidator
Identifica registros duplicados basándose en la columna `Transaction ID` y, en caso de haber, lo indica en el diccionario de errores con el tipo DUPLICATED_VALUES_ERROR.

#### - TypeValidator
Verifica que las columnas tengan los tipos de datos correctos según el esquema. Las columnas que no cumplen con el tipo esperado se reportan en el diccionario de errores con el tipo TYPE_ERROR.


### 3. Limpieza de Datos

#### Eliminación de Duplicados
Elimina las filas duplicadas identificadas en el DataFrame basándose en una columna clave como Transaction ID. 
La estrategia de conservación se controla dinámicamente mediante el archivo de configuración.

#### Conversión de tipos de datos
Estandariza los tipos de datos de las columnas identificadas en el DataFrame basándose en las reglas del esquema del proyecto "schema.py". 
Transforma textos en formatos de fecha correctos y aplica tipos numéricos de Pandas Int64 y Float64 que permiten operar matemáticamente sin fallar cuando existen valores nulos.

#### Imputación de valores numéricos basados en relaciones matemáticas entre columnas
Rescata datos faltantes evaluando la relación lógica entre las columnas Quantity, Price Per Unit y Total Spent. 
Si una de estas métricas está vacía, el sistema calcula y rellena el hueco automáticamente utilizando los valores disponiblels en las otras dos.

#### Manejo de Valores Nulos
Aplica una estrategia de resolución de nulos en dos fases, dirigida por el orquestador:
1. Eliminación crítica: Borra del registro aquellas filas que contienen valores nulos o textos inválidos como "UNKNOWN", en columnas definidas como innegociables (CRITICAL_COLUMNS).
2. Relleno opcional: Sustituye los vacíos restantes en las columnas no críticas autorizadas con un valor por defecto seguro como "NO_PROPORCIONADO", definido en la configuración.


### 4. Transformaciones y cálculos de nuevas columnas

#### Columna "Year Third"
Una vez hecha la limpieza de datos se procede a añadir una columa llamada Year Third en la que se asigna el tercio del año en el cual se da cada venta o transacción, con el fin de poder organizar los datos facilitando el reposting y poder detectar algun tipo de estacionalidad.

#### Columna "Weekday"
Se añade una columna Weekday en la que se asigna el dia de la semana en el que se produjo la venta dada la fecha de la transacción, de esta forma, se puede detrminar si hay dias en el que se producen más ventas o dias en el que caen.

#### Columna "Category"
Se añade una columna llemada Category en la que se agrupan los productos vendidos en dos categorias, permitiendo de este modo identificar que categorias se venden más y generan más ingresos.

### 5. Exportación
- Se exporta un nuevo archivo CSV limpio con las transformaciones aplicadas.
- Crea diferentes gráficos de barras para ver diferentes estadísticas de las ventas.


### 6. Sistema de Logging
- Se genera un reporte detallado de los errores encontrados durante la validación, indicando el tipo de error y las columnas afectadas.
- Además, incorpora mecanismos de seguimiento específicos:

    track_change: Registra automáticamente las modificaciones aplicadas al DataFrame (eliminación de duplicados, imputaciones, relleno de nulos, etc.), permitiendo trazabilidad completa del proceso.

    track_dtype_changes: Detecta y registra cambios en los tipos de datos de las columnas tras la conversión según el esquema definido.

- El resultado es un pipeline totalmente auditable, con un registro detallado de errores y transformaciones en app_log.txt

---

## Herramientas de calidad de código

El proyecto utiliza la herramienta **Ruff** para asegurar la calidad del código, siguiendo los siguientes estándares:

- pycodestyle (errores y warnings)
- pyflakes
- isort
- pep8-naming
- pyupgrade
- Longitud máxima de línea: 100 caracteres
