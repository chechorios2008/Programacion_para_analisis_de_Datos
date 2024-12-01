from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import time
from data_transform import Transform


class ScraperComercio:
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

    def extraer_datos(self):
        """
        Extrae los datos de productos de la página web.
        """
        if not hasattr(self, "driver") or self.driver is None:
            raise AttributeError(
                "El driver no está inicializado. Asegúrate de llamar a 'iniciar_driver()' antes."
            )

        if not hasattr(self, "data"):
            self.data = []

        for page in range(1, 15): 
            try:
                url = self.url.format(page)
                print(f"Accediendo a: {url}")
                self.driver.get(url)

                # Esperar unos segundos para que la página cargue completamente
                time.sleep(1)

                # Obtener los elementos de la página actual
                li_elements = self.driver.find_elements(
                    By.XPATH,
                    "//*[@id='js-hits']//li[contains(@class,'js-product-item')]",
                )
                if not li_elements:
                    print(f"No se encontraron elementos en la página {page}")
                    continue

                for element in li_elements:
                    try:
                        # Extraer datos de cada producto
                        titulo_element = element.find_element(By.TAG_NAME, "h3")
                        precio_element = element.find_element(By.CLASS_NAME, "price")
                        marca_element = element.find_element(
                            By.CLASS_NAME, "product__item__information__brand"
                        )

                        # Agregar los datos al listado
                        self.data.append(
                            {
                                "categoria": "Smartphone",
                                "marca": marca_element.text.strip(),
                                "nombre_producto": titulo_element.text.strip(),
                                "precio": precio_element.text.strip(),
                            }
                        )

                    except NoSuchElementException as e:
                        print(f"Elemento faltante en la página {page}: {e}")
                    except Exception as e:
                        print(
                            f"Error desconocido al procesar un elemento en la página {page}: {e}"
                        )

            except Exception as e:
                print(f"Error al acceder a la página {page}: {e}")

        print(f"Extracción completada. Total de productos extraídos: {len(self.data)}")

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
            return Transform(self.data).transform()
        except Exception as e:
            print(f"Error al ejecutar el scraping: {e}")
        finally:
            self.cerrar_driver()