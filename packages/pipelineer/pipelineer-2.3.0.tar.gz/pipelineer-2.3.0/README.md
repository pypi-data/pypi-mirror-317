![Alt text for the image](img/pipelineer_80x80.jpg)

# **Pipelineer** - Generador de Esquemas Avro, JSON, SQL y Tablas BigQuery

Pipelineer es una herramienta diseñada para automatizar la creación de:

- Esquemas en formato **Avro**, **JSON**, y **SQL** desde definiciones de tablas Oracle.
- **Scripts de tablas** en BigQuery con soporte para particiones, clustering y etiquetas (`labels`).
- **Procedimientos almacenados (MERGE)** para sincronizar datos entre tablas `staging` y `depure`.




## **Instalación**

1. Clona tu repositorio:
   ```bash
   git clone https://github.com/tu-repo/tu-repo.git
   ```
2. Instala las dependencias:
   ```bash
   pip install pipelineer
   ```

---

## **Comandos Disponibles**

Pipelineer organiza sus funcionalidades en subcomandos bajo el comando principal `make`.

### **1. `make template`**

Configura plantillas necesarias para trabajar con DAGs. Sobrescribe el contenido de un archivo con prefijo `dag_` en la raíz del proyecto utilizando una plantilla predefinida.

#### **Uso**
```bash
pipelineer make template --type {oracle|api}
```

#### **Argumentos**
| Argumento | Descripción                                      | Opciones       | Obligatorio |
|-----------|--------------------------------------------------|----------------|-------------|
| `--type`  | Especifica el tipo de plantilla a utilizar.      | `oracle`, `api`| Sí          |

#### **Ejemplo**
```bash
pipelineer make template --type oracle
```

---

### **2. `make schemas`**

Genera esquemas en formato Avro, JSON y SQL a partir de definiciones de tablas Oracle.

#### **Uso**
```bash
pipelineer make schemas
```

#### **Argumentos**
| Argumento              | Descripción                                     | Predeterminado       | Opciones           |
|------------------------|-------------------------------------------------|----------------------|--------------------|
| `--input-folder`       | Carpeta con los archivos `.sql`.                | `schemas/oracle`     | N/A                |
| `--avro-output-folder` | Carpeta de salida para los archivos Avro.       | `schemas/avsc`       | N/A                |
| `--json-output-folder` | Carpeta de salida para los archivos JSON.       | `schemas/json`       | N/A                |
| `--sql-output-folder`  | Carpeta de salida para los archivos SQL.        | `sql/oracle`         | N/A                |
| `--date-format`        | Formato de las fechas.                          | `datetime`           | `date`, `datetime` |

#### **Ejemplo**
```bash
pipelineer make schemas --input-folder schemas/oracle --date-format date
```

---

### **3. `make bq_tables`**

Genera scripts de creación de tablas en BigQuery basados en configuraciones definidas en archivos JSON.

#### **Uso**
```bash
pipelineer make bq_tables
```

#### **Argumentos**
| Argumento              | Descripción                                      | Predeterminado                    | Opcional |
|------------------------|--------------------------------------------------|-----------------------------------|----------|
| `--config-folder`      | Carpeta con los archivos de configuración JSON.  | `sql/bigquery/config/`           | Sí       |
| `--config-file`        | Ruta de un archivo de configuración específico.  | N/A                               | Sí       |
| `--output-folder`      | Carpeta de salida para los scripts generados.    | `sql/bigquery/scripts/create_table/` | Sí       |

#### **Ejemplo**
Generar scripts para todas las tablas:
```bash
pipelineer make bq_tables
```

Generar un script para una tabla específica:
```bash
pipelineer make bq_tables --config-file sql/bigquery/config/cob_compro.json
```

---

### **4. `make bq_store_procedures`**

Genera procedimientos almacenados para operaciones de `MERGE` en BigQuery.

#### **Uso**
```bash
pipelineer make bq_store_procedures
```

#### **Argumentos**
| Argumento              | Descripción                                      | Predeterminado                    | Opcional |
|------------------------|--------------------------------------------------|-----------------------------------|----------|
| `--config-folder`      | Carpeta con los archivos de configuración JSON.  | `sql/bigquery/config/`           | Sí       |
| `--output-folder`      | Carpeta de salida para los procedimientos generados. | `sql/scripts/store_procedure/` | Sí       |

#### **Ejemplo**
```bash
pipelineer make bq_store_procedures
```

---

## **Archivo de Configuración**

Un archivo JSON define los parámetros necesarios para generar scripts de tablas y procedimientos.

```json
{
  "table_name": "TABLE_NAME",
  "zone": ["stg", "dep"],
  "partition_field": "date_column",
  "partition_type": "DAY",
  "partition_data_type": "DATE",
  "clustering_fields": ["field1", "field2"],
  "date_field_type": "DATETIME",
  "dataset": "dataset_name",
  "labels": [
    {"key": "origen", "value": "menu_andes"},
    {"key": "ambiente", "value": "dev"}
  ],
  "merge_fields": ["ccr_codigo", "cpa_caja"]
}
```

### **Descripción de los Campos**
| Campo                 | Descripción                                                                             | Obligatorio | Ejemplo                      |
|-----------------------|-----------------------------------------------------------------------------------------|-------------|------------------------------|
| `table_name`          | Nombre de la tabla en formato Oracle (mayúsculas).                                      | Sí          | `"COB_COMPRO"`              |
| `zone`                | Zonas donde se crearán las tablas (`stg`, `dep`, etc.).                                 | Sí          | `["stg", "dep"]`            |
| `partition_field`     | Campo usado para partición.                                                             | No          | `"pla_fecven"`              |
| `partition_type`      | Tipo de partición (`DAY`, `MONTH`, `YEAR`).                                             | No          | `"MONTH"`                   |
| `partition_data_type` | Tipo de dato del campo de partición (`DATE`, `DATETIME`, `TIMESTAMP`).                  | No          | `"DATETIME"`                |
| `clustering_fields`   | Lista de campos usados para clustering.                                                | No          | `["cpa_codigo", "emp_rut"]` |
| `date_field_type`     | Tipo de dato para columnas de fecha (`DATE`, `DATETIME`, `TIMESTAMP`).                  | No          | `"DATETIME"`                |
| `dataset`             | Nombre del dataset destino en BigQuery para tablas `dep`.                              | Sí          | `"finance_data"`            |
| `labels`              | Lista de etiquetas clave-valor para identificar el origen y ambiente de datos.          | Sí          | `[{"key": "origen", "value": "menu_andes"}]` |
| `merge_fields`        | Campos clave usados en la cláusula `ON` del procedimiento almacenado.                   | No          | `["ccr_codigo", "cpa_caja"]`|

---

## **Flujo Recomendado**

1. Configura la plantilla:
   ```bash
   pipelineer make template --type oracle
   ```

2. Genera los esquemas:
   ```bash
   pipelineer make schemas
   ```

3. Crea las tablas en BigQuery:
   ```bash
   pipelineer make bq_tables
   ```

4. Genera procedimientos almacenados:
   ```bash
   pipelineer make bq_store_procedures
   ```

---

## **Contribuciones**

¡Se aceptan contribuciones! Si encuentras un problema o tienes sugerencias, por favor abre un **issue** o envía un **pull request**.

---

## **Licencia**

Este proyecto está bajo la licencia MIT.
```

