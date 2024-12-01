from datetime import datetime
import pandas as pd
import numpy as np
import re


class Transform:
    def __init__(self, data):
        self.df = pd.DataFrame(data)

    def clean_data(self):
        self.df = self.df.drop_duplicates()
        self.df = self.df.drop(index=0)

    def date_transform(self):
        self.df["f_extraccion"] = datetime.now().date()

    def price_transform(self):

        # Función auxiliar para limpiar y convertir un solo valor de precio
        def clean_price(price_str):
            # Elimina todos los caracteres no numéricos
            cleaned_price = re.sub(r"[^\d]", "", price_str)
            # Convierte la cadena limpia a un número entero
            return int(cleaned_price)

        self.df["precio"] = self.df["precio"].apply(clean_price)

    def memoria_column(self):

        # Función para extraer el valor de memoria
        def extraer_memoria(nombre_producto):
            # Busca el patrón "número GB" (con o sin espacio)
            patron = r"(\d+) ?GB"
            match = re.search(patron, nombre_producto)
            if match:
                return match.group(1) + " GB"  # Devuelve el valor completo con el "GB"
            else:
                return ""  # Si no se encuentra el patrón, devuelve None

        # Aplica la función a cada fila de la columna 'nombre_producto'
        self.df["memoria"] = self.df["nombre_producto"].apply(extraer_memoria)

    def operative_sistem(self):

        def asignar_os(nombre_producto):
            primeros_7 = nombre_producto[:7].lower()
            if primeros_7 == "iphone ":
                return "iOS"
            elif primeros_7 == "celular":
                return "Android"
            else:
                return "Otro OS"  # Valor por defecto para otros casos

        self.df["os"] = self.df["nombre_producto"].apply(asignar_os)

    def transform(self):
        self.clean_data()
        self.date_transform()
        self.price_transform()
        self.memoria_column()
        self.operative_sistem()
        print("Datos transformados con éxito")
        print(self.df.head())
        return self.df
