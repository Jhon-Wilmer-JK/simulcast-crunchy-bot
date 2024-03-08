# simulcast-crunchy-bot
un bot que obtiene las ultimas publicaciones de episodios de Crunchyroll y un comando para buscar info de los enlaces de Crunchyroll
importante aclarar que solo es funcional al 100% en SO Ubuntu y similares (no hice la prueba en Windows XD)

- Clone éste repo:
```
git clone https://github.com/Jhon-Wilmer-JK/simulcast-crunchy-bot cr_simulcast_bot/ && cd cr_simulcast_bot
```

- Instalar navegador:
```
sudo apt install chromium-browser
```

- instalar python3
```
sudo apt install python3 python3-pip
```

- instalar selenium:
```
pip install selenium
```

- ejecutar el bot en 2do plano y 24/7:
```
nohup python3 asuna_bot.py > log_bot.txt 2>&1 &
```

- buscar el prceso:
```
ps aux | grep furina_bot.py
```

- terminar el proceso:
```
kill ID_del_proceso
```
**1. Campos requeridos**

- `BOT_TOKEN`: El token de Bot de Telegram que obtuviste de [@BotFather](https://t.me/BotFather). `Fuente`
- `OWNER_ID`: El ID de usuario de Telegram (no el nombre de usuario) del propietario del bot. `Ent`
- `TELEGRAM_API`: esto es para autenticar su cuenta de Telegram para descargar archivos de Telegram. puedes conseguir esto
  de <https://my.telegram.org>. `Ent`
- `TELEGRAM_HASH`: esto es para autenticar su cuenta de Telegram para descargar archivos de Telegram. puedes conseguir esto
  de <https://my.telegram.org>. `Fuente`
