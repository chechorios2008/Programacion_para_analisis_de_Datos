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
                f"postgresql+psycopg2://{self.user}:{self.password}@{self.host}:{self.port}/{self.nombredb}"
            )
            with self.conection.connect() as connection:
                print("Conexión exitosa")
        except SQLAlchemyError as e:
            print(f"Conexión errónea: {e}")
        except Exception as e:
            print(f"Ocurrió un error inesperado durante la conexión: {e}")

    def create_schema(self, nombre_schema=""):
        try:
            nombre_schema = nombre_schema.replace(".", "")
            with self.conection.connect() as conexion:
                create_schema = f"CREATE SCHEMA IF NOT EXISTS {nombre_schema};"
                conexion = conexion.execution_options(isolation_level="AUTOCOMMIT")
                conexion.execute(text(create_schema))
                print("Creación de esquema exitosa")
        except SQLAlchemyError as e:
            print(f"Error al crear el esquema: {e}")
        except Exception as e:
            print(f"Ocurrió un error inesperado al crear el esquema: {e}")

    def create_table(self, nombre_tbl="", ruta_sql="", schema="", columnas=""):
        try:
            with open(ruta_sql, "r") as file:
                script_tabla = file.read()
            with self.conection.connect() as conexion:
                conexion = conexion.execution_options(isolation_level="AUTOCOMMIT")
                script_tabla = script_tabla.format(schema, nombre_tbl, columnas)
                conexion.execute(text(script_tabla))
                print("Creación exitosa de tabla")
        except FileNotFoundError as e:
            print(f"Archivo SQL no encontrado: {e}")
        except SQLAlchemyError as e:
            print(f"Creación errónea de tabla: {e}")
        except Exception as e:
            print(f"Ocurrió un error inesperado al crear la tabla: {e}")

    def insert_df(self, df, nombre_tabla, tipo_insert="append"):
        """
        Inserta un DataFrame en la tabla especificada de la base de datos.

        Args:
            df (pd.DataFrame): DataFrame a insertar.
            nombre_tabla (str): Nombre de la tabla de destino.
            tipo_insert (str): Comportamiento en caso de existir datos ('append', 'replace', etc.).
        """
        try:
            # Insertar el DataFrame en la base de datos
            df.to_sql(
                nombre_tabla,
                con=self.conection,
                schema=self.schema,
                if_exists=tipo_insert,
                index=False,
            )
            print(f"Se insertó correctamente en {nombre_tabla}")
        except SQLAlchemyError as e:
            print(f"No se pudo insertar en {nombre_tabla}. Error: {e}")