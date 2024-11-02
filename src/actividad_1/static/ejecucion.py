import os
from modelo import Modelo

ruta_base = os.path.dirname(__file__)
ruta_sql = os.path.join(ruta_base, 'sql', 'script_creacion.sql')
ruta_xlsx = os.path.join(ruta_base, 'xlsx', 'data_comercio.xlsx')

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
    precio DECIMAL(10, 2) NOT NULL,
    f_extraccion TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP  
"""
modelo = Modelo(host, port, nombredb, user, password, schema=nombre_schema)
modelo.create_schema(nombre_schema)
modelo.create_table(nombre_tbl=nombre_tabla, ruta_sql=ruta_sql, schema=nombre_schema, columnas=columnas)
modelo.insert_df(ruta_insumo=ruta_xlsx, nombre_tabla=nombre_tabla, tipo_insert='append')
