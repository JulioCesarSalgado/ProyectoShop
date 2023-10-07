import json
import time
import sys
import os
import logging
import arrow
from datetime import date
from abc import ABC, abstractmethod
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import uuid
import jsonlines
import datetime
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(root_dir)
from models.catalog_item import CatalogItem
import timeit
from kafka import KafkaProducer

# Crear un logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Crear un manejador para escribir los logs a un archivo
file_handler = logging.FileHandler('app.log')
logger.addHandler(file_handler)

# Crear un manejador para escribir los logs a stdout
stream_handler = logging.StreamHandler()
logger.addHandler(stream_handler)

while True:
    kafka_host = os.environ.get('KAFKA_HOST')
    port_kafka_host = os.environ.get('PORT_KAFKA_HOST')

    if kafka_host is not None and port_kafka_host is not None:
        # Las variables de entorno están disponibles, sal del bucle
        break

    logging.info("Esperando a que las variables de entorno estén disponibles...")
    time.sleep(10)

catalog_items = []
catalog_items_jsonl = []

producer = KafkaProducer(bootstrap_servers=f'{kafka_host}:{port_kafka_host}')

logging.info("Funciona")
class CarsoSelenium(ABC):
    """ Base class for our carso-based catalog seleniumm """
    @abstractmethod
    def __init__(self, **kwargs):
        self.gcount = 0
        self.archive = kwargs.get("archive")
        
        self.shop = kwargs.get("shop")
        self.url = kwargs.get("url")
        self.article = kwargs.get("article")
        self.next = kwargs.get("next")
        
        self.name = kwargs.get("name")
        self.price = kwargs.get("price")
        self.description = kwargs.get("description")
        self.category = kwargs.get("category")
        self.specifications = kwargs.get("specifications")
        self.classspecifications = kwargs.get("classspecifications")
        self.picture = kwargs.get("picture")
        self.date = kwargs.get("date")

    def parse(self):
        urls = []
        categories = []


        def get_text_exclude_children(driver, element, position): # Funcion para seleccionar el primer nodo de un texto en el cuerpo HTML
            return driver.execute_script("""
            var parent = arguments[0];
            var position = arguments[1];
            var child = parent.childNodes[position];
            var ret = "";
            if (child.nodeType === Node.TEXT_NODE)
                ret += child.textContent;
            return ret;
            """, element, position)
        
        def find_element_text(driver, xpath): # Funcion para seleccionar el texto de un elemento por medio de xpath
            # logging.info(xpath)
            # logging.info(driver)
            try:
                element = driver.find_element(By.XPATH, xpath)
                # logging.info(element.text) # Impresion para asegurarse de que esta haciendo iteraciones correctamente
                return element.text
            except Exception as e:
                logging.info(f"Error: $e")# Impresion para asegurarse de que esta haciendo iteraciones correctamente
                # logging.info("Errores extraños")
                return "Error"
            
        def Categoria(url, category, driver): # Funcion donde se obtiene la informacion de cada producto de todas las paginas "Next" que contiene la categoria
            try: # Validar inexistente driver
                driver.quit()
            except Exception as e:
                logging.info("Ningun driver")

            logging.info("Cargando nuevo driver...")
            time.sleep(5)

            
            # Seccion para configurar Selenium
            # options = webdriver.ChromeOptions()
            # options.headless = True
            # options.binary_location = r'/usr/bin/google-chrome'
            # driver = webdriver.Chrome(executable_path=r'/usr/local/bin/chromedriver', options=options)
            # driver.implicitly_wait(5)
            
            options = Options()
            options.add_argument('--headless')
            driver = webdriver.Chrome(options=options)
            driver.implicitly_wait(5)

            #options = webdriver.FirefoxOptions()
            #options.headless = True
            #options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'
            #driver = webdriver.Firefox(executable_path=r'C:\Users\julio\OneDrive\Documentos\Semestre 9\SCRAPYNLP\geckodriver-v0.32.2-win32\geckodriver.exe', options=options)
            #driver.implicitly_wait(5)
            
            # Cierre de seccion para configurar Selenium

            name = ""
            price = 0.0
            specifications = {}
            pictures = []
            count = 0

            # Direccion url de la categoria o del "Next" si entro por recursividad
            driver.get(url)

            # Selecciona todos los productos de la primera pagina de la categoria
            tagsP = driver.find_elements(By.XPATH, self.article) #'//div[@class="boxProductosCategory"]/article[@class="cardProduct"]/a'

            urlsP = []

            for tag in tagsP: # Se crea una lista de URLs de cada producto
                urlsP.append(tag.get_attribute('href'))

            for urls in urlsP: # Iteracion por la direccion url de cada producto

                start = timeit.default_timer()
                count += 1
                self.gcount += 1

                

                if self.gcount % 100 == 0: # Cada 100 productos actualizaremos el driver para optimizacion
                    driver.quit()
                    logging.info("Cargando nuevo driver...")
                    time.sleep(5)
                    
                    # Seccion para configurar Selenium

                    options = Options()
                    options.add_argument('--headless')
                    driver = webdriver.Chrome(options=options)
                    driver.implicitly_wait(5)

                    # options = webdriver.ChromeOptions()
                    # options.headless = True
                    # options.binary_location = r'/usr/bin/google-chrome'
                    # driver = webdriver.Chrome(executable_path=r'/usr/local/bin/chromedriver', options=options)
                    # driver.implicitly_wait(5)
                    
                    #options = webdriver.FirefoxOptions()
                    #options.headless = True
                    #options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'
                    #driver = webdriver.Firefox(executable_path=r'C:\Users\julio\OneDrive\Documentos\Semestre 9\SCRAPYNLP\geckodriver-v0.32.2-win32\geckodriver.exe', options=options)
                    #driver.implicitly_wait(5)

                    # Cierre de seccion para configurar Selenium
                    

                # Direccion del producto en la iteracion n

                driver.get(urls)

                # Tiempo de espera para dejar cargando la pagina
                time.sleep(3)
                
                logging.info(f"Categoría {category}") # Impresion para asegurarse de que esta haciendo iteraciones correctamente

                # Recoleccion del nombre del producto
                name = find_element_text(driver, self.name) #'//h1[@class="h2"]'

                try: # Recoleccion del precio del producto
                    # logging.info(get_text_exclude_children(driver, driver.find_element(By.XPATH, self.price), 0)) # Impresion para asegurarse de que esta haciendo iteraciones correctamente
                    price = get_text_exclude_children(driver, driver.find_element(By.XPATH, self.price), 0) #'//div[@class="pPrice"][text()]'
                except Exception as e:
                    # logging.info("Precio")
                    logging.info(f"Error: $e") # Impresion para asegurarse de que esta haciendo iteraciones correctamente
                    price = "Error"

                # Recoleccion de la descripcion del producto
                description = find_element_text(driver, self.description) #'//div[@class="textDescriptionSears"]'
             

                if "Sanborns" == self.shop: # Si es la pagina Sanborns, se hace click en un boton para activar la visibilidad de las especificaciones
                    try:
                        driver.find_element(By.ID, "react-tabs-2").click()
                    except Exception as e:
                        logging.info("Visibilidad")
                        logging.info(f"Error: $e") 

                if "Sanborns" == self.shop: # Si es la pagina Sanborns, se hace click en un boton para activar la visibilidad de las especificaciones
                    try:
                        driver.find_element(By.ID, "react-tabs-2").click()
                    except Exception as e:
                        logging.info("Visibilidad")
                        logging.info(f"Error: $e") 

                try: # Recoleccion de las especificaciones
                    li_elements = driver.find_elements(By.XPATH, self.specifications) #'//ul[@class="listAttributes"]/li'
                    for li in li_elements: # Se enlistan las especificaciones
                        key = str(li.find_element(By.CLASS_NAME, self.classspecifications[0]).text) #atributesKey xh-highlight
                        value = str(li.find_element(By.CLASS_NAME, self.classspecifications[1]).text) #atributesValue xh-highlight
                        specifications[key] = value
                except Exception as e:
                    logging.info("Especificaciones")
                    logging.info(f"Error: $e") 

                # logging.info(specifications) # Impresion para asegurarse de que esta haciendo iteraciones correctamente

                try:
                    elements = driver.find_elements(By.XPATH, self.picture) #'//div/img[@class="imagenInferiorActual"]'
                    pictures = [element.get_attribute('src') for element in elements]
                    pictures = list(map(str, pictures))
                except Exception as e:
                    logging.info("Imagen")
                    logging.info(f"Error: $e")
                
                # logging.info(pictures) # Impresion para asegurarse de que esta haciendo iteraciones correctamente

                # logging.info(self.date) # Impresion para asegurarse de que esta haciendo iteraciones correctamente

                try: # Cambiamos el formato del precio a float
                    price = float(price.replace('$', '').replace(',', ''))
                except Exception as e:
                    price = 0.000

		# Generar un UUID
                item_id = str(uuid.uuid4())

                catalog_items.append(CatalogItem( # Guardamos la informacion a una lista.
                    id = item_id,
                    name = name,
                    price = price,
                    desc = description,
                    category = str(category),
                    specifications = specifications,
                    pictures= pictures,
                    date = arrow.now().format('YYYY-MM-DD')
                ))

                data = json.dumps(catalog_items[-1].__dict__, default=date_handler, ensure_ascii=False)
                producer.send('productos', value=data.encode('utf-8'))
                producer.flush()
                logging.info(f"{self.gcount} productos almacenados.") # Impresion para asegurarse de que esta haciendo iteraciones correctamente
                #logging.info(json.dumps(catalog_items[-1].__dict__, default=date_handler, ensure_ascii=False))

		#logging.info(catalog_items)
                
		# catalog_items_jsonl.append({
                #     'id': str(uuid.uuid1()),
                #     'name': name,
                #     'price': price,
                #     'desc': description,
                #     'category': str(category),
                #     'specifications': specifications,
                #     'pictures': pictures,
                #     'date': datetime.date.today().isoformat()
                # })

                # with open(self.archive, "a", encoding="utf-8") as f: # Creacion del archivo Json de Sears
                #     json.dump(catalog_items[-1].dict(), f, default=date_handler, ensure_ascii=False)
                #     f.write(",\n")
                end = timeit.default_timer()

                logging.info(f"Tiempo de ejecucion: {end - start} segundos para escribir en el archivo json.")        

            # Volvemos a la direccion url de la categoria o del "Next" si entro por recursividad
            driver.get(url)
            
            try: # Obtenemos la url del boton next, este es por si la clase se llama " next"
                tagsN = driver.find_element(By.XPATH, '//a[@class=" next"]') #'//a[@class=" next"]'
                urlsN = tagsN.get_attribute('href')
                # logging.info(urlsN) # Impresion para asegurarse de que esta haciendo iteraciones correctamente
                Categoria(urlsN, category, driver)
            except Exception as a:
                try: # Por si la clase se llama "next"
                    tagsN = driver.find_element(By.XPATH, '//a[@class="next"]') #'//a[@class=" next"]'
                    urlsN = tagsN.get_attribute('href')
                    # logging.info(urlsN) # Impresion para asegurarse de que esta haciendo iteraciones correctamente
                    Categoria(urlsN, category, driver)
                except Exception as e:
                    logging.info(f"Error: $e")
                    logging.info("-----Vacio-----") # Impresion para asegurarse de que esta haciendo iteraciones correctamente
        
        
        # logging.info("funciona")

        # Seccion para configurar Selenium

        #options = webdriver.FirefoxOptions()
        #options.headless = True
        #options.binary_location = r'/snap/bin/firefox'
        #driver = webdriver.Firefox(executable_path=r'/home/flexadmin/JulioCesar/GeckoDriver/geckodriver', options=options)

        options = Options()
        options.add_argument('--headless')
        driver = webdriver.Chrome(options=options)
        driver.implicitly_wait(5)

        # options = webdriver.ChromeOptions()
        # options.headless = True
        # options.binary_location = r'/usr/bin/google-chrome'
        # driver = webdriver.Chrome(executable_path=r'/usr/local/bin/chromedriver', options=options)
        
        #options = webdriver.FirefoxOptions()
        #options.headless = True
        #options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'
        #driver = webdriver.Firefox(executable_path=r'C:\Users\julio\OneDrive\Documentos\Semestre 9\SCRAPYNLP\geckodriver-v0.32.2-win32\geckodriver.exe', options=options)
        #driver.implicitly_wait(5)

        # Cierre de seccion para configurar Selenium



        # logging.info("funciona")
        # Pagina principal
        url = self.url #Ej. "https://www.sears.com.mx/"
        
        driver.get(url)

        # 5 segundos de margen para encontrar el elemento.
        driver.implicitly_wait(5)

        # logging.info("funciona?")
        # Elemento xpath donde se encuentra todas las categorias
        try:
            tags = driver.find_elements(By.XPATH, self.category) #'//li[@class="alone marginTopCa"]/a'
        except Exception as e:
            logging.info(f"Error: $e")


        # logging.info("funcionamos previo")
        for tag in tags: # Se crea una lista de URLs de cada categoria y del nombre de las categorias 
            # logging.info("funcionamos en itera?")
            urls.append(tag.get_attribute('href'))
            categories.append(tag.get_attribute("innerHTML"))   

        # logging.info("funcionamos")
        # Hacemos zip al url y su respectiva categoria
        url_category = zip(urls, categories)

        for url, category in url_category: # Hacemos iteracion por cada categoria conseguida en la pagina
            # logging.info("Funcionaaa?")
            Categoria(url, category, driver)

        driver.quit() # Cerramos el driver

class Sanborns(CarsoSelenium): # Atributos de la pagina Sanborns
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.archive = 'catalog_items_Sanborns.jsonl'

        self.shop = "Sanborns"
        self.url = "https://www.sanborns.com.mx/"
        self.article = '//div[@class="boxProductosCategory"]/article[@class="cardProduct"]/a'
        self.next = '//a[@class="next"]'
        
        self.name = '//h1[@class="h2"]'
        self.price = '//div[@class="pPrice"][text()]'
        self.description = '//div[@class="textDescriptionSears"]'
        self.category = '//li[@class="MenuCategoria_alone__kjNwr MenuCategoria_marginTopCa__d3yzq"]/a'
        self.specifications = '//ul[@class="listAttributesSears"]/li'
        self.classspecifications = ['atributesKeySears','atributesValueSears']
        self.picture = '//div/img[@class="imagenInferiorActual"]'
        self.date = date.today()

class Sears(CarsoSelenium): # Atributos de la pagina Sears
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.archive = 'catalog_items_Sears.jsonl'

        self.shop = "Sears"
        self.url = "https://www.sears.com.mx/"
        self.article = '//div[@class="boxProductosCategory"]/article[@class="cardProduct"]/a'
        self.next = '//a[@class="next"]'
        
        self.name = '//h1[@class="h2"]'
        self.price = '//div[@class="pPrice"][text()]'
        self.description = '//div[@class="textDescriptionSears"]'
        self.category = '//li[@class="MenuCategoria_alone__4K5no MenuCategoria_marginTopCa__NTs63"]/a'
        self.specifications = '//ul[@class="listAttributesSears"]/li'
        self.classspecifications = ['/span[@class="atributesKeySears"]','/span[@class="atributesValueSears"]']
        self.picture = '//div/img[@class="imagenInferiorActual"]'
        self.date = date.today()

class Claro(CarsoSelenium): # Atributos de la pagina ClaroShop
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.archive = 'catalog_items_Claro.jsonl'
        
        self.shop = "ClaroShop"
        self.url = "https://www.claroshop.com/"
        self.article = '//div[@class="boxProductosCategory"]/article[@class="cardProduct"]/a'
        self.next = '//a[@class="next"]'
        
        self.name = '//h1[@class="stylesShopData_h2__A2_Qw"]'
        self.price = '//p[@class="stylesShopData_priceSale__V7S4R"][text()]'
        self.description = '//div[@class="stylesDescription_textDescription__hTECf"]'
        self.category = '//li[@class="MenuCategoria_alone__PQx7S MenuCategoria_marginTopCa__OU9oM"]/a'
        self.specifications = '//ul[@class="stylesSpecification_listAttributes__AI1Zg"]/li'
        self.classspecifications = ['stylesSpecification_atributesKey__qd_DB','stylesSpecification_atributesValue__ke_Y3']
        self.picture = '//div/picture/img[@class="stylesSliderProductoDesktop_imagenInferiorActual__62stf"]'
        self.date = date.today()

            
def date_handler(obj): # Cambio del formato para la fecha
    if hasattr(obj, 'isoformat'):
        return obj.isoformat()
    else:
        raise TypeError(f'Object of type {obj.__class__.__name__} is not JSON serializable')

Claro().parse()

with open("catalog_items_Claro_Copie.json", "w") as f: # Creacion del archivo Json de Claroshop
    json.dump([item.dict() for item in catalog_items], f, default=date_handler)
    
# Vaciamos la lista
catalog_items = []

Sears().parse()

with open("catalog_items_Sears_Copie.json", "w") as f: # Creacion del archivo Json de Sears
    json.dump([item.dict() for item in catalog_items], f, default=date_handler)
    
# Vaciamos la lista
catalog_items = []

Sanborns().parse()

with open("catalog_items_Sanborns_Copie.json", "w") as f: # Creacion del archivo Json de Sanborns
    json.dump([item.dict() for item in catalog_items], f, default=date_handler)
