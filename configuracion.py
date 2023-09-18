# configuracion.py

import telebot
import requests
import time
import json

# Configuraciones iniciales
objetivo_coinjoin = 2
comision_real_ltc = 5000000
comision_real_btc = 18000
comision_hombre_muerto = 50000
comision_bloqueo = 50000
comision_codifica = 50000

# Inicialización del bot
bot = telebot.TeleBot('6284649:AWwb2zdKibE-IY23LU')
usuario = {}
idioma_usuario = "es"