# simulcast-crunchy-bot
un bot que obtiene las ultimas publicaciones de episodios de Crunchyroll y un comando para buscar info de los enlaces de Crunchyroll
importante aclarar que solo es funcional al 100% en SO Ubuntu y similares

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
