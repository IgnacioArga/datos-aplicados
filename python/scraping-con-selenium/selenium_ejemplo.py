
# Automatización con Selenium: click en botón y captura de precio

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

# Configurar opciones del navegador
options = Options()
options.add_argument('--headless')  # Ejecutar en segundo plano, si quieres ver 
                                    # al navegador ejecutando en vivo no correr esta línea
options.add_argument('--disable-gpu')

# Inicializar navegador
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# URL de ejemplo (reemplazar por la real)
url = "https://www.ejemplo.com/producto"
driver.get(url)
time.sleep(2)  # Esperar que cargue la página

# Hacer click en un botón (ejemplo: mostrar precio, aceptar cookies, etc.)
try:
    boton = driver.find_element(By.ID, "ver-precio")  # Cambiar selector según HTML
    boton.click()
    time.sleep(2)  # Esperar resultado tras click
except:
    print("No se encontró el botón o no fue necesario hacer click")

# Obtener el precio (modificar selector según el sitio real)
try:
    precio = driver.find_element(By.CLASS_NAME, "precio-producto").text
    print(f"Precio encontrado: {precio}")
except:
    print("No se encontró el precio")

# Cerrar el navegador
driver.quit()

