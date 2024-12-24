import re

def generate_gcs_object_name(resources_config_path):
    """
    Genera el valor de GCS_OBJECT_NAME basado en los datos de resources_config.py.
    """
    resources_config = {}
    with open(resources_config_path, "r") as file:
        exec(file.read(), resources_config)

    resources = resources_config.get("RESOURCES_CONFIG", {})
    dominio = resources.get("dominio", "unknown")
    subdominio = resources.get("subdominio", "unknown")
    origen = resources.get("origen", "unknown")
    producto = resources.get("producto", "unknown")

    return f"{dominio}/{subdominio}/{producto}/{origen}/tables_to_process.py"


def replace_template(template_file, dag_file, resources_config_path):
    # Confirmar con el usuario si desea proceder
    confirmation = input(f"¿Está seguro de reemplazar el contenido de tu dag con el del template? (si/no): ").lower()
    if confirmation not in ["si", "s", "yes", "y"]:
        print("Operación cancelada.")
        return

    try:
        # Generar el valor de GCS_OBJECT_NAME
        gcs_object_name = generate_gcs_object_name(resources_config_path)

        # Leer el contenido del template
        with open(template_file, "r") as template:
            content = template.read()

        # Reemplazar la variable GCS_OBJECT_NAME en el contenido del template
        updated_content = re.sub(
            r'GCS_OBJECT_NAME\s*=\s*".*?"', 
            f'GCS_OBJECT_NAME = "{gcs_object_name}"', 
            content
        )

        # Escribir el contenido actualizado en el archivo DAG
        with open(dag_file, "w") as dag:
            dag.write(updated_content)

        print(f"Contenido de '{dag_file}' reemplazado con éxito con GCS_OBJECT_NAME: {gcs_object_name}")

    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{template_file}' o '{dag_file}'.")
    except Exception as e:
        print(f"Error al reemplazar contenido: {e}")
