from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.keys import Keys
import time

def obtener_todas_entradas(driver):
    try:
        cookies_banner = driver.find_element(By.ID, '_evidon-accept-button')
        cookies_banner.click()  # Puedes intentar hacer clic en el banner para cerrarlo
    except:
        # El banner de cookies no está presente o ya está cerrado
        pass
    time.sleep(5) 
    # Desplaza la página hacia abajo para cargar más contenido
    for _ in range(60):
        try:
            driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.DOWN)
            time.sleep(0.1)  # Espera 0.2 segundos entre cada desplazamiento
        except Exception as e:
            print(f"Error al desplazarse hacia abajo: {e}")

    # Haz clic en el botón "Ver más"
        # Hacer clic en el botón "Ver más" si está presente
    try:
        ver_mas_button = driver.find_element(By.CLASS_NAME, 'button--is-type-four--yKPXY')
        ver_mas_button.click()
    except:
        pass

    #########################################################################################
    # Extrae enlaces de episodios (modifica según tu estructura HTML)
    enlaces_episodios = [a.get_attribute('href') for a in driver.find_elements(By.CLASS_NAME, 'playable-release-episode-card-link--y4yXx')]
    names = [a.get_attribute('title') for a in driver.find_elements(By.CLASS_NAME, 'playable-release-episode-card-link--y4yXx')]
    # Extraer el texto de los elementos <span>
    etiquetas_span = driver.find_elements(By.CLASS_NAME, 'release-episode-card-media-type__label--6FnjK')
    textos_span = [span.text for span in etiquetas_span]
    
    # Crear un conjunto para almacenar enlaces únicos,
    enlaces_unicos = set()

    # Crear una lista de tuplas (nombre, episodio, enlace)
    todas_entradas = []
    for enlace, nombre, episodio in zip(enlaces_episodios, names, textos_span):
        # Verificar si el enlace ya ha sido registrado
        if enlace not in enlaces_unicos:
            enlaces_unicos.add(enlace)
            todas_entradas.append((nombre, episodio, enlace))

    return todas_entradas

def obtener_entradas_previas():
    try:
        with open('entradas_previas.txt', 'r') as archivo:
            return set(archivo.read().splitlines())
    except FileNotFoundError:
        return set()

def guardar_entradas_actuales(entradas_actuales):
    with open('entradas_previas.txt', 'w') as archivo:
        for _, name, enlace in entradas_actuales:
            archivo.write(enlace + '\n')

# Configura las opciones de Chrome
opciones_chrome = webdriver.ChromeOptions()
opciones_chrome.add_argument('--headless')  #para ocultar chromium
opciones_chrome.add_argument('--no-sandbox')
opciones_chrome.add_argument('--remote-debugging-port=9222')
opciones_chrome.add_argument('--disable-gpu')

# Inicia el navegador con las opciones de Chrome
driver = webdriver.Chrome(options=opciones_chrome)
try:
    # Abre la URL de Crunchyroll
    driver.get('https://www.crunchyroll.com/es/')

    # Espera a que la página se cargue completamente (puedes ajustar este tiempo según sea necesario)
    driver.implicitly_wait(5)

    entradas_actuales = obtener_todas_entradas(driver)
    entradas_previas = obtener_entradas_previas()

    nuevas_entradas = [entrada for entrada in entradas_actuales if entrada[2] not in entradas_previas]

    if nuevas_entradas:
        #print("Nuevas entradas encontradas:")
        for nombre, episodio, enlace in nuevas_entradas:
            nombre_formateado = nombre.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            print(f"⛩ <b>Título:</b><a href='{enlace}'> <b>{nombre_formateado}</b></a> - {episodio}")
        guardar_entradas_actuales(entradas_actuales)
    else:
        print("No hay nuevas entradas.")

finally:
    # Cierra el navegador al finalizar, incluso si hay excepciones
    driver.quit()
