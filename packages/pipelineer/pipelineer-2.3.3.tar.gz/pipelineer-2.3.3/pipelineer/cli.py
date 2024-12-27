import argparse
import os
import pkg_resources  # Para acceder a archivos dentro del paquete
from .utils.generator import process_multiple_sql_files, generate_bigquery_table_scripts, generate_bigquery_store_procedures,extract_oracle_schemas,generate_tables_to_process
from .utils.templates import replace_template


def main():
    parser = argparse.ArgumentParser(description="Herramienta para generar esquemas Avro, JSON y SQL desde archivos SQL")
    
    # Subcomandos principales
    subparsers = parser.add_subparsers(dest="command", required=True, help="Comando principal ('make')")

    # Subcomando 'make'
    make_parser = subparsers.add_parser("make", help="Subcomando 'make'")
    make_subparsers = make_parser.add_subparsers(dest="subcommand", required=True, help="Subcomandos de 'make' ('schemas' o 'template')")

    # Subcomando 'make schemas'
    schemas_parser = make_subparsers.add_parser("ingest_schemas", help="Subcomando 'ingest_schemas'")
    schemas_parser.add_argument("--input-folder", default="schemas/oracle", help="Carpeta de entrada con .sql")
    schemas_parser.add_argument("--avro-output-folder", default="schemas/avsc", help="Carpeta de salida Avro")
    schemas_parser.add_argument("--json-output-folder", default="schemas/json", help="Carpeta de salida JSON")
    schemas_parser.add_argument("--sql-output-folder", default="sql/oracle", help="Carpeta de salida SQL")
    schemas_parser.add_argument("--date-format", default="datetime", choices=["date", "datetime"], help="Formato de fechas")

    # Subcomando 'make template'
    template_parser = make_subparsers.add_parser("template", help="Subcomando 'template'")
    template_parser.add_argument("--type", required=True, choices=["oracle", "api"], help="Tipo de template (oracle o api)")

    # Subcomando 'make bq_tables'
    bq_tables_parser = make_subparsers.add_parser("bq_tables", help="Subcomando 'bq_tables'")
    bq_tables_parser.add_argument("--config-folder", default="sql/bigquery/config/", help="Carpeta con los archivos de configuración de BigQuery (predeterminado: sql/bigquery/config/)")
    bq_tables_parser.add_argument("--config-file", help="Ruta del archivo de configuración específico (opcional)")
    bq_tables_parser.add_argument("--output-folder", default="sql/bigquery/scripts/create_table", help="Carpeta de salida para los scripts de creación de tablas (predeterminado: sql/bigquery/scripts/)")
    bq_tables_parser.add_argument("--schema-folder", default="schemas/oracle", help="Carpeta con los archivos de esquema Oracle (.sql)")

    # Subcomando 'make bq_store_procedures'
    sp_procedures_parser = make_subparsers.add_parser("bq_store_procedures", help="Generar procedimientos almacenados para MERGE")
    sp_procedures_parser.add_argument("--output-folder", default="sql/bigquery/scripts/store_procedure/", help="Carpeta de salida para los procedimientos almacenados (predeterminado: sql/scripts/store_procedure/)")
    sp_procedures_parser.add_argument("--schema-folder", default="schemas/oracle", help="Carpeta de entrada con .sql")
    
    # Subcomando 'make oracle_schemas'
    oracle_schemas_parser = make_subparsers.add_parser("oracle_schemas", help="Extrae esquemas de Oracle")
    oracle_schemas_parser.add_argument("--output-folder", default="schemas/oracle", help="Carpeta de salida")

    args = parser.parse_args()

    if args.command == "make":
        if args.subcommand == "ingest_schemas":
            process_multiple_sql_files(
                input_folder=args.input_folder,
                avro_output_folder=args.avro_output_folder,
                json_output_folder=args.json_output_folder,
                sql_output_folder=args.sql_output_folder,
                date_format=args.date_format,
            )
        elif args.subcommand == "template":
            template_file = ""
            dag_file = ""
            
            template_file = None
            if args.type == "oracle":
                generate_tables_to_process("template")
                template_file = pkg_resources.resource_filename(__name__, "templates/oracle.py")
            elif args.type == "api":
                template_file = pkg_resources.resource_filename(__name__, "templates/api.py")

            # Buscar archivo dag_
            for file in os.listdir("."):
                if file.startswith("dag_"):
                    dag_file = file
                    break

            if not dag_file:
                print("Error: No se encontró un archivo que comience con 'dag_' en la raíz.")
                return

            # Reemplazar contenido
            replace_template(template_file, dag_file,  resources_config_path="template/resources_config.py")
        elif args.subcommand == "bq_tables":
            generate_bigquery_table_scripts(
                config_folder=args.config_folder,
                schema_folder=args.schema_folder, 
                config_file=args.config_file,
                output_folder=args.output_folder
            )
        elif args.subcommand == "bq_store_procedures":
            generate_bigquery_store_procedures(
                schema_folder=args.schema_folder,
                output_folder=args.output_folder,
                template_folder = "template"

            )
        elif args.subcommand == "oracle_schemas":
            extract_oracle_schemas(output_folder=args.output_folder)
        else:
            make_parser.print_help()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
