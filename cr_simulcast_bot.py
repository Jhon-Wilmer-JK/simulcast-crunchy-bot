import subprocess
import logging
import re
import os
from pyrogram import Client as tgClient, filters, enums
import asyncio
from pyrogram.types import InlineQueryResultArticle, InputTextMessageContent

# Definir el TOKEN del bot de Telegram y el ID del grupo
telegram_token = '' #obtener de botfather
TELEGRAM_API = "" #obtener en https://my.telegram.org
TELEGRAM_HASH = "" #obtener en https://my.telegram.org
CANAL_ID = -100 #crunchyroll canal
GRUPO_ID = -100  # Reemplazar con el ID real de tu grupo de pruebas

# Configurar el registro de actividad
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

bot = tgClient("my_bot", api_id=TELEGRAM_API, api_hash=TELEGRAM_HASH, bot_token=telegram_token)

@bot.on_message(filters.command("start"))
async def start_command(client, message):
    user_mention = message.from_user.mention(style="html") if message.from_user else ""
    await message.reply_text(f"{user_mention}¡Hola! Soy un bot en desarrollo.", reply_to_message_id=message.id)

# Maneja las consultas en línea
@bot.on_inline_query()
async def handle_inline_query(client, inline_query):
    if "anime" in inline_query.query.lower():
        # Aquí podrías realizar alguna consulta o búsqueda de resultados
        resultados = [
            "Resultado 1 pruebas",
            "Resultado 2 en beta",
            "Resultado 3 muy pronto"
        ]
        # Construye los resultados de la consulta en línea
        results = [
            InlineQueryResultArticle(
                title=f"Resultado {i}",
                input_message_content=InputTextMessageContent(resultado)
            ) for i, resultado in enumerate(resultados, start=1)
        ]
        # Envía los resultados de la consulta en línea
        await inline_query.answer(results)


@bot.on_message(filters.command("cr_search"))
async def analizar_cr(client, message):
    try:
        if len(message.command) > 1:
            link = message.command[1]
            inicial = await message.reply_text("⌬ <b>Buscando...</b>", reply_to_message_id=message.id)
            process = await asyncio.create_subprocess_shell(
                f'echo "{link}" | python3 analizador_cr_priv.py',
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            stdout, stderr = await process.communicate()
            if stdout:
                print(stdout.decode())
                patron_titulo = r"<b>Título:</b>\s(.+)"
                resultado = re.search(patron_titulo, stdout.decode())
                if resultado:
                    titulo = resultado.group(1)
                    imagen_path = f"cr_img/{titulo}.jpg"
                    print(imagen_path)
                    if os.path.isfile(imagen_path):
                        await inicial.delete()
                        await client.send_photo(chat_id=message.chat.id, photo=imagen_path, caption=stdout.decode(), reply_to_message_id=message.id)
                        os.remove(imagen_path)
                    else:
                        await inicial.delete()
                        await message.reply_text(stdout.decode(), reply_to_message_id=message.id, disable_web_page_preview=True)
            elif stderr:
                logging.error(stderr.decode())
                await inicial.delete()
                await message.reply_text("Espera 25s y vuelve a intentar", reply_to_message_id=message.id)
        else:
            await message.reply_text(f"Por favor, proporciona el <code>enlace</code>", reply_to_message_id=message.id)
    except Exception as e:
        logging.error(f"Error al ejecutar el script analizador_cr: {e}")

async def analizar_crunchyroll(link, datoss, output_text, client):
    try:
        process = await asyncio.create_subprocess_shell(
            f'echo "{link}" | python3 analizador_cr.py',
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        if stdout:
            sout = stdout.decode()

            # Dividir el texto en líneas
            lineas = sout.split('\n')
            # Eliminar la primera línea
            texto_sin_primera_linea = '\n'.join(lineas[1:])
            textos = f"{output_text}{texto_sin_primera_linea}"
            #textosss = f"{output_text}{sout}"
            print(textos)
            #print(textosss)
            patron_titulo = r"<b>Título:</b>\s(.+)"
            resultado = re.search(patron_titulo, sout)
            if resultado:
                titulo = resultado.group(1)
                imagen_path = f"cr_img/{titulo}.jpg"
                print(imagen_path)
                if os.path.isfile(imagen_path):
                    await datoss.delete()
                    await client.send_photo(chat_id=CANAL_ID, photo=imagen_path, caption=textos)
                    os.remove(imagen_path)
                else:
                    await datoss.delete()
                    await bot.send_message(CANAL_ID, textos, disable_web_page_preview=True)
        elif stderr:
            logging.error(stderr.decode())
    except Exception as e:
        logging.error(f"Error al ejecutar el script analizador_cr.py: {e}")

async def verificar_nuevas_entradas():
    try:
        process = await asyncio.create_subprocess_shell(
            'python3 scraping_crunchy.py',
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        if stdout:
            output_text = stdout.decode()
            print(output_text)
            if 'No hay nuevas entradas.' not in output_text:
                datoss = await bot.send_message(CANAL_ID, output_text, disable_web_page_preview=True)
                urls = re.findall(r"<a\s+href='(.*?)'", output_text)
                print(urls[0])
                for url in urls:
                    await analizar_crunchyroll(url, datoss, output_text, bot)
                    await asyncio.sleep(5) 
                logging.info("Nuevas entradas enviadas al grupo.")
            else:
                logging.info("No hay nuevas entradas.")
        elif stderr:
            logging.error(stderr.decode())
    except Exception as e:
        logging.error(f"Error inesperado: {e}")

async def main3():
    while True:
        await verificar_nuevas_entradas()
        await asyncio.sleep(60)  

def main() -> None:
    try:
        print('Iniciando el Bot...')
        if not bot.is_initialized:
            bot.start()
            print('Bot iniciado correctamente. Esperando mensajes...')
            asyncio.get_event_loop().run_until_complete(main3())  
        else:
            print('El bot ya está conectado.')
    except KeyboardInterrupt:
        print('Se presionó Ctrl+C. Deteniendo el bot...')
        bot.stop()
    except Exception as e:
        print(f"Error al iniciar el bot: {str(e)}")
if __name__ == '__main__':
    main()

