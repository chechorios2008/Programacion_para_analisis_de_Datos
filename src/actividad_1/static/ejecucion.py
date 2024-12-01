import os
from modelo import Modelo
from scrapper import ScraperComercio


ruta_base = os.path.dirname(__file__)
ruta_sql = os.path.join(ruta_base, "sql", "script_creacion.sql")

host = "localhost"
port = "5432"
nombredb = "postgres"
user = "postgres"
password = "2789478"
nombre_tabla = "catalogo_ventas"
nombre_schema = "informacion_comercial"

columnas = """
    id SERIAL PRIMARY KEY,
    categoria VARCHAR(255),
    marca VARCHAR(255),
    nombre_producto VARCHAR(255) NOT NULL,
    precio INT NOT NULL,
    memoria VARCHAR(255),
    os VARCHAR(50),
    f_extraccion TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP  
"""

# URL del sitio web a scrapear
url = "https://www.alkosto.com/celulares/smartphones/c/BI_101_ALKOS?page={}&sort=relevance"


def main():
    try:
        # Inicializar scraper y obtener datos
        scraper = ScraperComercio(url)
        df = scraper.ejecutar()

        # Conectar con la base de datos y realizar las operaciones
        modelo = Modelo(host, port, nombredb, user, password, schema=nombre_schema)
        modelo.create_schema(nombre_schema)
        modelo.create_table(
            nombre_tbl=nombre_tabla,
            ruta_sql=ruta_sql,
            schema=nombre_schema,
            columnas=columnas,
        )
        modelo.insert_df(
            df=df, nombre_tabla=nombre_tabla, tipo_insert="append"
        )  # Pasar el DataFrame directamente
        print("Datos insertados exitosamente en la base de datos.")
    except Exception as e:
        print(f"Error durante la ejecución: {e}")


if __name__ == "__main__":
    main()