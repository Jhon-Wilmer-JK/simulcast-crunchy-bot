from selenium.webdriver.chrome.webdriver import WebDriver as Chrome
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import multiprocessing
import time


import requests
import os

def guardar_imagen(url, nombre_archivo, ubicacion="cr_img"):
    # Define la ruta completa del archivo
    ruta_completa = os.path.join(ubicacion, nombre_archivo+".jpg")

    # Verifica si la carpeta de ubicación existe, si no, la crea
    if ubicacion and not os.path.exists(ubicacion):
        os.makedirs(ubicacion)
    # Envía una solicitud GET para obtener la imagen
    response = requests.get(url)
    if response.status_code == 200:
        # Guarda la imagen en el disco
        with open(ruta_completa, 'wb') as f:
            f.write(response.content)
            #print(f"La imagen se ha guardado como '{ruta_completa}'")
    else:
        print("Error al descargar la imagen.")
        pass

def analizar_ep_cr(cr_link_ep):
    # Inicializar el navegador
    # Configura las opciones de Chrome
    opciones_chrome = Options()
    opciones_chrome.add_argument('--headless')  #para ocultar chromium
    opciones_chrome.add_argument('--no-sandbox')  #para ocultar chromium
    opciones_chrome.add_argument('--remote-debugging-port=9244')  #para ocultar chromium
    opciones_chrome.add_argument('--disable-gpu')  #para ocultar chromium
    driver = Chrome(options=opciones_chrome)  # Cambia a webdriver.Firefox() si estás usando Firefox
    try:
        try:
            # Abre la URL de Crunchyroll
            driver.get(cr_link_ep)

            # Espera a que la página se cargue completamente
            driver.implicitly_wait(2)
            # Cerrar el banner de cookies si está presente
            try:
                cookies_banner = driver.find_element(By.ID, '_evidon-accept-button')
                cookies_banner.click()  # Puedes intentar hacer clic en el banner para cerrarlo
            except:
                # El banner de cookies no está presente o ya está cerrado
                pass
            time.sleep(2) 

            #guardar la img
            try:
                # Encuentra el elemento de la imagen por su clase o cualquier otro identificador único
                imagen_element = driver.find_element(By.CLASS_NAME, 'content-image__image--7tGlg')
                # Obtiene el atributo 'src' que contiene el enlace de la imagen
                img_link = imagen_element.get_attribute('src')
            except:
                img_link = "https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgtqyo8SNw6H4Hm7_Ioqm2rsgED0sET2MP_VaY3-mZaXxACrBd8OaifjfRLev2JG0pImhw3Wbaj5MMRwEPweeotWSi8zFfPtpFFoPfmwdXNNAFEKQtz0V16R7MA2R6dgHGu1KVelR8KEG2N9PN7XidgkNMdSv1ijWQfW0PPpBIPCZpjdwAIZmsdiEtxxVo/s320/no_image-transformed.jpeg"
                print ("no hay link de imagen oficial")
                pass

            # Desplaza la página hacia abajo para cargar más contenido (puedes ajustar la cantidad de desplazamiento)
            for _ in range(10):
                try:
                    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.DOWN)
                    time.sleep(0.1)  # Espera 0.1 segundos entre cada desplazamiento
                except Exception as e:
                    print(f"Error al desplazarse hacia abajo: {e}")
            
            # Verificar si hay un encabezado de error 404
            try:
                error_header = driver.find_element(By.CLASS_NAME, 'heading--nKNOf')
                if "404 - Página no encontrada" in error_header.text:
                    print("404 - Página no encontrada\n ¡Yuzu dice que aquí no hay nada!")
                    exit()
            except NoSuchElementException:
                print("pagina no encontrado!")
                pass

            # Verificar si el botón "No" está presente y hacer clic en él
            try:
                button_no = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//button[@data-t="reject-btn"]/span[contains(text(), "No")]'))
                )
                button_no.click()
            except:
                pass

            # Hacer clic en el botón "Ver más" si está presente
            try:
                button = WebDriverWait(driver, 2).until(
                    EC.visibility_of_element_located((By.XPATH, '//button[@class="call-to-action--PEidl call-to-action--is-s--xFu35 expandable-section__button--KeiDD" and @data-t="expandable-btn"]'))
                )
                button.click()
            except:
                pass

            # Obtener la información
            try:
                # Título
                titulo_element = driver.find_element(By.XPATH, '//div[@class="current-media-parent-ref"]/a/h4')
                titulo = titulo_element.text
            except NoSuchElementException:
                titulo = "None - No encontrado"

            try:
                # Calificación
                calificacion_element = driver.find_element(By.XPATH, '//div[@class="current-media-parent-ref"]//p[@class="text--gq6o- text--is-m--pqiL- star-rating-short-static__rating--bdAfR"]')
                calificacion = calificacion_element.text
            except NoSuchElementException:
                calificacion = "None - No encontrado"

            try:
                # Número de Calificaciones
                nro_calificaciones_element = driver.find_element(By.XPATH, '//div[@class="current-media-parent-ref"]//p[@class="text--gq6o- text--is-m--pqiL- star-rating-short-static__votes-count--h9Sun"]')
                nro_calificaciones = nro_calificaciones_element.text
            except NoSuchElementException:
                nro_calificaciones = "None - No encontrado"

            try:
                # Número de Episodio
                numero_episodio_element = driver.find_element(By.XPATH, '//h1[contains(@class, "heading--is-family-type-one") and contains(@class, "title")]')
                numero_episodio = numero_episodio_element.text
            except NoSuchElementException:
                numero_episodio = "None - No encontrado"

            try:
                # Detalles2
                detalles_element2 = driver.find_element(By.XPATH, '//div[@class="meta-tags--o8OYw media-tags"]//span[@class="text--gq6o- text--is-m--pqiL- meta-tags__tag--W4JTZ meta-tags__type--is-three--02anH"]')
                detalles_text2 = detalles_element2.text
                detalles2 = f"{detalles_text2} ⧫"
            except NoSuchElementException:
                detalles2 = ""
            try:
                # Detalles
                detalles_element = driver.find_element(By.XPATH, '//div[@class="meta-tags--o8OYw media-tags"]//span[@class="text--gq6o- text--is-m--pqiL- meta-tags__tag--W4JTZ"]')
                detalles_text = detalles_element.text
                detalles = detalles_text
            except NoSuchElementException:
                detalles = "None - No encontrado"

            try:
                # Fecha de lanzamiento erc-current-media-info
                fecha_lanzamiento_element = driver.find_element(By.XPATH, '//div[@class="erc-current-media-info"]//p[@class="text--gq6o- text--is-m--pqiL- release-date"]')
                fecha_lanzamiento = fecha_lanzamiento_element.text
            except NoSuchElementException:
                fecha_lanzamiento = "None - No encontrado"
                
            try:
                # Descripción expandable-section__wrapper--G-ttI expandable-section__wrapper--is-faded--EE4Zg expandable-section__wrapper--is-long--ZL6oO
                descripcion_element = driver.find_element(By.XPATH, '//div[@class="expandable-section__wrapper--G-ttI expandable-section__wrapper--is-faded--EE4Zg expandable-section__wrapper--is-long--ZL6oO"]//p[@class="text--gq6o- text--is-l--iccTo expandable-section__text---00oG"]')
                descripcion = descripcion_element.text
            except NoSuchElementException:
                descripcion = "None - No encontrado"

            try:
                # Audio
                audio_element = driver.find_element(By.XPATH, '//div[@class="details-table__table-row--4eYc5" and @data-t="detail-row-audio-language"]//h5[@data-t="details-table-description"]')
                audio = audio_element.text
            except NoSuchElementException:
                audio = "None - (Tal vez ja-JP)"

            try:
                # Subtítulos
                subtitulos_element = driver.find_element(By.XPATH, '//div[@class="details-table__table-row--4eYc5" and @data-t="detail-row-subtitles-language"]//h5[@data-t="details-table-description"]')
                subtitulos = subtitulos_element.text
            except NoSuchElementException:
                subtitulos = "None - No encontrado"
            
            #enlazar el nombre
            guardar_imagen(img_link, titulo)
            hiper_link = f"<b>➲ Descargar:</b>\n" \
                         f"<a href='https://telegra.ph/download-animes-03-03'>" \
                         f"╭──────────╮\n" \
                         f"│ DOWNLOAD ⇩ │\n" \
                         f"╰──────────╯</a>"

            # Imprimir la información
            print("⛩ <b>Título:</b>", titulo)
            print("📊 <b>Calificación:</b>", calificacion,"★", f"{nro_calificaciones}")
            print("🎬 <b>N° Episodio:</b>", numero_episodio)
            print("👀 <b>Detalles:</b>",f"{detalles2}", detalles)
            print("🔖 <b>Tipo de enlace:</b> Video")
            print("📅 <b>Fecha:</b>", fecha_lanzamiento)
            print("🎙 <b>Audio:</b>", audio)
            print("🗺 <b>Subtítulos:</b>", subtitulos)
            print("🔰 <b>Descripción:</b>", descripcion, "\n")
            #print("➪ Ver:", cr_link_ep)
            print(hiper_link)
            
        except Exception as e:
            print("Se produjo un error:", e)
        #input("Presiona Enter para salir...")
    finally:
        # Cerrar el navegador al finalizar
        driver.quit()

# analizar series de crunchyroll
def analizar_serie_cr(cr_link_serie):
    # Inicializar el navegador
    # Configura las opciones de Chrome
    opciones_chrome = Options()
    opciones_chrome.add_argument('--headless')  #para ocultar chromium
    opciones_chrome.add_argument('--no-sandbox')  #para ocultar chromium
    opciones_chrome.add_argument('--remote-debugging-port=9244')  #para ocultar chromium
    opciones_chrome.add_argument('--disable-gpu')  #para ocultar chromium
    driver = Chrome(options=opciones_chrome)  # Cambia a webdriver.Firefox() si estás usando Firefox
    try:
        try:
            # Abre la URL de Crunchyroll
            driver.get(cr_link_serie)

            # Espera a que la página se cargue completamente
            driver.implicitly_wait(5)
            # Cerrar el banner de cookies si está presente
            try:
                cookies_banner = driver.find_element(By.ID, '_evidon-accept-button')
                cookies_banner.click()  # Puedes intentar hacer clic en el banner para cerrarlo
            except:
                # El banner de cookies no está presente o ya está cerrado
                pass
            time.sleep(2) 
                        
            #guardar la img
            try:
                # Encuentra el elemento de la imagen por su clase o cualquier otro identificador único
                imagen_element = driver.find_element(By.CLASS_NAME, 'content-image__image--7tGlg')
                # Obtiene el atributo 'src' que contiene el enlace de la imagen
                img_link = imagen_element.get_attribute('src')
            except:
                img_link = "https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgtqyo8SNw6H4Hm7_Ioqm2rsgED0sET2MP_VaY3-mZaXxACrBd8OaifjfRLev2JG0pImhw3Wbaj5MMRwEPweeotWSi8zFfPtpFFoPfmwdXNNAFEKQtz0V16R7MA2R6dgHGu1KVelR8KEG2N9PN7XidgkNMdSv1ijWQfW0PPpBIPCZpjdwAIZmsdiEtxxVo/s320/no_image-transformed.jpeg"
                print ("no hay link de imagen oficial")
                pass

            # Desplaza la página hacia abajo para cargar más contenido (puedes ajustar la cantidad de desplazamiento)
            for _ in range(10):
                try:
                    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.DOWN)
                    time.sleep(0.1)  # Espera 0.1 segundos entre cada desplazamiento
                except Exception as e:
                    print(f"Error al desplazarse hacia abajo: {e}")
            
            # Verificar si hay un encabezado de error 404
            try:
                error_header = driver.find_element(By.CLASS_NAME, 'heading--nKNOf')
                if "404 - Página no encontrada" in error_header.text:
                    print("404 - Página no encontrada\n¡Yuzu dice que aquí no hay nada!")
                    exit()
            except NoSuchElementException:
                print("pagina no encontrado!")
                pass

            # Verificar si el botón "No" está presente y hacer clic en él
            try:
                button_no = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//button[@data-t="reject-btn"]/span[contains(text(), "No")]'))
                )
                button_no.click()
            except:
                pass

            # Hacer clic en el botón "Ver más" si está presente
            try:
                button = WebDriverWait(driver, 2).until(
                    EC.visibility_of_element_located((By.XPATH, '//button[@class="call-to-action--PEidl call-to-action--is-s--xFu35 expandable-section__button--KeiDD" and @data-t="expandable-btn"]'))
                )
                button.click()
            except:
                pass

            # Obtener la información
            try:
                # Título
                titulo_element = driver.find_element(By.XPATH, '//div[@class="hero-heading-line"]//h1[@class="heading--nKNOf heading--is-l--zGnGW heading--is-family-type-one--GqBzU title"]')
                titulo = titulo_element.text
            except NoSuchElementException:
                titulo = "None - No encontrado"

            try:
                # Calificación
                calificacion_element = driver.find_element(By.XPATH, '//div[@class="star-rating-average-data--Liuvt"]//span[@class="text--gq6o- text--is-heavy--2YygX text--is-m--pqiL- star-rating-average-data__label--TdvQs"]')
                calificacion = calificacion_element.text
            except NoSuchElementException:
                calificacion = "None - No encontrado"

            try:
                #genero
                # Encuentra todos los elementos small dentro de los enlaces en la clase "badge__text-wrapper--Cku2k"
                genero_elements = driver.find_elements(By.XPATH, '//div[@class="erc-content-genres genres-wrapper"]//small[@class="text--gq6o- text--is-s--JP2oa badge__text--puKze"]')
                
                # Itera sobre los elementos encontrados y extrae el texto de cada uno
                generos = [genero.text for genero in genero_elements]
                
                # Convierte la lista de géneros a una cadena separada por comas
                generos_str = ", ".join(generos)

            except NoSuchElementException:
                generos_str = "None - No encontrado"

            try:
                # Detalles2
                detalles_element2 = driver.find_element(By.XPATH, '//div[@class="erc-series-tags tags"]//div[@class="meta-tags--o8OYw"]//span[@class="text--gq6o- text--is-m--pqiL- meta-tags__tag--W4JTZ meta-tags__type--is-three--02anH"]')
                detalles_text2 = detalles_element2.text
                detalles2 = f"{detalles_text2} ⧫"
            except NoSuchElementException:
                detalles2 = ""
            try:
                # Detalles
                detalles_element = driver.find_element(By.XPATH, '//div[@class="erc-series-tags tags"]//div[@class="meta-tags--o8OYw"]//span[@class="text--gq6o- text--is-m--pqiL- meta-tags__tag--W4JTZ"]')
                detalles_text = detalles_element.text
                detalles = detalles_text
            except NoSuchElementException:
                detalles = "None - No encontrado"

            try:
                # editor
                editor_element = driver.find_element(By.XPATH, '//div[@class="details-table__table-row--4eYc5" and @data-t="detail-row-publisher"]//h5[@data-t="details-table-description"]')
                editor = editor_element.text
            except NoSuchElementException:
                editor = "None - No encontrado"
                
            try:
                # Descripción expandable-section__wrapper--G-ttI expandable-section__wrapper--is-faded--EE4Zg expandable-section__wrapper--is-long--ZL6oO
                descripcion_element = driver.find_element(By.XPATH, '//div[@class="expandable-section__wrapper--G-ttI expandable-section__wrapper--is-faded--EE4Zg expandable-section__wrapper--is-long--ZL6oO"]//p[@class="text--gq6o- text--is-l--iccTo expandable-section__text---00oG"]')
                descripcion = descripcion_element.text
            except NoSuchElementException:
                descripcion = "None - No encontrado"

            try:
                # Audio
                audio_element = driver.find_element(By.XPATH, '//div[@class="details-table__table-row--4eYc5" and @data-t="detail-row-audio-language"]//h5[@data-t="details-table-description"]')
                audio = audio_element.text
            except NoSuchElementException:
                audio = "None - No encontrado"

            try:
                # Subtítulos
                subtitulos_element = driver.find_element(By.XPATH, '//div[@class="details-table__table-row--4eYc5" and @data-t="detail-row-subtitles-language"]//h5[@data-t="details-table-description"]')
                subtitulos = subtitulos_element.text
            except NoSuchElementException:
                subtitulos = "None - No encontrado"

            #enlazar el nombre
            guardar_imagen(img_link, titulo)

            # Imprimir la información
            print("⛩ <b>Título:</b>", titulo)
            print("📊 <b>Calificación:</b>", calificacion, "★")
            print("🏷 <b>Genero:</b>", generos_str)
            print("👀 <b>Detalles:</b>",f"{detalles2}", detalles)
            print("🔖 <b>Tipo de enlace:</b> Serie")
            print("🎥 <b>Editor:</b>", editor)
            print("🎙 <b>Audio:</b>", audio)
            print("🗺 <b>Subtítulos:</b>", subtitulos)
            print("🔰 <b>Descripción:</b>", descripcion)
            #print("➪ Ver:", cr_link_serie)
            
        except Exception as e:
            print("Se produjo un error:", e)
        #input("Presiona Enter para salir...")
    finally:
        # Cerrar el navegador al finalizar
        driver.quit()

def linker(link):
    if link == "https://www.crunchyroll.com" or link == "https://www.crunchyroll.com/" or link == "www.crunchyroll.com" or link == "www.crunchyroll.com/" or link == "crunchyroll.com" or link == "crunchyroll.com/":
        print("Ingrese un enlace de serie o EP de Crunchyroll.")
        exit()
    elif "crunchyroll.com/" in link and "/episode" in link:
        #print("Es un enlace global de Crunchyroll.")
        analizar_ep_cr(link)
    elif "crunchyroll.com/" in link and "/watch/" in link:
        #print("Es un enlace de episodio de Crunchyroll.")
        analizar_ep_cr(link)
    elif "crunchyroll.com/" in link and "/series/" in link:
        #print("Es un enlace de serie de Crunchyroll.")
        analizar_serie_cr(link)
    else:
        print("Ingrese un enlace válido de Crunchyroll.")
        exit()

if __name__ == "__main__":
    cr_link = input()

    # Inicia un nuevo proceso para ejecutar la tarea
    proceso = multiprocessing.Process(target=linker, args=(cr_link,))
    proceso.start()
    proceso.join()
