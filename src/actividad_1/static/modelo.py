from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
import pandas as pd
from datetime import datetime


class Modelo:
    def __init__(self, host="", port="", nombredb="", user="", password="", schema=""):
        self.host = host
        self.port = port
        self.nombredb = nombredb
        self.user = user
        self.password = password
        self.schema = schema
        self.conection = None
        self.conect()

    def conect(self):
        try:
            self.conection = create_engine(
                f'postgresql+psycopg2://{self.user}:{self.password}@{self.host}:{self.port}/{self.nombredb}'
            )
            with self.conection.connect() as connection:
                print("Conexión exitosa")
        except SQLAlchemyError as e:
            print(f"Conexión errónea: {e}")
        except Exception as e:
            print(f"Ocurrió un error inesperado durante la conexión: {e}")

    def create_schema(self, nombre_schema=""):
        try:
            nombre_schema = nombre_schema.replace(".","")
            with self.conection.connect() as conexion:
                create_schema = f'CREATE SCHEMA IF NOT EXISTS {nombre_schema};'
                conexion = conexion.execution_options(isolation_level="AUTOCOMMIT")
                conexion.execute(text(create_schema))
                print("Creación de esquema exitosa")
        except SQLAlchemyError as e:
            print(f"Error al crear el esquema: {e}")
        except Exception as e:
            print(f"Ocurrió un error inesperado al crear el esquema: {e}")


    def create_table(self, nombre_tbl="", ruta_sql="",schema="",columnas=""):
        try:
            with open(ruta_sql, 'r') as file:
                script_tabla = file.read()
            with self.conection.connect() as conexion:
                conexion = conexion.execution_options(isolation_level="AUTOCOMMIT")
                script_tabla = script_tabla.format(schema,nombre_tbl,columnas)
                conexion.execute(text(script_tabla))
                print("Creación exitosa de tabla")
        except FileNotFoundError as e:
            print(f"Archivo SQL no encontrado: {e}")
        except SQLAlchemyError as e:
            print(f"Creación errónea de tabla: {e}")
        except Exception as e:
            print(f"Ocurrió un error inesperado al crear la tabla: {e}")


    def insert_df(self,ruta_insumo="", nombre_tabla="", tipo_insert='append',tipo="xlsx"):
        fecha_actual = datetime.now()
        try:
            df = pd.read_excel(ruta_insumo,index_col=False)
            df["f_extraccion"] = fecha_actual
            print("Se creo el dataframe")
        except SQLAlchemyError as e:
            print("No se creo el dataframe {}".format(e))
        try:
            #df.to_sql(nombre_tabla, con=self.conection,schema=None,  if_exists=tipo_insert, index=False)
            df.to_sql(nombre_tabla, con=self.conection, schema=self.schema, if_exists=tipo_insert, index=False)
            print("Se inserto correctamente en {}".format(nombre_tabla))
        except SQLAlchemyError as e:
            print("No se inserto en {} error {}".format(nombre_tabla, e))