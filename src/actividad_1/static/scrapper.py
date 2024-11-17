from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import pandas as pd


class Scraper_comercio:
    def __init__(self, url):
        """
        Inicializa el scraper con la URL del sitio web y configura el driver.
        """
        self.url = url
        self.driver = None
        self.data = []

    def iniciar_driver(self):
        """
        Inicializa el driver de Selenium.
        """
        self.driver = webdriver.Chrome()
        self.driver.get(self.url)

    def extraer_datos(self):
        """
        Extrae los datos de productos de la página web.
        """
        li_elements = self.driver.find_elements(By.CSS_SELECTOR, '#js-hits li')

        for element in li_elements:
            try:
                titulo_element = element.find_element(By.TAG_NAME, 'h3')
                precio_element = element.find_element(By.CLASS_NAME, 'price')
                marca_element = element.find_element(By.CLASS_NAME, 'product__item__information__brand')
                self.data.append({
                    'categoria': 'Celulares',
                    'marca': marca_element.text,
                    'nombre_producto': titulo_element.text,
                    'precio': precio_element.text
                })
            except NoSuchElementException:
                pass

    def procesar_datos(self):
        """
        Convierte los datos extraídos en un DataFrame y limpia la columna de precios.
        """
        df = pd.DataFrame(self.data)
        df['precio'] = df['precio'].replace({'\$': '', '\.': ''}, regex=True).astype(float)
        return df

    def cerrar_driver(self):
        """
        Cierra el driver de Selenium.
        """
        if self.driver:
            self.driver.quit()

    def ejecutar(self):
        """
        Método que realiza el flujo completo de scraping y devuelve el DataFrame final.
        """
        try:
            self.iniciar_driver()
            self.extraer_datos()
            return self.procesar_datos()
        finally:
            self.cerrar_driver()