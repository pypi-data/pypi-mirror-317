import os
import re
import json
import sys
import importlib.util
from .mappers import map_oracle_to_avro
import oracledb 


def generate_avro_and_mapping(sql_file_path, avro_output_path, json_output_path, sql_output_path, date_format):
    with open(sql_file_path, 'r') as sql_file:
        sql_content = sql_file.read()

    # Limpiar contenido eliminando bloques irrelevantes (constraints, tablespaces, etc.)
    sql_content_cleaned = re.sub(
        r"(CONSTRAINT\s+.*|TABLESPACE\s+.*|SUPPLEMENTAL\s+.*|PCTFREE\s+.*|STORAGE\s+.*|LOGGING\s+.*|ENABLE\s+ROW\s+MOVEMENT\s+.*);?",
        "",
        sql_content,
        flags=re.IGNORECASE | re.MULTILINE
    )

    # Extraer nombre de la tabla
    table_name_match = re.search(r'CREATE TABLE\s+"[^"]+"\."([^"]+)"', sql_content_cleaned, re.IGNORECASE)
    table_name = table_name_match.group(1).lower() if table_name_match else "unknown_table"

    # Extraer columnas válidas
    columns = re.findall(r'"([^"]+)"\s+([A-Z0-9\(\),\s]+)', sql_content_cleaned, re.IGNORECASE)

    # Crear esquema Avro
    avro_schema = {
        "type": "record",
        "name": table_name,
        "fields": []
    }

    # Mapeo JSON
    field_mappings = []
    column_names_types = []

    for column_name, column_type in columns:
        # Evitar columnas inválidas (coincidencia exacta con el nombre de la tabla)
        if column_name.lower() == table_name:
            continue

        # Mapear tipos de Oracle a Avro
        avro_type = map_oracle_to_avro(column_type)

        # Ajustar tipo para JSON
        if isinstance(avro_type, dict) and avro_type.get("logicalType") == "decimal":
            json_type = "numeric"
        elif avro_type == "long":
            json_type = "int"
        else:
            json_type = avro_type

        # Añadir al esquema Avro
        avro_schema["fields"].append({
            "name": column_name.upper(),  # Convención en minúsculas
            "type": ["null", avro_type] if isinstance(avro_type, str) else ["null", avro_type]
        })

        # Añadir al mapeo JSON
        field_mappings.append((column_name.upper(), json_type))

        # Mantener el nombre y tipo original para la consulta SQL
        column_names_types.append((column_name.upper(), column_type.strip().upper()))

    # Guardar esquema Avro
    if not os.path.isdir(avro_output_path):
        os.makedirs(avro_output_path)
    avro_file_path = os.path.join(avro_output_path, f"{table_name}.avsc")
    with open(avro_file_path, 'w') as avro_file:
        json.dump(avro_schema, avro_file, indent=4)

    # Guardar mapeo JSON
    if not os.path.isdir(json_output_path):
        os.makedirs(json_output_path)
    json_file_path = os.path.join(json_output_path, f"{table_name}.json")
    with open(json_file_path, 'w') as json_file:
        json.dump(dict(field_mappings), json_file, indent=4)

    # Generar consulta SQL
    select_columns = []
    for col_name, col_type in column_names_types:
        if col_type.startswith("DATE"):
            format_string = 'YYYY-MM-DD HH24:MI:SS' if date_format == 'datetime' else 'YYYY-MM-DD'
            select_columns.append(f"TO_CHAR({col_name}, '{format_string}') AS {col_name}")
        else:
            select_columns.append(col_name)

    select_columns_str = ",\n    ".join(select_columns)
    sql_query = f"SELECT\n    {select_columns_str}\nFROM\n    {table_name.upper()}\nWHERE\n    ROWNUM <= 100"

    # Guardar consulta SQL
    if not os.path.isdir(sql_output_path):
        os.makedirs(sql_output_path)
    sql_query_file_path = os.path.join(sql_output_path, f"{table_name}.sql")
    with open(sql_query_file_path, 'w') as query_file:
        query_file.write(sql_query)

    print(f"Generado Avro: {avro_file_path}")
    print(f"Generado JSON: {json_file_path}")
    print(f"Generado SQL: {sql_query_file_path}")

def process_multiple_sql_files(input_folder, avro_output_folder, json_output_folder, sql_output_folder, date_format='datetime'):
    if not os.path.isdir(input_folder):
        raise ValueError("La carpeta de entrada no existe.")

    sql_files = [f for f in os.listdir(input_folder) if f.lower().endswith('.sql')]
    if not sql_files:
        raise ValueError("No se encontraron archivos SQL en la carpeta de entrada.")

    for sql_file in sql_files:
        sql_file_path = os.path.join(input_folder, sql_file)
        generate_avro_and_mapping(sql_file_path, avro_output_folder, json_output_folder, sql_output_folder, date_format)

    print("Proceso finalizado. Todos los archivos generados correctamente.")


def generate_bigquery_table_scripts(config_folder, schema_folder, config_file=None, output_folder="sql/bigquery/scripts/"):
    """
    Genera scripts de creación de tablas en BigQuery con base en un archivo de configuración y esquemas Oracle.
    Incluye definición de claves primarias si existen en el esquema.
    """
    if not os.path.isdir(config_folder):
        raise ValueError(f"La carpeta de configuración no existe: {config_folder}")
    if not os.path.isdir(schema_folder):
        raise ValueError(f"La carpeta de esquemas no existe: {schema_folder}")

    config_files = [os.path.join(config_folder, f) for f in os.listdir(config_folder) if f.endswith(".json")]
    if config_file:
        config_files = [config_file]

    if not config_files:
        raise ValueError("No se encontraron archivos de configuración en la carpeta especificada.")

    if not os.path.isdir(output_folder):
        os.makedirs(output_folder)

    for file in config_files:
        with open(file, 'r') as f:
            config = json.load(f)

        table_name = config.get("table_name")
        zones = config.get("zone", ["stg"])
        partition_field = config.get("partition_field")
        clustering_fields = config.get("clustering_fields", [])
        partition_type = config.get("partition_type", "DAY")
        dataset = config.get("dataset")
        labels = config.get("labels", [])

        if not table_name or not dataset:
            raise ValueError(f"El archivo de configuración {file} debe contener 'table_name' y 'dataset'.")

        schema_file = os.path.join(schema_folder, f"{table_name.lower()}.sql")
        if not os.path.isfile(schema_file):
            print(f"Esquema no encontrado: {schema_file}. Saltando {table_name}.")
            continue

        fields, primary_keys = parse_oracle_schema(schema_file)

        for zone in zones:
            zone_dataset = "staging_dataset" if zone == "stg" else dataset
            bq_table_name = f"{zone}_{table_name.lower()}"

            script_lines = [f"CREATE TABLE IF NOT EXISTS `${{PROJECT_NAME}}.{zone_dataset}.{bq_table_name}` ("]
            for column_name, column_type, is_not_null in fields:
                null_status = "NOT NULL" if is_not_null else ""
                script_lines.append(f"  {column_name} {column_type} {null_status},")

            script_lines.append("  fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),")
            script_lines.append("  fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP()")

            if script_lines[-1].endswith(","):
                script_lines[-1] = script_lines[-1][:-1]
            
            if zone == "dep":
                script_lines.append(")")
            else:
                script_lines.append(");")
        

            if partition_field and zone == "dep":
                script_lines.append(f"PARTITION BY DATETIME_TRUNC({partition_field}, {partition_type})")

            if clustering_fields and zone == "dep":
                script_lines.append(f"CLUSTER BY {', '.join([field.lower() for field in clustering_fields])}")

            if labels and zone == "dep":
                label_list = ", ".join([f"('{label['key']}', '{label['value']}')" for label in labels])
                script_lines.append(f"OPTIONS(labels=[{label_list}]);")

            if primary_keys and zone == "dep":
                pk_fields = ", ".join(primary_keys)
                script_lines.append(f"ALTER TABLE `${{PROJECT_NAME}}.{zone_dataset}.{bq_table_name}` ADD PRIMARY KEY ({pk_fields}) NOT ENFORCED;")

            script = "\n".join(script_lines)

            output_file = os.path.join(output_folder, f"{zone}_{table_name.lower()}.sql")
            with open(output_file, 'w') as output:
                output.write(script)

            print(f"Script generado: {output_file}")

def parse_oracle_schema(schema_file):
    """
    Analiza un archivo SQL con una definición de tabla Oracle y extrae los campos, tipos y si son NOT NULL.
    También detecta las claves primarias definidas en la tabla.
    """
    with open(schema_file, 'r') as file:
        content = file.read()

    # Limpiar contenido eliminando elementos irrelevantes
    content = re.sub(
        r"(TABLESPACE\s+.*|SUPPLEMENTAL\s+.*|PCTFREE\s+.*|STORAGE\s+.*|LOGGING\s+.*|ENABLE ROW MOVEMENT|SEGMENT CREATION.*);?",
        "",
        content,
        flags=re.IGNORECASE | re.MULTILINE
    )

    # Extraer columnas válidas
    columns = re.findall(
        r'^\s*"([A-Za-z0-9_]+)"\s+([A-Z0-9\(\),\s]+)(\s+NOT NULL ENABLE)?(?:,|$)',
        content, re.MULTILINE
    )

    # Extraer definición de claves primarias
    primary_key_match = re.search(
        r'CONSTRAINT\s+"[A-Za-z0-9_]+"\s+PRIMARY\s+KEY\s*\((.*?)\)',
        content, re.IGNORECASE
    )
    primary_keys = []
    if primary_key_match:
        primary_keys = [
            pk.strip().strip('"').lower() for pk in primary_key_match.group(1).split(',')
        ]

    # Preparar campos válidos
    fields = []
    for column_name, column_type, not_null in columns:
        column_name = column_name.lower()  # Convertir a minúsculas
        column_type = column_type.strip().upper()

        # Mapear tipos de datos Oracle a BigQuery
        if column_type.startswith("NUMBER"):
            if "(" in column_type:  # NUMBER(p, s)
                match = re.match(r"NUMBER\((\d+),\s*(\d+)\)", column_type)
                if match:
                    precision, scale = map(int, match.groups())
                    column_type = "NUMERIC" if precision <= 38 else "BIGNUMERIC"
            else:
                column_type = "NUMERIC"
        elif column_type.startswith("VARCHAR2") or column_type.startswith("CHAR"):
            column_type = "STRING"
        elif column_type.startswith("DATE"):
            column_type = "DATETIME"
        elif column_type.startswith("RAW"):
            column_type = "BYTES"
        elif column_type in ["CLOB", "NCLOB"]:
            column_type = "STRING"
        elif column_type == "BLOB":
            column_type = "BYTES"
        else:
            column_type = "STRING"  # Tipo por defecto

        # Determinar si el campo es NOT NULL
        is_not_null = "NOT NULL" if not_null else ""

        fields.append((column_name, column_type, is_not_null))

    return fields, primary_keys

def generate_bigquery_store_procedures(template_folder, schema_folder, output_folder):
    """
    Genera procedimientos almacenados para MERGE en BigQuery basado en tablas configuradas en `resources_config.py`.
    Solo procesa tablas con el campo `merge` igual a True.
    Maneja dinámicamente la conversión de campos de fecha.
    """
    resources_config_path = os.path.join(template_folder, "resources_config.py")
    
    if not os.path.exists(resources_config_path):
        raise FileNotFoundError(f"El archivo 'resources_config.py' no existe en {template_folder}")

    if not os.path.isdir(schema_folder):
        raise ValueError(f"La carpeta de esquemas no existe: {schema_folder}")
    
    if not os.path.isdir(output_folder):
        os.makedirs(output_folder)

    # Cargar configuración desde resources_config.py
    resources_config = {}
    with open(resources_config_path, "r") as file:
        exec(file.read(), resources_config)

    resources = resources_config.get("RESOURCES_CONFIG", {})
    if not resources:
        raise ValueError("El archivo resources_config.py no contiene la clave 'RESOURCES_CONFIG'.")

    dataset_destino = resources["dataset_destino"]
    tablas = resources["tablas"]

    for tabla in tablas:
        if not tabla.get("merge", False):  # Solo procesar tablas con merge=True
            continue

        table_name = tabla["nombre"]
        schema_file = os.path.join(schema_folder, f"{table_name.lower()}.sql")
        
        if not os.path.isfile(schema_file):
            print(f"Esquema no encontrado: {schema_file}. Saltando {table_name}.")
            continue

        # Extraer campos y claves primarias del esquema
        fields, primary_keys = parse_oracle_schema(schema_file)

        if not fields or not primary_keys:
            print(f"No se encontraron campos o claves primarias en el esquema de {table_name}. Saltando.")
            continue

        # Identificar campos de tipo fecha
        date_fields = [field[0] for field in fields if field[1] in ("DATETIME", "DATE")]

        all_fields = [field[0] for field in fields]
        all_fields.append("fecha_creacion")
        all_fields.append("fecha_actualizacion")

        # Preparar nombres de tabla y procedimiento
        target_table = f"${{PROJECT_NAME}}.{dataset_destino}.dep_{table_name.lower()}"
        source_table = f"${{PROJECT_NAME}}.staging_dataset.stg_{table_name.lower()}"
        procedure_name = f"{dataset_destino}.sp_merge_dep_{table_name.lower()}"

        # Crear las cláusulas ON, UPDATE y INSERT
        on_clause = " AND ".join([f"T.{pk} = S.{pk}" for pk in primary_keys])

        update_fields = [
            f"T.{field} = " + (f"CAST(S.{field} AS DATETIME)" if field in date_fields else f"S.{field}")
            for field in all_fields if field not in ["fecha_creacion", "fecha_actualizacion"]
        ]
        update_clause = ",\n      ".join(update_fields)
        update_clause += ",\n      T.fecha_actualizacion = CURRENT_TIMESTAMP()"

        insert_fields = ",\n      ".join(all_fields)
        insert_values = ",\n      ".join([
            f"CAST(S.{field} AS DATETIME)" if field in date_fields else (
                "CURRENT_TIMESTAMP()" if field in ["fecha_creacion", "fecha_actualizacion"] else f"S.{field}"
            )
            for field in all_fields
        ])

        # Generar el procedimiento almacenado
        procedure_script = f"""
CREATE OR REPLACE PROCEDURE `${{PROJECT_NAME}}.{procedure_name}`()
BEGIN
  MERGE `{target_table}` T
  USING `{source_table}` S
  ON {on_clause}
  WHEN MATCHED THEN
    UPDATE SET
      {update_clause}
  WHEN NOT MATCHED THEN
    INSERT (
      {insert_fields}
    )
    VALUES (
      {insert_values}
    );
END;
"""

        # Guardar el archivo
        output_file = os.path.join(output_folder, f"sp_merge_dep_{table_name.lower()}.sql")
        with open(output_file, 'w') as output:
            output.write(procedure_script)

        print(f"Procedimiento almacenado generado: {output_file}")



def extract_oracle_schemas(output_folder, tables_config="schemas/config/oracle_tables.py", config_path="connections/oracle_config.py"):
    """
    Extrae el esquema de tablas Oracle y genera archivos SQL.
    """
    # Cargar listado de tablas
    table_list = load_table_list(tables_config)
    print(f"Tablas a procesar: {table_list}")

    # Cargar configuración Oracle
    config = load_oracle_config(config_path)
    # Fuerza el uso del Thin Client
    oracledb.init_oracle_client(lib_dir=None, driver_mode=oracledb.DRIVER_MODE_THIN)
    # Conectar a Oracle
    try:
        connection = oracledb.connect(user=config['user'], password=config['password'], host=config['host'], service_name=config['service_name'], port=1521)
        print("Conexión a Oracle exitosa.")
    except Exception as e:
        raise Exception(f"Error conectándose a Oracle: {e}")

    # Crear carpeta de salida si no existe
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Procesar cada tabla
    for table in table_list:
        try:
            cursor = connection.cursor()

            # Obtener el esquema de la tabla
            cursor.execute(f"""
                SELECT DBMS_METADATA.GET_DDL('TABLE', '{table}') FROM DUAL
            """)
            ddl = cursor.fetchone()[0]

            # Limpiar el esquema (opcional)
            ddl_cleaned = re.sub(r'SEGMENT\s+CREATION.*?;', ';', ddl, flags=re.DOTALL)

            # Guardar el esquema en un archivo .sql
            file_path = os.path.join(output_folder, f"{table.lower()}.sql")
            with open(file_path, 'w') as f:
                f.write(ddl_cleaned)
            print(f"Esquema generado para la tabla: {table}")

        except Exception as e:
            print(f"Error extrayendo esquema para {table}: {e}")
        finally:
            cursor.close()

    connection.close()
    print("Extracción completada.")

def load_table_list(config_path="schemas/config/oracle_tables.py"):
    """
    Carga el listado de tablas desde un archivo .py.
    """
    if not os.path.isfile(config_path):
        raise FileNotFoundError(f"El archivo de configuración no existe: {config_path}")
    
    spec = importlib.util.spec_from_file_location("config", config_path)
    config = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(config)

    if not hasattr(config, "ORACLE_TABLES"):
        raise AttributeError("El archivo de configuración no contiene 'ORACLE_TABLES'.")

    return config.ORACLE_TABLES

def load_oracle_config(config_path):
    """
    Carga la configuración de conexión Oracle desde un archivo .py usando exec.
    """
    oracle_config = {}
    try:
        with open(config_path, "r") as file:
            exec(file.read(), oracle_config)
        connection_config = oracle_config.get("CONNECTION_CONFIG", {})
        if not connection_config:
            raise ValueError("CONNECTION_CONFIG no definido en el archivo de configuración.")
        return connection_config
    except Exception as e:
        raise Exception(f"Error al cargar la configuración Oracle: {e}")
    
def generate_tables_to_process(template_folder):
    """
    Genera el archivo tables_to_process.py en la carpeta template basado en resources_config.py.
    """
    import textwrap

    resources_config_path = os.path.join(template_folder, "resources_config.py")
    tables_to_process_path = os.path.join(template_folder, "tables_to_process.py")

    # Verificar si el archivo resources_config.py existe
    if not os.path.exists(resources_config_path):
        raise FileNotFoundError(f"El archivo resources_config.py no se encuentra en {template_folder}")

    # Cargar el contenido de resources_config.py
    resources_config = {}
    with open(resources_config_path, "r") as file:
        exec(file.read(), resources_config)

    resources = resources_config.get("RESOURCES_CONFIG", {})

    # Validar que la configuración contenga las claves necesarias
    required_keys = [
        "dataset_destino",
        "dominio",
        "subdominio",
        "origen",
        "tablas",
        "producto"
    ]

    for key in required_keys:
        if key not in resources:
            raise ValueError(f"Falta la clave requerida '{key}' en RESOURCES_CONFIG")

    # Generar la estructura de TABLES_TO_PROCESS
    tables_to_process = []
    for table in resources["tablas"]:
        table_entry = {
            "oracle_table": table["nombre"].upper(),
            "bigquery_table": table["nombre"].lower(),
            "dataset_destino": f"{resources['dataset_destino']}",
            "store_procedure": f"sp_merge_dep_{table['nombre'].lower()}",
            "gcs_schema_avsc_path": f"{resources['dominio']}/{resources['subdominio']}/{resources['producto']}/{resources['origen']}",
            "dominio": resources["dominio"],
            "subdominio": resources["subdominio"],
            "gcs_schema_json_path": f"{resources['dominio']}/{resources['subdominio']}/{resources['producto']}/{resources['origen']}",
            "gcs_query": f"{resources['dominio']}/{resources['subdominio']}/{resources['producto']}/{resources['origen']}",
            "gcs_ingest_path": f"data_ingest_{resources['origen']}/{resources['dominio']}/{resources['subdominio']}/{resources['producto']}",
            "gcs_raw_path": f"{resources['dominio']}/{resources['subdominio']}/{resources['producto']}/{resources['origen']}",
            "origen": resources["origen"],
            "merge": table["merge"],
            "load_mode": table["load_mode"],
            "producto": resources["producto"],

        }
        tables_to_process.append(table_entry)

    # Guardar el archivo tables_to_process.py con formato ordenado
    with open(tables_to_process_path, "w") as file:
        file.write("TABLES_TO_PROCESS = [\n")
        for entry in tables_to_process:
            formatted_entry = textwrap.indent(
                f"{repr(entry)},", "    "
            )
            file.write(f"{formatted_entry}\n")
        file.write("]\n")

    print(f"Archivo tables_to_process.py generado en {tables_to_process_path}")
