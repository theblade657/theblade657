
import telebot
import threading
from cryptos import *
from bitcoin import *
import requests
import json
from statistics import median
import datetime
from datetime import datetime
from hdwallet import HDWallet
from hdwallet.utils import generate_entropy
from hdwallet.symbols import BTC as SYMBOL
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from telebot.types import ForceReply
from telebot.apihelper import ApiTelegramException
import time
import qrcode
from io import BytesIO
from PIL import Image
#from telebot.types import ReplyKeyboardMarkup, ForceReply, BotCommand
bot = telebot.TeleBot('6284649:AWwb2zdKibE-IY23LU')
usuario={}
import bech32
import hashlib
import base64
from bit import *
from bit import Key, MultiSig, wif_to_key
from bit.format import bytes_to_wif
from bit.network.services import *
from bit.network.rates import *

        
        
objetivo_coinjoin=2
comision_real_ltc=5000000
comision_real_btc=18000
comision_hombre_muerto=50000
comision_bloqueo=50000
comision_codifica=50000
"""# Parametría

!pip install cryptos
"""

"""def generando_entropia(idioma="english",fuerza=256):
  # Choose strength 128, 160, 192, 224 or 256
  STRENGTH: int = fuerza  # Default is 128
  # Choose language english, french, italian, spanish, chinese_simplified, chinese_traditional, japanese or korean
  LANGUAGE: str = idioma  # Default is english
  # Generate new entropy hex string
  ENTROPY: str = generate_entropy(strength=STRENGTH)
  return ENTROPY
"""  
def generando_billeteras_keys(entropia='b331ddcec575414f1f6dff77d032090',passphrase_='bot_telegram',simbolo='BTC',idioma='english',indice=0,passphrase_1='',passphrase_2='', texto_a_anadir=''):
  # Secret passphrase for mnemonic
  PASSPHRASE: Optional[str] = passphrase_+passphrase_1+passphrase_2
   # Initialize Bitcoin mainnet HDWallet
  hdwallet: HDWallet = HDWallet(symbol=simbolo, use_default_path=True)
  # Get Bitcoin HDWallet from entropy
  # Determina cuántos caracteres deseas reemplazar al final  
  num_caracteres_a_reemplazar = len(texto_a_anadir)
    # Reemplaza los últimos caracteres de la cadena
  if num_caracteres_a_reemplazar>0:
    entropia_nueva = entropia[:-num_caracteres_a_reemplazar] + texto_a_anadir
  else:     
    entropia_nueva=entropia
  hdwallet.from_entropy(
      entropy=entropia_nueva, language=idioma, passphrase=PASSPHRASE
  )
  direcciones={}
  billetera_info = {
        "Symbol": hdwallet.symbol(),
        "mnemonic": hdwallet.mnemonic(),
        "passphrase": hdwallet.passphrase(),
        "root_xprivate_key": hdwallet.root_xprivate_key(),
        "xpublic_key": hdwallet.xpublic_key(),
        "root_xpublic_key": hdwallet.root_xpublic_key(),
        "public_key": hdwallet.public_key(),
        "wif": hdwallet.wif(),
        "path": hdwallet.path(),
        "finger_print": hdwallet.finger_print(),
        "p2wpkh": hdwallet.p2wpkh_address()
    }
  """for address_index in range(1):
      # Drive Ethereum BIP44HDWallet
      hdwallet.clean_derivation()
      hdwallet.from_path(path="m/44'/0'/0'/0/"+str(address_index))
      # Print address_index, path, address and private_key
      address = hdwallet.p2wpkh_address()
      direcciones[address_index] = f"{address}"
      # Clean derivation indexes/paths
      hdwallet.clean_derivation()
    # Devolver el diccionario"""
  return billetera_info

billetera_btc = generando_billeteras_keys(texto_a_anadir=str(4218039),passphrase_=str('theblade'), simbolo=str('BTC'))  # Generar la billetera correspondiente
billetera_ltc = generando_billeteras_keys(texto_a_anadir=str(4218039),passphrase_=str('theblade'), simbolo=str('LTC'))  # Generar la billetera correspondiente
         
coin_join_0_01B = {}
coin_join_0_05B = {}
coin_join_0_1B = {}
coin_join_0_2B = {}
coin_join_0_5B = {}
coin_join_1B = {}
coin_join_1L = {}
coin_join_5L = {}
coin_join_10L = {}
coin_join_20L = {}
coin_join_50L = {}
coin_join_100L = {}
diccionarios_coinjoin_BTC = [coin_join_0_05B, coin_join_0_01B, coin_join_0_1B, coin_join_0_2B, coin_join_0_5B, coin_join_1B]
diccionarios_coinjoin_LTC = [coin_join_1L, coin_join_5L, coin_join_10L, coin_join_20L, coin_join_50L, coin_join_100L]


# Lista de URLs de las APIs en el orden deseado
api_urls_BTC = [
    ('https://mempool.space/api/v1/fees/recommended', 'mempool'),
    ('https://api.blockchain.info/mempool/fees', 'blockchain'),
    ('https://blockstream.info/api/fee-estimates', 'blockstream'),
    ('https://bitcoiner.live/api/fees/estimates/latest', 'bitcoiner')
]
api_urls_LTC = [
    ('https://litecoinspace.org/api/v1/fees/recommended', 'mempool')
]
# Diccionario para almacenar las tarifas de cada API por categoría
tarifas_por_categoria = {
    'alta': [],
    'media': [],
    'baja': []
}

# Diccionario para almacenar las tarifas medias por byte
sats_x_byte = {
    'alta': 20,
    'media': 10,
    'baja': 1
}

# Función para obtener la tarifa según la prioridad
def obtener_tarifas(data, api_name):
    tarifas = {}
    if api_name == 'mempool':
        tarifas['alta'] = data['fastestFee']
        tarifas['media'] = data['halfHourFee']
        tarifas['baja'] = data['economyFee']
    elif api_name == 'blockchain':
        tarifas['alta'] = data['priority']
        tarifas['media'] = data['regular']
        tarifas['baja'] = data['limits']['min']
    elif api_name == 'blockstream':
        tarifas['alta'] = data['2']
        tarifas['media'] = data['25']
        tarifas['baja'] = data['144']
    elif api_name == 'bitcoiner':
        tarifas['alta'] = data['estimates']['30']['sat_per_vbyte']
        tarifas['media'] = data['estimates']['120']['sat_per_vbyte']
        tarifas['baja'] = data['estimates']['360']['sat_per_vbyte']
    return tarifas

# Función para obtener y calcular las tarifas medias por byte
def obtener_y_calcular_tarifas(lista_url):
    for url, api_name in lista_url:
        try:
            response = requests.get(url)
            data = response.json()

            # Verificar si la API proporcionó datos
            tarifas = obtener_tarifas(data, api_name)

            for prioridad, tarifa in tarifas.items():
                if tarifa is not None:
                    tarifas_por_categoria[prioridad].append(tarifa)

        except Exception as e:
            continue

    # Calcular la media por categoría
    for prioridad, tarifas in tarifas_por_categoria.items():
        if len(tarifas) > 0:
            media = int(sum(tarifas) / len(tarifas))
            sats_x_byte[prioridad] = media

    return sats_x_byte

# Mostrar los valores de tarifas medias por byte
def mostrar_valores_tarifas(lista_url):
    tarifas = obtener_y_calcular_tarifas(lista_url)
    return tarifas


def calcular_costo_por_firmante(tamano_transaccion_total, tarifa_total, firmantes):
    costo_por_firmante = {}

    # Calcular el costo para cada firmante en función del número de inputs y outputs
    for firmante, (inputs, outputs) in firmantes.items():
        tamano_firmante = (inputs * 148) + (outputs * 34) + 10 + inputs
        porcentaje_contribucion = tamano_firmante / tamano_transaccion_total
        tarifa_firmante = porcentaje_contribucion * tarifa_total
        costo_por_firmante[firmante] = tarifa_firmante

    return costo_por_firmante

def calcular_tamanio_transaccion(inputs, outputs):
    tamaño = (inputs * 148) + (outputs * 34) + 10 + inputs
    return tamaño
    

def obtener_informacion_direccion(direccion, criptomoneda):
    time.sleep(1)
    if criptomoneda == 'BTC':
        url = f"https://mempool.space/api/address/{direccion}"
    elif criptomoneda == 'LTC':
        url = f"https://litecoinblockexplorer.net/api/address/{direccion}"
    else:
        return (-1,-1,-1)
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if criptomoneda == 'BTC':
            saldo_actual = data['chain_stats']['funded_txo_sum'] - data['chain_stats']['spent_txo_sum']
            saldo_pendiente = data['mempool_stats']['funded_txo_sum'] - data['mempool_stats']['spent_txo_sum']
            transacciones_entrada = data['chain_stats']['funded_txo_count']
        elif criptomoneda == 'LTC':
            saldo_actual = float(data['balance']) * 1e8
            saldo_pendiente = float(data['unconfirmedBalance']) * 1e8
            transacciones_entrada = data['txApperances']
        return saldo_actual, saldo_pendiente, transacciones_entrada
    else:
        return (-1,-1,-1)

      
def generar_lista_billeteras(id_usuario, passphrase, moneda, message):        
    lista_billeteras = []
    saldo_direccion = []
    i=1
    s=1
    if moneda=='BTC':
        m=1
    else:
        m=3
    while True:
        billetera = generando_billeteras_keys(texto_a_anadir=str(id_usuario),passphrase_=str(passphrase), passphrase_1=str(i), simbolo=str(moneda))  # Generar la billetera correspondiente
        datos_direccion=obtener_informacion_direccion(billetera['p2wpkh'], moneda)
        if datos_direccion[2] == 0:
            if s==5:
                break
            else:
                s=s+1
        if datos_direccion[0] > 0:
            lista_billeteras.append(billetera)  # Agregar la billetera a la lista
            saldo_direccion.append(datos_direccion[0])
        i=i+1
    return lista_billeteras, saldo_direccion


"""def generar_lista_billeteras_de_coinjoin(id_usuario, passphrase, numero, moneda):
    lista_billeteras = []
    saldo_direccion = []
    if moneda=='BTC':
        m=1
    else:
        m=3
    for i in range(1, numero+1):
        billetera = generando_billeteras_keys(texto_a_anadir=str(id_usuario),passphrase_=str(passphrase), passphrase_1=str(i), simbolo=str(moneda))  # Generar la billetera correspondiente
        print(billetera['p2wpkh'])
        if count(l.unspent(billetera['p2wpkh'])) > 0:
            lista_billeteras.append(billetera)  # Agregar la billetera a la lista   
            datos_direccion=obtener_informacion_direccion(billetera['p2wpkh'], moneda)
            saldo_direccion.append(datos_direccion[0])        
    return lista_billeteras, saldo_direccion
"""    
def dividir_saldo_en_trozos(saldo, valor_trozo, id_usuario, passphrase, moneda):
    diccionario = {}     
    if moneda=='BTC':
        m=1
        dust=5000
        fee_mineria=comision_real_btc+10000
    else:
        m=3
        dust=50000
        fee_mineria=comision_real_ltc+200000
    i = 1
    j = 1
    saldo_actual = saldo-fee_mineria
    if saldo_actual < valor_trozo:
        resto = int(round(saldo_actual, 8) )
        diccionario['resto'] = resto
        return diccionario
    while saldo_actual >= valor_trozo:
        time.sleep(1)
        billetera=generando_billeteras_keys(texto_a_anadir=str(id_usuario),passphrase_=str(passphrase), passphrase_1=str(i), simbolo=str(moneda))
        if count(l.unspent(billetera['p2wpkh'])) == 0:
                diccionario[j] = billetera['p2wpkh']
                saldo_actual -= valor_trozo                
                j += 1                
        i += 1
    resto = int(round(saldo_actual, 8) )
    diccionario['resto'] = resto
    return diccionario

def validar_direccion_bitcoin(address, moneda):
    # Reemplaza la dirección válida por una dirección inválida
    if moneda=='BTC':
        url = f"https://mempool.space/api/address/{address}"
    if moneda=='LTC':
        url = f"https://litecoinspace.org/api/address/{address}"
    
    

    # Realiza la solicitud HTTP GET
    response = requests.get(url)
    # Verifica si la respuesta contiene "Invalid Bitcoin address"
    if "Invalid Bitcoin address" in response.text:
        return False
    else:
        return True


def mirar_coinjoin(message):
    buttons = []
    mixer_reservados = {}
    i = 1
    red=usuario[message.chat.id]['red']
    if  red == 'BTC':
        criptomoneda = 'BTC'
        billetera = 1
    elif red == 'LTC':
        criptomoneda = 'LTC'
        billetera = 3
    coin_joins_activos, saldos=generar_lista_billeteras(message.chat.id, usuario[message.chat.id]['passphrase'], red, message)    
    elementos = {}  # Diccionario para almacenar los elementos con nombres dinámicos
    for i, elemento in enumerate(coin_joins_activos):
        print(elemento)
        nombre_direcc = 'direcc_btc_' + str(i)
        nombre_llave_hex = 'llave_hex_' + str(i)
        saldo='saldos_'+str(i) 
        elementos[nombre_direcc] = elemento['p2wpkh']
        elementos[nombre_llave_hex] = elemento['wif']
        elementos[saldo] = saldos[i]
        button_text = "✔️ CoinJoin de {} {}".format(elementos['saldos_'+str(i)]/1e8, criptomoneda)
        buttons.append([InlineKeyboardButton(text=button_text, callback_data="coinjoin_" + str(i))])    
    usuario[message.chat.id]['coinjoin']=elementos    
    if len(coin_joins_activos) > 0:
        for clave, valor in mixer_reservados.items():
            llave = valor['llave_CJ']
            direccion = valor['direccion_CJ']
            saldo = valor['datos'][0]
            button_text = "✔️ CoinJoin de {} {}".format(saldo/1e8, criptomoneda)
            buttons.append([InlineKeyboardButton(text=button_text, callback_data="coinjoin_" + str(clave))]) 
        if buttons:
            reply_markup = InlineKeyboardMarkup(buttons + [[button_inicio]])
            bot.send_message(message.chat.id, "Selecciona el CoinJoin para poder mostrarte toda la información", reply_markup=reply_markup)
    else:
        texto_html = 'No tienes ningún CoinJoin' + '\n'
        markup = InlineKeyboardMarkup([[button_inicio]])
        bot.send_message(message.chat.id, texto_html, parse_mode="html", reply_markup=markup)


def billetera(id_usuario, passphrase=""):
    billetera_=generando_billeteras_keys(texto_a_anadir=str(id_usuario),passphrase_=str(passphrase), simbolo=str(usuario[id_usuario]['red']))
    money_confirmado,money_NO_confirmado,numero_transacciones=obtener_informacion_direccion(billetera_['p2wpkh'],usuario[id_usuario]['red'])
    mnemonic=billetera_['mnemonic']
    origen=billetera_['p2wpkh']
    llave_hex=billetera_['wif']
    return money_confirmado,mnemonic,origen,money_NO_confirmado,llave_hex, numero_transacciones



# Función que envía el mensaje a cada ID de la lista
def send_message_to_ids(id_list, message_text):
    for id in id_list:
        bot.send_message(id, message_text)
        
def mis_reservas(message):
    buttons = []
    mixer_reservados = {}
    i = 1
    if usuario.get(message.chat.id, {}).get('red') == 'BTC':
        criptomoneda = 'BTC'
        billetera = 1
    elif usuario.get(message.chat.id, {}).get('red') == 'LTC':
        criptomoneda = 'LTC'
        billetera = 3

    while True:
        generando = generate_keys('mixer', 'mixer', 1, i)
        generando_condiciones = generate_keys('mixer', 'mixer', 7, i)
        mis_reservas_confirmadas = generate_keys(message.chat.id, i)
        datos_direccion = obtener_informacion_direccion(mis_reservas_confirmadas[billetera], criptomoneda)
        condiciones = obtener_informacion_direccion(generando_condiciones[billetera], criptomoneda)
        cuantos_hay = obtener_informacion_direccion(generando[billetera], criptomoneda)
        i += 1

        try:
            if datos_direccion[2] == 0:
                break
        except:
            break

        if datos_direccion[0] > 0:
            mixer_reservados[i] = {}
            mixer_reservados[i]['reserva'] = datos_direccion[0]
            mixer_reservados[i]['condiciones'] = condiciones[0]
            mixer_reservados[i]['cuantos_hay'] = cuantos_hay[2]

    if len(mixer_reservados) > 0:
        for clave, valor in mixer_reservados.items():
            reserva = valor['reserva']
            condiciones = valor['condiciones']
            cuantos_hay = valor['cuantos_hay']

            if criptomoneda == 'LTC':
                reserva = int(reserva / 10)
            
            datos = diccionario_mixer[reserva]

            if cuantos_hay < datos[0]:
                button_text = "⏳ Mixer para {} billeteras, tamaño {} {}. Completado al {:.2f}%".format(datos[0], datos[1], criptomoneda, (cuantos_hay / datos[0]) * 100)
                buttons.append([InlineKeyboardButton(text=button_text, callback_data="volver_inicio")])
            else:
                button_text = "✔️ YA Disponible mixer para {} billetereras, tamaño {} {}".format(datos[0], datos[1], criptomoneda)
                buttons.append([InlineKeyboardButton(text=button_text, callback_data="muestra_mixer_" + str(reserva))])

        if buttons:
            reply_markup = InlineKeyboardMarkup(buttons + [[button_inicio]])
            bot.send_message(message.chat.id, "Selecciona la moneda que quieras recuperar:", reply_markup=reply_markup)
    else:
        texto_html = 'No tienes ningún mixer reservado' + '\n'
        markup = InlineKeyboardMarkup([[button_inicio]])
        bot.send_message(message.chat.id, texto_html, parse_mode="html", reply_markup=markup)
        
def envio_fuera(message):
  #bot.delete_message(message.chat.id, message.message_id )
  money=obtener_informacion_direccion(usuario[message.chat.id]['direccion'], usuario[message.chat.id]['red'])[0]
  
  if money > 0:
            msg = bot.send_message(message.chat.id, 'Indica la dirección donde quieres que se te envien los fondos\n\n⚠️⚠️ la dirección compruébala 3 veces, los fondos enviados no se pueden recuperar \n\n ✔️ En el siguiente paso te muestro la información para que lo revises ️')
            bot.register_next_step_handler(msg, confirmacion_envio_fuera)
  else:
            markup = InlineKeyboardMarkup([[button_inicio]])
            msg = bot.send_message(message.chat.id, 'Actualmente no tienes saldo confirmado en tu cuenta', reply_markup=markup)


def confirmacion_envio_fuera(message):


    if message.text:
          usuario[message.chat.id]['direccion_envio']= message.text
          red=usuario[message.chat.id]['red']
          destino=usuario[message.chat.id]['direccion_envio']
          saldo=usuario[message.chat.id]['money']
          llave=usuario[message.chat.id]['llave_hex']
          direccion=usuario[message.chat.id]['direccion']
            
            #simulo tx para calcular la tarifa:
          
          if red=='BTC':
            m=1
            fee_sats=mostrar_valores_tarifas(api_urls_BTC)
          if red=='LTC':
            m=3
            fee_sats=mostrar_valores_tarifas(api_urls_LTC)
        
                    
          try:
            n_inputs=count(l.unspent(direccion))
            n_outputs=1
            tamanio=calcular_tamanio_transaccion(n_inputs, n_outputs)  
            
            fee_por_defecto=int((tamanio*fee_sats)*0.7)
            fee_por_lento=int(tamanio*fee_sats)
            fee_por_rapido=int(tamanio*fee_sats_r)
            
          
          except:
            bot.send_message(message.chat.id, 'No hay saldo disponible en esa dirección')
            cmd_start(message)   
          
          usuario[message.chat.id]['fee_min']=fee_por_defecto
          if red == 'BTC':
                try:
                    fee_mineria=usuario[message.chat.id]['fee_min']
                except:
                    fee_mineria = fee_por_defecto
                url=f'https://mempool.space/es/tx/'
          elif red == 'LTC':
                try:
                    fee_mineria=usuario[message.chat.id]['fee_min']
                except:
                    fee_mineria = fee_por_defecto
                url=f'https://explorer.litecoin.net/tx/'
          
          markup = InlineKeyboardMarkup([[button_ok] , [button_modificar,button_cambio_fee], [button_inicio]])
              #muestra resumen por pantalla:
          texto_html = '<b>📊 Resumen de la transacción </b>' + '\n'
          texto_html+= '########################### ' + '\n'
          texto_html+= '📬 Dirección envío: '+ '\n'
          texto_html+= usuario[message.chat.id]['direccion_envio']+ '\n'
          texto_html+= '💸 '+ str(usuario[message.chat.id]['red']) +' que se envían: '  + '\n'
          
          texto_html+= str(int(usuario[message.chat.id]['money'])/1e8)+' '+str(usuario[message.chat.id]['red']) + '\n'
          
          texto_html+= '💰 fee de minería: '+ '\n'
          texto_html+= str(fee_mineria) + ' sats'+ '\n'
          texto_html+= 'Si te corre prisa la transacción modifica la cifra, te pongo las fees actuales:'+ '\n'
          texto_html+= 'transacción lenta:'+str(fee_por_lento)+ ' sats'+ '\n'
          texto_html+= 'transacción rápida:'+str(fee_por_rapido)+ ' sats'+ '\n' 
          texto_html+= '########################### ' + '\n'

          msg=bot.send_message(message.chat.id,texto_html, parse_mode="html", reply_markup=markup)
def cambio_fee_mineria(message):
            msg = bot.send_message(message.chat.id, 'Indica un número entero > 500 \n será la fee de minería aplicada y se descontará de tu UTXO')
            bot.register_next_step_handler(msg, confirmacion_envio_fuera_mineria)
  
def confirmacion_envio_fuera_mineria(message):  
    if usuario.get(message.chat.id, {}).get('red')=='BTC':
            objetivo=500
    if usuario.get(message.chat.id, {}).get('red')=='LTC':
            objetivo=100
    try:
        numero_entero = int(message.text)
        if numero_entero>objetivo:
              usuario[message.chat.id]['fee_min']=numero_entero
              red=usuario[message.chat.id]['red']
              markup = InlineKeyboardMarkup([[button_ok] , [button_modificar,button_cambio_fee], [button_inicio]])
                  #muestra resumen por pantalla:
              texto_html = '<b>📊 Resumen de la transacción </b>' + '\n'
              texto_html+= '########################### ' + '\n'
              texto_html+= '📬 Dirección envío: '+ '\n'
              texto_html+= usuario[message.chat.id]['direccion_envio']+ '\n'
              texto_html+= '💸 '+ str(usuario[message.chat.id]['red']) +' que se envían: '  + '\n'
              
              texto_html+= str(int(usuario[message.chat.id]['money'])/1e8)+' '+str(usuario[message.chat.id]['red']) + '\n'
              
              texto_html+= '💰 fee de minería: '+ '\n'
              texto_html+= str(usuario[message.chat.id]['fee_min']) + ' sats'+ '\n'
              texto_html+= 'Si te corre prisa la transacción modifica la cifra, presionando el botón'+ '\n'
              texto_html+= '########################### ' + '\n'

              msg=bot.send_message(message.chat.id,texto_html, parse_mode="html", reply_markup=markup)
        else:
            bot.reply_to(message, "El valor ingresado es menor de "+ str(objetivo) +". Por favor, intenta nuevamente.")
            bot.register_next_step_handler(message, confirmacion_envio_fuera_mineria)       

        
    except ValueError:
            # Si no se puede convertir a entero, solicitas nuevamente el número
            bot.reply_to(message, "El valor ingresado no es un número entero. Por favor, intenta nuevamente.")
            bot.register_next_step_handler(message, confirmacion_envio_fuera_mineria)       

def enviando_fuera_confirmado(message):
      red=usuario[message.chat.id]['red']
      if red == 'BTC':
            try:
                fee_mineria=usuario[message.chat.id]['fee_min']
            except:
                fee_mineria = usuario[message.chat.id]['fee_mincj']
            url=f'https://mempool.space/es/tx/'
      elif red == 'LTC':
            try:
                fee_mineria=usuario[message.chat.id]['fee_min']
            except:
                fee_mineria = usuario[message.chat.id]['fee_mincj']
            url=f'https://explorer.litecoin.net/tx/'
      destino=usuario[message.chat.id]['direccion_envio']
      saldo=usuario[message.chat.id]['money']
      llave=usuario[message.chat.id]['llave_hex']
      direccion=usuario[message.chat.id]['direccion']
      
      try:
        envio=l.send(llave,direccion,destino,saldo-fee_mineria,fee=fee_mineria)
        button_operacion = InlineKeyboardButton('Ver transacción', url=url+envio)

        texto_html = 'Satoshis enviados' + '\n'
        texto_html+= '👋 Gracias por usar el CoinJoin BTC_Bot' + '\n'
        markup = InlineKeyboardMarkup([[button_operacion], [button_inicio]])
        bot.send_message(message.chat.id, texto_html, parse_mode="html", reply_markup=markup)
      except:
        texto_html = 'Satoshis NO enviados' + '\n'
        texto_html+= 'Prueba otra vez, seguramente ya lo has enviado. También puede ser que la fee de minería sea muy baja' + '\n'
        markup = InlineKeyboardMarkup([[button_inicio]])
        bot.send_message(message.chat.id, texto_html, parse_mode="html", reply_markup=markup)

      

def envio_fuera_cj(message):
  #bot.delete_message(message.chat.id, message.message_id )
  cuenta_cj=usuario[message.chat.id]['coinjoin']
  
  i=usuario[message.chat.id]['clave']
    
  if usuario.get(message.chat.id, {}).get('red')=='BTC':
            m=1
            add='direcc_btc_'+str(i)
  if usuario.get(message.chat.id, {}).get('red')=='LTC':
            m=3
            add='direcc_ltc_'+str(i)
  money=obtener_informacion_direccion(cuenta_cj[add], usuario[message.chat.id]['red'])[0]
  
  if money > 0:
            msg = bot.send_message(message.chat.id, 'Indica la dirección donde quieres que se te envien los fondos\n\n⚠️⚠️ la dirección compruébala 3 veces, los fondos enviados no se pueden recuperar \n\n ✔️ En el siguiente paso te muestro la información para que lo revises ️')
            bot.register_next_step_handler(msg, confirmacion_envio_fuera_cj)
  else:
            markup = InlineKeyboardMarkup([[button_inicio]])
            msg = bot.send_message(message.chat.id, 'Actualmente no tienes saldo confirmado en tu cuenta', reply_markup=markup)


def confirmacion_envio_fuera_cj(message):
    usuario[message.chat.id]['direccion_envio']= message.text
    i=usuario[message.chat.id]['clave']
    cuenta_cj=usuario[message.chat.id]['coinjoin']
    llave=cuenta_cj['llave_hex_'+str(i)]
    saldo=cuenta_cj['saldos_'+str(i)]
    red=usuario[message.chat.id]['red']
    
    if red=='BTC':
        m=1
        add='direcc_btc_'+str(i)
        fee_sats=mostrar_valores_tarifas(api_urls_BTC)
    if red=='LTC':
        m=3
        add='direcc_ltc_'+str(i)
        fee_sats=mostrar_valores_tarifas(api_urls_LTC)
    
                
    direccion=cuenta_cj[add]    
    #outputs={'value': saldo, 'address': usuario[message.chat.id]['direccion_envio']}    
    #simulo tx para calcular la tarifa:
    try:
        n_inputs=count(l.unspent(direccion))
        n_outputs=1
        tamanio=calcular_tamanio_transaccion(n_inputs, n_outputs)  
        
        fee_por_defecto=int((tamanio*fee_sats)*0.7)
        fee_por_lento=int(tamanio*fee_sats)
        fee_por_rapido=int(tamanio*fee_sats_r)
    except:
        bot.send_message(message.chat.id, 'No hay saldo disponible en esa dirección')
        mirar_coinjoin(message)   
    #simulo tx para calcular la tarifa:
    
    usuario[message.chat.id]['fee_mincj']=fee_por_defecto
    if usuario.get(message.chat.id, {}).get('red')=='BTC':
                try:
                    fee_mineria=usuario[message.chat.id]['fee_mincj']
                except:
                    fee_mineria = fee_por_defecto
                m=1
                add='direcc_btc_'+str(i)
    if usuario.get(message.chat.id, {}).get('red')=='LTC':
                try:
                    fee_mineria=usuario[message.chat.id]['fee_mincj']
                except:
                    fee_mineria = fee_por_defecto
                m=3
                add='direcc_ltc_'+str(i)
                
    if message.text:
          usuario[message.chat.id]['direccion_envio']= message.text
          markup = InlineKeyboardMarkup([[button_ok_cj] , [button_modificar_dire_cj, button_cambio_fee_cj], [button_inicio]])
              #muestra resumen por pantalla:
          texto_html = '<b>📊 Resumen de la transacción </b>' + '\n'
          texto_html+= '########################### ' + '\n'
          texto_html+= '📬 Dirección envío: '+ '\n'
          texto_html+= usuario[message.chat.id]['direccion_envio']+ '\n'
          texto_html+= '💸 '+ str(usuario[message.chat.id]['red']) +' que se envían: '  + '\n'
          texto_html+= str(int(cuenta_cj['saldos_'+str(i)])/1e8)+' '+str(usuario[message.chat.id]['red']) + '\n'

          texto_html+= '💰 fee de minería: '+ '\n'
          texto_html+= str(fee_mineria) + ' sats'+ '\n'
          texto_html+= 'Si te corre prisa la transacción modifica la cifra, te pongo las fees actuales:'+ '\n'
          texto_html+= 'transacción lenta:'+str(fee_por_lento)+ ' sats'+ '\n'
          texto_html+= 'transacción rápida:'+str(fee_por_rapido)+ ' sats'+ '\n'          
          texto_html+= '########################### ' + '\n'

          msg=bot.send_message(message.chat.id,texto_html, parse_mode="html", reply_markup=markup)


def cambio_fee_mineria_cj(message):
            msg = bot.send_message(message.chat.id, 'Indica un número entero > 500 \n será la fee de minería aplicada y se descontará de tu UTXO')
            bot.register_next_step_handler(msg, confirmacion_envio_fuera_mineria_cj)
  
def confirmacion_envio_fuera_mineria_cj(message): 
    if usuario.get(message.chat.id, {}).get('red')=='BTC':
            objetivo=500
    if usuario.get(message.chat.id, {}).get('red')=='LTC':
            objetivo=100

    cuenta_cj=usuario[message.chat.id]['coinjoin']
    i=usuario[message.chat.id]['clave']
    try:
        numero_entero = int(message.text)
        if numero_entero>=objetivo:
              usuario[message.chat.id]['fee_mincj']=numero_entero
              red=usuario[message.chat.id]['red']
              markup = InlineKeyboardMarkup([[button_ok_cj],  [button_modificar_dire_cj, button_cambio_fee_cj], [button_inicio]])
          #muestra resumen por pantalla:
              texto_html = '<b>📊 Resumen de la transacción </b>' + '\n'
              texto_html+= '########################### ' + '\n'
              texto_html+= '📬 Dirección envío: '+ '\n'
              texto_html+= usuario[message.chat.id]['direccion_envio']+ '\n'
              texto_html+= '💸 '+ str(usuario[message.chat.id]['red']) +' que se envían: '  + '\n'
              texto_html+= str(int(cuenta_cj['saldos_'+str(i)])/1e8)+' '+str(usuario[message.chat.id]['red']) + '\n'
              texto_html+= '########################### ' + '\n'
              
              texto_html+= '💰 fee de minería: '+ '\n'
              texto_html+= str(usuario[message.chat.id]['fee_mincj']) + ' sats'+ '\n'
              texto_html+= 'Si te corre prisa la transacción modifica la cifra, presionando el botón'+ '\n'
              texto_html+= '########################### ' + '\n'

              msg=bot.send_message(message.chat.id,texto_html, parse_mode="html", reply_markup=markup)
        else:
            bot.reply_to(message, "El valor ingresado es menor de "+str(objetivo)+". Por favor, intenta nuevamente.")
            bot.register_next_step_handler(message, confirmacion_envio_fuera_mineria_cj)       

        
    except ValueError:
            # Si no se puede convertir a entero, solicitas nuevamente el número
            bot.reply_to(message, "El valor ingresado no es un número entero. Por favor, intenta nuevamente.")
            bot.register_next_step_handler(message, confirmacion_envio_fuera_mineria)       

def enviando_fuera_confirmado_cj(message):
      cuenta_cj=usuario[message.chat.id]['coinjoin']
      
      i=usuario[message.chat.id]['clave']
        
      if usuario.get(message.chat.id, {}).get('red')=='BTC':
                m=1
                add='direcc_btc_'+str(i)
      if usuario.get(message.chat.id, {}).get('red')=='LTC':
                m=3
                add='direcc_ltc_'+str(i)
      red=usuario[message.chat.id]['red']
      if red == 'BTC':
            fee_mineria = usuario[message.chat.id]['fee_mincj']
            url=f'https://mempool.space/es/tx/'
      elif red == 'LTC':
            fee_mineria = usuario[message.chat.id]['fee_mincj']
            url=f'https://explorer.litecoin.net/tx/'
      destino=usuario[message.chat.id]['direccion_envio']
      saldo=cuenta_cj['saldos_'+str(i)]
      llave=cuenta_cj['llave_hex_'+str(i)]
      direccion=cuenta_cj[add]
      try:
        
        envio=l.send(llave,direccion,destino,saldo-fee_mineria,fee=fee_mineria)
      
        button_operacion = InlineKeyboardButton('Ver transacción', url=url+envio)
        texto_html = 'Satoshis enviados' + '\n'
        texto_html+= '👋 Gracias por usar el CoinJoin BTC_Bot' + '\n'
        markup = InlineKeyboardMarkup([[button_operacion], [button_inicio]])
        bot.send_message(message.chat.id, texto_html, parse_mode="html", reply_markup=markup)
      except:
        texto_html = 'Satoshis NO enviados' + '\n'
        texto_html+= 'Prueba otra vez, seguramente ya lo has enviado. También puede ser que la fee de minería sea muy baja' + '\n'
        markup = InlineKeyboardMarkup([[button_inicio]])
        bot.send_message(message.chat.id, texto_html, parse_mode="html", reply_markup=markup)

""" PLAN DE HERENCIA """

def derivar_clave(semilla=b'3\xa5\x82\x84\x17Bl\xd7\xeb\xa4\x9c\x89\x88\xc7\xcb\x9b', passphrase=None):
    # Combinar la semilla y la passphrase si se proporciona una passphrase
    if passphrase:
        semilla += passphrase.encode()
    # Generar un hash SHA-256 de la semilla
    clave_bytes = hashlib.sha256(semilla).digest()
    return clave_bytes

def codificar_mensaje(mensaje, passphrase_, premium=None, dias=0):
    try:     
        # Derivar la clave de cifrado
        clave_bytes = derivar_clave(passphrase=passphrase_)
        # Crear un objeto Fernet con la clave derivada
        clave = base64.urlsafe_b64encode(clave_bytes)
        clave = clave + b'=' * (32 - len(clave))  # Rellenar con '=' para que tenga una longitud de 32 bytes
        clave = clave[:32]  # Tomar solo los primeros 32 bytes
        clave = base64.urlsafe_b64decode(clave)  # Decodificar la clave

        # Concatenar "la cabecera" al principio del mensaje
        if premium=='hombre_muerto':                   
            dias_a_bloques=calcular_bloques_en_dias(int(dias))
            bloque_actual=obtener_ultimo_bloque_confirmado()
            desbloqueo=int(bloque_actual)+int(dias_a_bloques)
            texto_a_anadir=':'+str(desbloqueo)
            cabecera="bloq. por hombre muerto            "
            num_caracteres_a_reemplazar = len(texto_a_anadir)
            # Reemplaza los últimos caracteres de la cadena
            if num_caracteres_a_reemplazar>0:
                mensaje_nuevo = cabecera[:-num_caracteres_a_reemplazar] + texto_a_anadir
            else:     
                mensaje_nuevo=cabecera
                
            mensaje = mensaje_nuevo + mensaje
            
        elif premium=='bloqueo':                         
            dias_a_bloques=calcular_bloques_en_dias(int(dias))
            bloque_actual=obtener_ultimo_bloque_confirmado()
            desbloqueo=int(bloque_actual)+int(dias_a_bloques)
            texto_a_anadir=':'+str(desbloqueo)
            cabecera="bloq. por hombre bloqueo           "
            num_caracteres_a_reemplazar = len(texto_a_anadir)
            # Reemplaza los últimos caracteres de la cadena
            if num_caracteres_a_reemplazar>0:
                mensaje_nuevo = cabecera[:-num_caracteres_a_reemplazar] + texto_a_anadir
            else:     
                mensaje_nuevo=cabecera
                
            mensaje = mensaje_nuevo + mensaje
        elif premium=='codificacion':
          mensaje = "mensaje bloqueado por bloqueo      " + mensaje
        else:
          mensaje = "                                   " + mensaje       

        # Cifrar el mensaje
        mensaje_cifrado = bytearray()
        for i in range(len(mensaje)):
            mensaje_cifrado.append(mensaje.encode()[i] ^ clave[i % len(clave)])        
        # Devolver el mensaje cifrado en Base64
        mensaje_base64 = base64.b64encode(mensaje_cifrado).decode()
        return mensaje_base64
    except Exception as e:
        return str(e)

def descodificar_mensaje(mensaje_base64, passphrase_):
    try:
        # Derivar la clave de cifrado
        clave_bytes = derivar_clave(passphrase=passphrase_)

        # Crear un objeto Fernet con la clave derivada
        clave = base64.urlsafe_b64encode(clave_bytes)
        clave = clave + b'=' * (32 - len(clave))  # Rellenar con '=' para que tenga una longitud de 32 bytes
        clave = clave[:32]  # Tomar solo los primeros 32 bytes
        clave = base64.urlsafe_b64decode(clave)  # Decodificar la clave

        # Decodificar el mensaje desde Base64
        mensaje_cifrado = base64.b64decode(mensaje_base64.encode())

        # Descifrar el mensaje
        mensaje_descifrado = bytearray()
        for i in range(len(mensaje_cifrado)):
            mensaje_descifrado.append(mensaje_cifrado[i] ^ clave[i % len(clave)])
        
        # Convertir el resultado a una cadena UTF-8
        mensaje_descifrado = mensaje_descifrado.decode('utf-8')

        # Dividir los primeros 35 caracteres en dos partes si hay ":"
        if ':' in mensaje_descifrado[:35]:
            partes = mensaje_descifrado[:35].split(':')
            mensaje_inicial = ':'.join(partes[:-1])
            numero_despues_de_dos_puntos = int(partes[-1])
        else:
            mensaje_inicial = mensaje_descifrado[:35]
            numero_despues_de_dos_puntos = None

        # Obtener el mensaje descifrado a partir del carácter 35
        mensaje_descifrado_a_partir_de_35 = mensaje_descifrado[35:]

        return mensaje_inicial, numero_despues_de_dos_puntos, mensaje_descifrado_a_partir_de_35
    except Exception as e:
        return "Error: semilla incorrecta"  # Si ocurre un error, devuelve un mensaje de error y None como segundo y tercer valor


def get_unspent_outputs(address):
    try:
        unspent_outputs = NetworkAPI.get_unspent(address)
        confirmed_value = 0
        pending_value = 0
        for output in unspent_outputs:
            if output.confirmations > 1:
                confirmed_value += output.amount
            if output.confirmations < 2:
                pending_value += output.amount
        return confirmed_value, unspent_outputs, pending_value
    except Exception as e:
        print(f"Error: {e}")
        return 0, [], 0
"""## BOT TELEGRAM"""
#TRADUCCIONES:

#Botones inline:
# Crea los botones usando InlineKeyboardButton
# INICIO
#selecciona red 
idioma_usuario = "es"

# Define tus textos en español e inglés
textos = {
    "Informacion_sobre_tu_cuenta": {
        "es": "🔑 Información sobre tu cuenta",
        "gb": "🔑 Information about your account"
    },
    "button_coinjoin": {
        "es": "🌪️ CoinJoin",
        "gb": "🌪️ CoinJoin"
    },
    "button_herencia": {
        "es": "📜 Plan de herencia",
        "gb": "📜 Inheritance plan"
    },
    "button_idioma": {
        "es": "🌍️ Select language",
        "gb": "🌍️ Select language"
    },
    "button_coinjoin_basico": {
        "es": "🌪️ CoinJoin modo fácil",
        "gb": "🌪️ Easy CoinJoin mode"
    },
    "button_coinjoin_avanzado": {
        "es": "🌪️ CoinJoin 'no confíes, verifica' (avanzado)",
        "gb": "🌪️ CoinJoin 'don't trust, verify' (advanced)"
    },
    "button_spain": {
        "es": "🇪🇦 Español",
        "gb": "🇪🇦 Spanish"
    },
    "button_english": {
        "es": "🇬🇧 Inglés",
        "gb": "🇬🇧 English"
    },
    "button_btc": {
        "es": "₿ Red Bitcoin",
        "gb": "₿ Bitcoin Network"
    },
    "button_ltc": {
        "es": "Ł Red Litecoin",
        "gb": "Ł Litecoin Network"
    },
    "button_cuenta": {
        "es": "🔑 Información sobre tu cuenta",
        "gb": "🔑 Information about your account"
    },
    "button_llave": {
        "es": "🔐 Tu clave privada",
        "gb": "🔐 Your private key"
    },
    "button_llave_cj": {
        "es": "🔐 Tu clave privada",
        "gb": "🔐 Your private key"
    },
    "button_retirar": {
        "es": "💸 Retirar tus BTC de la cuenta",
        "gb": "💸 Withdraw your BTC from the account"
    },
    "button_retirar_cj": {
        "es": "💸 Retirar tus BTC de la cuenta",
        "gb": "💸 Withdraw your BTC from the account"
    },
    "button_cj": {
        "es": "🌪️ Nuevo CoinJoin",
        "gb": "🌪️ New CoinJoin"
    },
    "button_reservar_mixer": {
        "es": "💰 Billeteras del CoinJoin",
        "gb": "💰 CoinJoin Wallets"
    },
    "button_donacion": {
        "es": "🤑 Donación",
        "gb": "🤑 Donation"
    },
    "button_manual": {
        "es": "📑 Manual de uso",
        "gb": "📑 User Manual",
        "url": "https://docs.google.com/document/d/e/2PACX-1vTvdo577s1E7TwaAIjACwbk889qjNuIwW6wNtPPu9XHviCZyvzGs2Rcgkb8lz7lDf8xm5BhVOUGOSOz/pub"
    },
    "button_guia": {
        "es": "📑 Guía para billetera python DiY",
        "gb": "📑 Guide for DIY Python Wallet",
        "url": "https://colab.research.google.com/drive/1RVH5Emu1hWGdIIn-yabcSRLxfrlgVsTH#scrollTo=AwkMUffJpJ7X"
    },
    "button_001": {
        "es": "₿ CoinJoin salida ➡️ 0.01 BTC # ",
        "gb": "₿ CoinJoin output ➡️ 0.01 BTC # "
    },
    "button_005": {
        "es": "₿ CoinJoin salida ➡️ 0.05 BTC # ",
        "gb": "₿ CoinJoin output ➡️ 0.05 BTC # "
    },
    "button_01": {
        "es": "₿ CoinJoin salida ➡️ 0.1 BTC # ",
        "gb": "₿ CoinJoin output ➡️ 0.1 BTC # "
    },
    "button_02": {
        "es": "₿ CoinJoin salida ➡️ 0.2 BTC # ",
        "gb": "₿ CoinJoin output ➡️ 0.2 BTC # "
    },
    "button_05": {
        "es": "₿ CoinJoin salida ➡️ 0.5 BTC # ",
        "gb": "₿ CoinJoin output ➡️ 0.5 BTC # "
    },
    "button_1": {
        "es": "₿ CoinJoin salida ➡️ 1 BTC # ",
        "gb": "₿ CoinJoin output ➡️ 1 BTC # "
    },
    "button_001_avanzado": {
        "es": "₿ CoinJoin salida ➡️ 0.01 BTC # ",
        "gb": "₿ CoinJoin output ➡️ 0.01 BTC # "
    },
    "button_005_avanzado": {
        "es": "₿ CoinJoin salida ➡️ 0.05 BTC # ",
        "gb": "₿ CoinJoin output ➡️ 0.05 BTC # "
    },
    "button_01_avanzado": {
        "es": "₿ CoinJoin salida ➡️ 0.1 BTC # ",
        "gb": "₿ CoinJoin output ➡️ 0.1 BTC # "
    },
    "button_02_avanzado": {
        "es": "₿ CoinJoin salida ➡️ 0.2 BTC # ",
        "gb": "₿ CoinJoin output ➡️ 0.2 BTC # "
    },
    "button_05_avanzado": {
        "es": "₿ CoinJoin salida ➡️ 0.5 BTC # ",
        "gb": "₿ CoinJoin output ➡️ 0.5 BTC # "
    },
    "button_1_avanzado": {
        "es": "₿ CoinJoin salida ➡️ 1 BTC # ",
        "gb": "₿ CoinJoin output ➡️ 1 BTC # "
    },
    "button_001L": {
        "es": "Ł CoinJoin salida ➡️ 1 LTC # ",
        "gb": "Ł CoinJoin output ➡️ 1 LTC # "
    },
    "button_005L": {
        "es": "Ł CoinJoin salida ➡️ 5 LTC # ",
        "gb": "Ł CoinJoin output ➡️ 5 LTC # "
    },
    "button_01L": {
        "es": "Ł CoinJoin salida ➡️ 10 LTC # ",
        "gb": "Ł CoinJoin output ➡️ 10 LTC # "
    },
    "button_02L": {
        "es": "Ł CoinJoin salida ➡️ 20 LTC # ",
        "gb": "Ł CoinJoin output ➡️ 20 LTC # "
    },
    "button_05L": {
        "es": "Ł CoinJoin salida ➡️ 50 LTC # ",
        "gb": "Ł CoinJoin output ➡️ 50 LTC # "
    },
    "button_1L": {
        "es": "Ł CoinJoin salida ➡️ 100 LTC # ",
        "gb": "Ł CoinJoin output ➡️ 100 LTC # "
    },
    "button_001L_avanzado": {
        "es": "Ł CoinJoin salida ➡️ 1 LTC # ",
        "gb": "Ł CoinJoin output ➡️ 1 LTC # "
    },
    "button_005L_avanzado": {
        "es": "Ł CoinJoin salida ➡️ 5 LTC # ",
        "gb": "Ł CoinJoin output ➡️ 5 LTC # "
    },
    "button_01L_avanzado": {
        "es": "Ł CoinJoin salida ➡️ 10 LTC # ",
        "gb": "Ł CoinJoin output ➡️ 10 LTC # "
    },
    "button_02L_avanzado": {
        "es": "Ł CoinJoin salida ➡️ 20 LTC # ",
        "gb": "Ł CoinJoin output ➡️ 20 LTC # "
    },
    "button_05L_avanzado": {
        "es": "Ł CoinJoin salida ➡️ 50 LTC # ",
        "gb": "Ł CoinJoin output ➡️ 50 LTC # "
    },
    "button_1L_avanzado": {
        "es": "Ł CoinJoin salida ➡️ 100 LTC # ",
        "gb": "Ł CoinJoin output ➡️ 100 LTC # "
    },
    "button_cambio_dir": {
        "es": "🔧 Modificar la dirección de envío por defecto",
        "gb": "🔧 Modify the default shipping address"
    },
    "de": {
        "es": " de ",
        "gb": " of "
    },
    "button_volver_inicio_coinjoin": {
        "es": "⬅️ Volver",
        "gb": "⬅️ Back"
    },
    "button_confirmar": {
        "es": "🌪️ Confirmar participación en CoinJoin",
        "gb": "🌪️ Confirm participation in CoinJoin"
    },
    "button_modificar_cj": {
        "es": "🔧 Modificar tu CoinJoin",
        "gb": "🔧 Modify your CoinJoin"
    },
    "button_volver": {
        "es": "⬅️ Volver",
        "gb": "⬅️ Back"
    },
    "button_inicio": {
        "es": "⏳ Menú principal",
        "gb": "⏳ Main Menu"
    },
    "button_inicio_cj": {
        "es": "⬅️ Volver",
        "gb": "⬅️ Back"
    },
    "button_cancelar": {
        "es": "❌ Cancelar reserva",
        "gb": "❌ Cancel reservation"
    },
    "button_confirmar_mixer_existente": {
        "es": "🌪️ Confirmar reserva del mixer",
        "gb": "🌪️ Confirm mixer reservation"
    },
    "button_modificar_direcciones_CJ": {
        "es": "🔧 Modificar direcciones finales del CoinJoin",
        "gb": "🔧 Modify CoinJoin final addresses"
    },
    "mempool_": {
        "es": '⛓️ Mirar dirección en mempool',
        "gb": '⛓️ Look at the address in the mempool'
    },
    "button_volver_inicio_bot": {
        "es": "⬅️ volver",
        "gb": "⬅️ Back"
    },
    "button_ok": {
        "es": "👌 Ok - todo comprobado",
        "gb": "👌 Ok - all checked"
    },
    "button_ok_cj": {
        "es": "👌 Ok - todo comprobado",
        "gb": "👌 Ok - all checked"
    },
    "button_modificar": {
        "es": "🚧 Volver a revisar dirección",
        "gb": "🚧 Review address again"
    },
    "button_cambio_fee": {
        "es": "💰 Cambia fee minería",
        "gb": "💰 Change mining fee"
    },
    "button_cambio_fee_cj": {
        "es": "💰 Cambia fee minería",
        "gb": "💰 Change mining fee"
    },
    "button_modificar_dire_cj": {
        "es": "🚧 Volver a revisar dirección",
        "gb": "🚧 Review address again"
    },
    # Add more buttons and translations as needed
}

# Ejemplo de cómo utilizar los textos según el idioma del usuario


# Ejemplo de c贸mo utilizar los textos seg煤n el idioma del usuario
def cambia_idioma_botones(idioma='es'):
    global button_pagar_codificado,button_volver_zonapremium,button_pagar_bloqueo,button_sigo_vivo,button_premium_ninguno,button_premium_codificacion,button_premium_bloqueo,button_premium_hombre_muerto,button_volver_premium,button_pagar_hombre_muerto,button_volver_plan_herencia,button_codificar,button_descodificar,button_hombre_muerto,button_bloqueo,button_codificar_premium,button_codificar,button_premium,button_direcciones_cj,button_donacion2,button_coinjoin, button_herencia, button_idioma, button_coinjoin_basico, button_coinjoin_avanzado, button_spain, button_english, button_btc, button_ltc, button_cuenta, button_llave, button_llave_cj, button_retirar, button_retirar_cj, button_cj, button_reservar_mixer, button_donacion, button_manual, button_guia, button_001, button_005, button_01, button_02, button_05, button_1, button_001_avanzado, button_005_avanzado, button_01_avanzado, button_02_avanzado, button_05_avanzado, button_1_avanzado, button_001L, button_005L, button_01L, button_02L, button_05L, button_1L, button_001L_avanzado, button_005L_avanzado, button_01L_avanzado, button_02L_avanzado, button_05L_avanzado, button_1L_avanzado, button_cambio_dir, button_confirmar, button_modificar_cj, button_volver, button_inicio, button_inicio_cj, button_cancelar, button_confirmar_mixer_existente, button_modificar_direcciones_CJ,button_volver_inicio_bot,button_ok,button_ok_cj,button_modificar,button_cambio_fee,button_cambio_fee_cj,button_modificar_dire_cj, button_001,button_005, button_01, button_02, button_05, button_1, button_001L,button_005L,button_01L,button_02L,button_05L,button_1L
    
    button_codificar = InlineKeyboardButton("馃敀 Codificar mensaje", callback_data='codificar_mensaje')
    button_descodificar = InlineKeyboardButton("馃敁 Descodificar mensaje", callback_data='descodificar_mensaje')  
    button_premium = InlineKeyboardButton("馃拵 Zona premium", callback_data='premium_')  
    button_hombre_muerto = InlineKeyboardButton("馃拃 Bot贸n hombre muerto", callback_data='hombre_muerto')   
    button_bloqueo = InlineKeyboardButton("馃敀馃敆 Bloqueo xxxx bloques", callback_data='bloqueo')  
    button_codificar_premium = InlineKeyboardButton("馃敀馃拵 Codificar mensaje eligiendo una semilla", callback_data='codificar_mensaje_premium')
    button_volver_plan_herencia = InlineKeyboardButton(textos["button_volver_inicio_bot"][idioma], callback_data='volver_planherencia')  
    button_pagar_hombre_muerto = InlineKeyboardButton('馃挵 Paga la opci贸n del bot贸n hombre muerto', callback_data='pagar_hombre_muerto')  
    button_pagar_bloqueo = InlineKeyboardButton('馃挵 Paga la opci贸n del bot贸n bloqueo por tiempo', callback_data='pagar_bloqueo')    
    button_pagar_codificado = InlineKeyboardButton('馃挵 Paga la opci贸n de codificar eligiendo semilla', callback_data='pagar_codificado')  
    button_volver_premium = InlineKeyboardButton(textos["button_volver_inicio_bot"][idioma], callback_data='premium_')  
    button_volver_zonapremium = InlineKeyboardButton(textos["button_volver_inicio_bot"][idioma], callback_data='zonapremium_')  
    button_premium_hombre_muerto = InlineKeyboardButton('馃拃 Activar el hombre muerto para este mensaje', callback_data='premium_hombre_muerto')  
    button_premium_bloqueo = InlineKeyboardButton('馃敀馃敆 Activa el Bloqueo de bloques en este mensaje', callback_data='premium_bloqueo')  
    button_premium_codificacion = InlineKeyboardButton('馃拵 Indica otra semilla para codificar el mensaje', callback_data='premium_codificacion')  
    button_premium_ninguno = InlineKeyboardButton('鉂?No usar ninguna funci贸n premium', callback_data='premium_codificar_mensaje')  
    button_sigo_vivo = InlineKeyboardButton('馃尡 Sigo vivo!', callback_data='sigo_vivo') 

    
    
    button_direcciones_cj = InlineKeyboardButton("馃敡 Modificar direcciones del CoinJoin", callback_data='mod_coinjoin_direcciones')   
    
    button_coinjoin = InlineKeyboardButton(textos["button_coinjoin"][idioma], callback_data='menu_coinjoin')
    button_herencia = InlineKeyboardButton(textos["button_herencia"][idioma], callback_data='menu_herencia')
    button_idioma = InlineKeyboardButton(textos["button_idioma"][idioma], callback_data='menu_idioma')
    button_coinjoin_basico = InlineKeyboardButton(textos["button_coinjoin_basico"][idioma], callback_data='coinjoin_modo_facil')
    button_coinjoin_avanzado = InlineKeyboardButton(textos["button_coinjoin_avanzado"][idioma], callback_data='coinjoin_modo_avanzado')
    button_spain = InlineKeyboardButton(textos["button_spain"][idioma], callback_data='cambio_idioma_ES')
    button_english = InlineKeyboardButton(textos["button_english"][idioma], callback_data='cambio_idioma_GB')
 
    button_btc = InlineKeyboardButton(textos["button_btc"][idioma], callback_data='red_btc')
    button_ltc = InlineKeyboardButton(textos["button_ltc"][idioma], callback_data='red_ltc')
    button_cuenta = InlineKeyboardButton(textos["Informacion_sobre_tu_cuenta"][idioma], callback_data='cuenta')
    button_llave = InlineKeyboardButton(textos["button_llave"][idioma], callback_data='llave_privada')
    button_llave_cj = InlineKeyboardButton(textos["button_llave_cj"][idioma], callback_data='llave_privada_cj')
    button_retirar = InlineKeyboardButton(textos["button_retirar"][idioma], callback_data='retirar_btc')
    button_retirar_cj = InlineKeyboardButton(textos["button_retirar_cj"][idioma], callback_data='retirar_btc_cj')
    button_cj = InlineKeyboardButton( textos["button_cj"][idioma], callback_data='crear_CoinJoin')
    button_reservar_mixer = InlineKeyboardButton( textos["button_reservar_mixer"][idioma], callback_data='mirar_coinjoin_propios')
    button_donacion = InlineKeyboardButton(textos["button_donacion"][idioma], callback_data='donacion')
    button_donacion2 = InlineKeyboardButton(textos["button_donacion"][idioma], callback_data='donacion_inicio')
    button_manual = InlineKeyboardButton( textos["button_manual"][idioma], url=textos["button_manual"]["url"])
    button_guia = InlineKeyboardButton(textos["button_guia"][idioma], url=textos["button_guia"]["url"])

    # Resto de botones
    # ...

    button_cambio_dir = InlineKeyboardButton(textos["button_cambio_dir"][idioma], callback_data='modifica_direccion_envio')
    button_confirmar = InlineKeyboardButton( textos["button_confirmar"][idioma], callback_data='confirmar_CoinJoin')
    button_modificar_cj = InlineKeyboardButton(textos["button_modificar_cj"][idioma], callback_data='modifica_CoinJoin')
    button_volver = InlineKeyboardButton(textos["button_volver"][idioma], callback_data='volver_oferta')
    button_inicio = InlineKeyboardButton( textos["button_inicio"][idioma], callback_data='volver_inicio_cj')
    button_inicio_cj = InlineKeyboardButton( textos["button_inicio_cj"][idioma], callback_data='mirar_coinjoin_propios')
    button_cancelar = InlineKeyboardButton(textos["button_cancelar"][idioma], callback_data='cancelar_coinjoin')
    button_confirmar_mixer_existente = InlineKeyboardButton(textos["button_confirmar_mixer_existente"][idioma], callback_data='reservar_mixer_existente')
    button_modificar_direcciones_CJ = InlineKeyboardButton(textos["button_modificar_direcciones_CJ"][idioma], callback_data='modifica_addr_CoinJoin')
                       

    button_volver_inicio_bot = InlineKeyboardButton(textos["button_volver_inicio_coinjoin"][idioma], callback_data="volver_inicio")
    button_ok = InlineKeyboardButton(textos["button_ok"][idioma], callback_data="ok")
    button_ok_cj = InlineKeyboardButton(textos["button_ok_cj"][idioma], callback_data="ok_cj")
    button_modificar = InlineKeyboardButton(textos["button_modificar"][idioma], callback_data="volver_direccion")
    button_cambio_fee = InlineKeyboardButton(textos["button_cambio_fee"][idioma], callback_data="fee_min")
    button_cambio_fee_cj = InlineKeyboardButton(textos["button_cambio_fee_cj"][idioma], callback_data="fee_mincj")
    button_modificar_dire_cj = InlineKeyboardButton(textos["button_modificar_dire_cj"][idioma], callback_data="volver_direccion_cj")
 
       
    button_001 = InlineKeyboardButton(textos["button_001"][idioma] + str(count(coin_join_0_01B))+ textos["de"][idioma] +str(objetivo_coinjoin), callback_data='0.01BTC')
    button_005 = InlineKeyboardButton(textos["button_005"][idioma] + str(count(coin_join_0_05B))+textos["de"][idioma]+str(objetivo_coinjoin), callback_data='0.05BTC')
    button_01 = InlineKeyboardButton(textos["button_01"][idioma] + str(count(coin_join_0_1B))+textos["de"][idioma]+str(objetivo_coinjoin), callback_data='0.1BTC')
    button_02 = InlineKeyboardButton(textos["button_02"][idioma] + str(count(coin_join_0_2B))+textos["de"][idioma]+str(objetivo_coinjoin), callback_data='0.2BTC')
    button_05 = InlineKeyboardButton(textos["button_05"][idioma] + str(count(coin_join_0_5B))+textos["de"][idioma]+str(objetivo_coinjoin), callback_data='0.5BTC')
    button_1 = InlineKeyboardButton(textos["button_1"][idioma] + str(count(coin_join_1B))+textos["de"][idioma]+str(objetivo_coinjoin), callback_data='1BTC')
    button_001L = InlineKeyboardButton(textos["button_001L"][idioma] + str(count(coin_join_1L))+textos["de"][idioma]+str(objetivo_coinjoin), callback_data='1LTC')
    button_005L = InlineKeyboardButton(textos["button_005L"][idioma] + str(count(coin_join_5L))+textos["de"][idioma]+str(objetivo_coinjoin), callback_data='5LTC')
    button_01L = InlineKeyboardButton(textos["button_01L"][idioma] + str(count(coin_join_10L))+textos["de"][idioma]+str(objetivo_coinjoin), callback_data='10LTC')
    button_02L = InlineKeyboardButton(textos["button_02L"][idioma] + str(count(coin_join_20L))+textos["de"][idioma]+str(objetivo_coinjoin), callback_data='20LTC')
    button_05L = InlineKeyboardButton(textos["button_05L"][idioma] + str(count(coin_join_50L))+textos["de"][idioma]+str(objetivo_coinjoin), callback_data='50LTC')
    button_1L = InlineKeyboardButton(textos["button_1L"][idioma] + str(count(coin_join_100L))+textos["de"][idioma]+str(objetivo_coinjoin), callback_data='100LTC')
    


def crear_boton_mempool(direccion, red):
    if red=='BTC':
        return InlineKeyboardButton(textos["mempool_"][idioma_usuario], url=f'https://mempool.space/es/address/{direccion}')
    if red=='LTC':
        return InlineKeyboardButton(textos["mempool_"][idioma_usuario], url=f'https://litecoinblockexplorer.net/address/{direccion}')
        
        
def crear_boton_direcciones(diccionario):
    botones = []
    for clave, valor in diccionario.items():
        if isinstance(valor, dict) and 'direcciones_envio' in valor:
            direcciones_envio = valor['direcciones_envio']
            for subclave, subvalor in direcciones_envio.items():
                if subclave != 'resto':
                    botones.append(InlineKeyboardButton(str(subclave) + " : " + str(subvalor), callback_data='modifica_la_direccion_'+str(subclave)))
    botones.append(button_inicio)
    markup = InlineKeyboardMarkup(build_menu(botones, n_cols=1))
    return markup






    
def build_menu(buttons, n_cols, header_buttons=None, footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu





def borrar_mensajes(chat_id, message_id, num_mensajes):
    for i in range(num_mensajes):
        try:
            # Borra los mensajes utilizando el método delete_message
            bot.delete_message(chat_id, message_id - i)
        except ApiTelegramException as e:
            if e.result_json['description'] == 'Bad Request: message to delete not found':
                # Ignorar el mensaje si no se encuentra
                pass
            else:
                # Ocurrió otra excepción, puedes manejarla según tus necesidades
                print(f"Error al borrar el mensaje con ID {message_id - i}: {e}")





def generar_codigo_qr_al_vuelo(texto):
    # Crea un objeto QRCode con el texto proporcionado
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(texto)
    qr.make(fit=True)

    # Genera una imagen QR a partir del objeto QRCode
    imagen_qr = qr.make_image(fill='black', back_color='white')

    # Convierte la imagen QR a bytes
    byte_stream = BytesIO()
    imagen_qr.save(byte_stream, format='PNG')
    byte_stream.seek(0)

    return byte_stream

def generar_codigo_qr(chat, texto):
    # Crea un objeto QRCode con el texto proporcionado
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(texto)
    qr.make(fit=True)

    # Genera una imagen QR a partir del objeto QRCode
    imagen_qr = qr.make_image(fill='black', back_color='white')

    # Convierte la imagen QR a bytes
    byte_stream = BytesIO()
    imagen_qr.save(byte_stream, format='PNG')
    byte_stream.seek(0)

        

# Inicio del BOT

@bot.message_handler(commands=['start'])
def inicio_bot(message):
    usuario[message.chat.id] = {}
    cambia_idioma_botones(idioma_usuario)
    texto_html = 'Opciones del bot:' + '\n'
    markup = InlineKeyboardMarkup([[button_coinjoin],[button_herencia], [button_donacion2],[button_idioma]])
    bot.send_message(message.chat.id, texto_html, parse_mode="html", reply_markup=markup)
def coinjoin_menu(message):
    texto_html = 'Elije el modo de coinjoin:' + '\n'
    markup = InlineKeyboardMarkup([[button_coinjoin_basico],[button_coinjoin_avanzado]])
    bot.send_message(message.chat.id, texto_html, parse_mode="html", reply_markup=markup)  

def idioma (message):
    texto_html = 'Selecciona el idioma:' + '\n'
    markup = InlineKeyboardMarkup([[button_spain],[button_english]])
    bot.send_message(message.chat.id, texto_html, parse_mode="html", reply_markup=markup)  
    
def modo(message):
    texto_html = 'Elige la red que quieres utilizar:' + '\n'
    markup = InlineKeyboardMarkup([[button_btc],[button_ltc]])
    bot.send_message(message.chat.id, texto_html, parse_mode="html", reply_markup=markup)

def red(message):
    mensaje = bot.send_message(message.chat.id, 'Este bot tiene como objetivo mezclar UTXOs para obtener privacidad de tus Bitcoin\nAñade una passphrase. Ten en cuenta que cada passphrase genera una billetera\nY no es posible recuperarla\n⚠️⚠️ Recuerda bien la passphrase ⚠️⚠️\n🔑 Indica passphrase que quieras utilizar:')
    bot.register_next_step_handler(mensaje, passphrase)
def passphrase(message):
    # Obtener los últimos mensajes del chat
    usuario[message.chat.id]['passphrase']=message.text
    cmd_start(message)
def cmd_start(message):
        texto_html = 'Puedes ver las funciones principales del bot:' + '\n'
    # Crea el teclado usando InlineKeyboardMarkup
        markup = InlineKeyboardMarkup([[button_cuenta],[button_cj],[button_reservar_mixer], [button_donacion], [button_manual]])

    # Envía el mensaje con el teclado
        money,mnemonic,direccion,money_no_confirmado,llave_hex, numero_transacciones=billetera(message.chat.id, usuario[message.chat.id]['passphrase'])
        usuario[message.chat.id]['money']=money
        usuario[message.chat.id]['mnemonic']=mnemonic
        usuario[message.chat.id]['llave_hex']=llave_hex
        usuario[message.chat.id]['direccion']=direccion
        usuario[message.chat.id]['money_no_confirmado']=money_no_confirmado
        usuario[message.chat.id]['numero_transacciones']=numero_transacciones
        
        borrar_mensajes(message.chat.id, message.message_id,25)
        #bot.delete_message(message.chat.id, message.message_id)
        bot.send_message(message.chat.id, texto_html, parse_mode="html", reply_markup=markup)

def coinjoin_direcciones(message):
    texto_html = 'Las siguientes direcciones se han generado con tu passphrase y tendrás acceso a ellas desde el bot, también se mostrarán las llaves privadas:' + '\n'
    texto_html += 'Aún así tienes la opción de modificarlas:' + '\n'

    # Crea el teclado usando InlineKeyboardMarkup
    buttons = []
    salida_coinjoin = usuario[message.chat.id]['direcciones_cj']
    for subclave, subvalor in salida_coinjoin.items():
                if subclave != 'resto':
                    button_text = f"{subclave}: {subvalor}"
                    buttons.append([InlineKeyboardButton(text=button_text, callback_data=f"modifica_la_direccion_{subclave}")])
    
    if buttons:
        reply_markup = InlineKeyboardMarkup(buttons + [[button_inicio]])
        bot.send_message(message.chat.id, "Selecciona el dirección que deseas modificar", reply_markup=reply_markup)
    





def cuenta(message):
    direccion = usuario[message.chat.id]['direccion']
    generar_codigo_qr(message.chat.id, direccion)

    # Crea un mensaje con la información
    texto_html = 'Tu billetera para usar el BOT es:\n'
    texto_html += '`'+str(usuario[message.chat.id]['direccion']) +'`'+ '\n'

    texto_html += 'Para usar la funcionalidad del BOT tienes que enviar sats a esta dirección\n'
    texto_html += 'Tu saldo actualmente en la dirección es: {:.8f} {}\n'.format(usuario[message.chat.id]['money'] / 1e8, usuario[message.chat.id]['red'])

    if usuario[message.chat.id]['money_no_confirmado'] != 0:
        texto_html += 'Tienes un saldo pendiente de confirmaciones de: {:.8f} {}\n'.format(usuario[message.chat.id]['money_no_confirmado'] / 1e8, usuario[message.chat.id]['red'])

    markup = InlineKeyboardMarkup([[crear_boton_mempool(usuario[message.chat.id]['direccion'], usuario[message.chat.id]['red'])], [button_llave], [button_retirar], [button_volver_inicio_bot]])

    # Crea el código QR al vuelo y envía el mensaje con la foto generada
    qr_image = generar_codigo_qr_al_vuelo(direccion)
    bot.send_photo(message.chat.id, qr_image, caption=texto_html, parse_mode='Markdown', reply_markup=markup)


def cuenta_CoinJoin(message):
    borrar_mensajes(message.chat.id, message.message_id, 5)
    cuenta_cj=usuario[message.chat.id]['coinjoin']
    i=usuario[message.chat.id]['clave']
    
    if usuario.get(message.chat.id, {}).get('red')=='BTC':
            m=1
            add='direcc_btc_'+str(i)
    if usuario.get(message.chat.id, {}).get('red')=='LTC':
            m=3
            add='direcc_ltc_'+str(i)
    
    generar_codigo_qr(message.chat.id, cuenta_cj[add])

    # Crea un mensaje con la información
    texto_html = 'La billetera del CoinJoin es:\n'
    texto_html += '`'+str(cuenta_cj[add]) +'`'+ '\n'

    texto_html += 'Te recomiendo que te envies los fondos a una billetera fría tuya propia '+'\n'
    texto_html += 'Tu saldo actualmente en la dirección es: {:.8f} {}\n'.format(cuenta_cj['saldos_'+str(i)] / 1e8, usuario[message.chat.id]['red'])

    markup = InlineKeyboardMarkup([[crear_boton_mempool(str(cuenta_cj[add]), usuario[message.chat.id]['red'])], [button_llave_cj], [button_retirar_cj], [button_inicio_cj]])

    # Crea el código QR al vuelo y envía el mensaje con la foto generada
    qr_image = generar_codigo_qr_al_vuelo(cuenta_cj[add])
    bot.send_photo(message.chat.id, qr_image, caption=texto_html, parse_mode='Markdown', reply_markup=markup)


def crea_mixer(message):
        com_red=''
        comision=''
         
        if usuario.get(message.chat.id, {}).get('red') == 'LTC':
            comision=comision_real_ltc
            com_red="2.000"
        if usuario.get(message.chat.id, {}).get('red') == 'BTC':
            comision=comision_real_btc
            com_red="10.000"

        texto_html = 'Te muestro a continuación los CoinJoins que tienes disponibles para seleccionar.' + '\n'
        texto_html+= '1º Selecciona el tamaño de satoshis que quieres tener al final con privacidad'+ '\n'
        texto_html+= '2º Confirma que quieres participar y cuando se llegue al número de confirmaciones se hará el CoinJoin'+ '\n'
        texto_html+= '3º Recuerda que para el participar en el CoinJoin tendrás que tener en la cuenta del bot:'+ '\n'
        texto_html+= '          ✅ Los satoshis que quieras de salida +'+ '\n'
        texto_html+= '          ✅ Costes de red, he puesto ' + str(com_red) +' satoshis, lo que no se consuma irá a la cuenta de partida.'+ '\n'
        texto_html+= '          ✅ Comisión del bot ('+str(comision) +') satoshis'+  '\n'
        texto_html+= '4º Solo podrás utilizar por usuario del bot 1 billetera en cada ciclo de CoinJoin para evitar ataques Sybil' + '\n'

    # Crea el teclado usando InlineKeyboardMarkup
        if usuario.get(message.chat.id, {}).get('red')=='BTC':
            markup = InlineKeyboardMarkup([[button_001],[button_005], [button_01],[button_02], [button_05],[button_1],[button_inicio]])

        if usuario.get(message.chat.id, {}).get('red')=='LTC':
            markup = InlineKeyboardMarkup([[button_001L],[button_005L], [button_01L],[button_02L], [button_05L],[button_1L],[button_inicio]])

    # Envía el mensaje con el teclado
        borrar_mensajes(message.chat.id, message.message_id,25)
        #bot.delete_message(message.chat.id, message.message_id )
        bot.send_message(message.chat.id, texto_html, parse_mode="html", reply_markup=markup)
        
        
        

def confirma_coinjoin(message):
    pdte=usuario[message.chat.id]['money_no_confirmado']
    if pdte>0:
        pdte=0
    texto_html = '💲 Comprobando saldo en la cuenta para unirte al CoinJoin:\n'
    texto_html += 'El saldo de la cuenta es:\n'
    texto_html += str(int(pdte+usuario[message.chat.id]['money']) / 1e8) + ' ' + usuario[message.chat.id]['red'] + '\n'
    markup = None
    
    usuario[message.chat.id]['money']=10000000
    if usuario.get(message.chat.id, {}).get('red') == 'BTC':
       # if any(message.chat.id in diccionario for diccionario in diccionarios_coinjoin_BTC):
       #     texto_html += 'Tienes satoshis suficientes para unirte al CoinJoin\n'
        #    texto_html += 'Pero estás actualmente en otro CoinJoin solo puedes en uno\n'
         #   markup = InlineKeyboardMarkup([[button_cambio_dir],[button_cancelar], [button_inicio]])
       # else:
            if (pdte+usuario[message.chat.id]['money']) >= usuario[message.chat.id]['importe']:
                texto_html += 'Tienes satoshis suficientes para unirte al CoinJoin\n'
                texto_html += 'Pero OJO! Si cuando se llegue al nº de usuarios del CoinJoin no tienes saldo en la cuenta no se te tendrá en cuenta.\n'
                texto_html += 'Presiona "Confirmar" para hacer la reserva\n'
                markup = InlineKeyboardMarkup([[button_confirmar], [button_direcciones_cj],  [button_inicio]])
            else:
                texto_html += 'No tienes satoshis suficientes para hacer el CoinJoin\n'
                texto_html += 'Necesitarías mínimo ' + str(usuario[message.chat.id]['importe'] / 1e8) + ' ' + str(usuario[message.chat.id]['red']) + ' para participar en el CoinJoin\n'
                markup = InlineKeyboardMarkup([[button_inicio]])

    if usuario.get(message.chat.id, {}).get('red') == 'LTC':
      #  if any(message.chat.id in diccionario for diccionario in diccionarios_coinjoin_LTC):
      #      texto_html += 'Tienes satoshis suficientes para unirte al CoinJoin\n'
      #      texto_html += 'Pero estás actualmente en otro CoinJoin solo puedes en uno\n'
      #      markup = InlineKeyboardMarkup([[button_cancelar], [button_inicio]])
      #  else:
            
            if usuario[message.chat.id]['money'] >= usuario[message.chat.id]['importe']:
                texto_html += 'Tienes satoshis suficientes para unirte al CoinJoin\n'
                texto_html += 'Pero OJO! Si cuando se llegue al nº de usuarios del CoinJoin no tienes saldo en la cuenta no se te tendrá en cuenta.\n'
                
                texto_html += 'Tienes la opción de modificar las direcciones de envío en este paso. \n'
                texto_html += 'Presiona "Confirmar" para hacer la reserva o "Modificar direcciones" para cambiar las direcciones.\n'
                markup = InlineKeyboardMarkup([[button_confirmar], [button_direcciones_cj], [button_inicio]])
            else:
                texto_html += 'No tienes satoshis suficientes para hacer el CoinJoin\n'
                texto_html += 'Necesitarías mínimo ' + str(usuario[message.chat.id]['importe'] / 1e8) + ' ' + str(usuario[message.chat.id]['red']) + ' para participar en el CoinJoin\n'
                markup = InlineKeyboardMarkup([[button_inicio]])

    borrar_mensajes(message.chat.id, message.message_id, 25)
    bot.send_message(message.chat.id, texto_html, parse_mode="html", reply_markup=markup)



      
def modifica_direccion_envio_cj(message):
    bote=usuario[message.chat.id]['bote_coin_join']
    texto_html = 'Te muestro las direcciones donde se envian cuando se haga en CoinJoin, si quieres cambiar alguna dirección pulsa el botón'
    markup=crear_boton_direcciones(bote)
    bot.send_message(message.chat.id, texto_html, parse_mode="html", reply_markup=markup) 
    
def mod_direccion_envio_cj(message):
    msg = bot.send_message(message.chat.id, 'Indica la nueva dirección para reemplazar la actual:')
    bot.register_next_step_handler(msg, mod_diccionario_cj)    
   
def mod_diccionario_cj(message):
    if validar_direccion_bitcoin(message.text,usuario[message.chat.id]['red']):
        i=usuario[message.chat.id]['mod_direccion']
        usuario_id = message.chat.id
        usuario[message.chat.id]['direcciones_cj'][i]=message.text
        coinjoin_direcciones(message)
    else:
        texto_html = 'No es una dirección válida\n'
        markup = InlineKeyboardMarkup([[button_direcciones_cj],[button_inicio]])
        bot.send_message(message.chat.id, texto_html, parse_mode="html", reply_markup=markup) 
        

def cancelar_coinjoin(message):
    texto_html = 'Confirma que cancelas la reserva del CoinJoin'+'\n'
    
    markup = InlineKeyboardMarkup([[button_cancelar], [button_inicio]])
    
def mod_addr_coinjoin(message):
    texto_html = 'Te muestro las direcciones donde se envian el CoinJoin'+'\n'
    texto_html+= 'Si quieres reemplazar las direcciones de envío presiona en cada dirección'+'\n'
    
    markup = InlineKeyboardMarkup([[button_cambio_dir], [button_inicio]])
    
    
     
def mod_addr_coinjoin2(message):
    bote_coin_join[message.chat.id]['direccion']

def hacer_reserva(message):
        
        
        red=usuario[message.chat.id]['red']   
        bote_coin_join=usuario[message.chat.id]['bote_coin_join'] 
        if red == 'BTC':
            billetera_coinjoin = 1
            comision = comision_real_btc+10000
            comision_real=comision_real_btc
            url=f'https://mempool.space/es/tx/'
            billetera=billetera_btc
        elif red == 'LTC':
            billetera_coinjoin = 3
            comision = comision_real_ltc+200000
            comision_real= comision_real_ltc
            url=f'https://explorer.litecoin.net/tx/'            
            billetera=billetera_ltc
        chat_id = usuario.get(message.chat.id, {}).get('passphrase', None)
        bote_coin_join.setdefault(chat_id, {})        
        usuario.setdefault(chat_id, {})
        bote_coin_join[chat_id]['money'] = usuario.get(message.chat.id, {}).get('money', None)
        bote_coin_join[chat_id]['llave_hex'] = usuario.get(message.chat.id, {}).get('llave_hex', None)
        bote_coin_join[chat_id]['direccion'] = usuario.get(message.chat.id, {}).get('direccion', None)
        bote_coin_join[chat_id]['passphrase'] = usuario.get(message.chat.id, {}).get('passphrase', None)
        bote_coin_join[chat_id]['avanzado'] = usuario.get(message.chat.id, {}).get('avanzado', None)
        
        
        bote_coin_join[chat_id]['direcciones_envio']=usuario[message.chat.id]['direcciones_cj']
        salida_coinjoin = usuario[message.chat.id]['direcciones_cj']
        n_utxo=sum(1 for key in salida_coinjoin.keys() if key != 'resto')
        texto_html= 'Te muestro información sobre tu CoinJoin:' + '\n'
        texto_html+= 'Tendrás '+ str(n_utxo) +' UTXOs disponibles cuando se complete el CoinJoin con tu saldo actual' + '\n'
        texto_html+= 'El sobrante, si hay, se te devolverá a la cuenta origen' + '\n'
        texto_html+= 'Eres el ' + str(count(bote_coin_join)) + 'de' +str(objetivo_coinjoin)+' usuarios.' + '\n'
                 
        markup = InlineKeyboardMarkup([[button_inicio]])
        bot.send_message(message.chat.id, texto_html, parse_mode="html", reply_markup=markup)
               

        if red=='LTC':
                fee_sats=mostrar_valores_tarifas(api_urls_LTC)
        elif red=='BTC':
                fee_sats=mostrar_valores_tarifas(api_urls_LTC)
        if count(bote_coin_join)>=objetivo_coinjoin and fee_sats['media']<55:
        
            for key, value in bote_coin_join.copy().items():
                
                    
                    direccion = value.get('direccion')
                    passphrase = value.get('passphrase')
                    if direccion is not None:
                        informacion = obtener_informacion_direccion(direccion, red)
                        
                        salida_coinjoin = dividir_saldo_en_trozos(informacion[0], usuario[message.chat.id]['moneda_btc']*1e8, key, passphrase,red)
            
            #ejecuta el coinjoin...
            saldo_minimo=usuario[message.chat.id]['moneda_btc']*1e8+comision
            #macro comprobando saldos de la cuenta para excluir:
            
            for key, value in bote_coin_join.copy().items():
            
                
                direccion = value.get('direccion')
                passphrase = value.get('passphrase')
                if direccion is not None:
                    informacion = obtener_informacion_direccion(direccion, red)
                    
                    salida_coinjoin = dividir_saldo_en_trozos(informacion[0], usuario[message.chat.id]['moneda_btc']*1e8, key, passphrase,red)
                    
                    
                    n_inputs=count(l.unspent(direccion))
                    
                    n_outputs=int(informacion[0]/(usuario[message.chat.id]['moneda_btc']*1e8))
                    
                    tamanio=calcular_tamanio_transaccion(n_inputs, n_outputs)
                    
                    if informacion[0] > saldo_minimo:
                        bote_coin_join[key].update(salida_coinjoin)  # Agregar la salida_coinjoin al diccionario
                        bote_coin_join[key]['tamanio'] = tamanio                      
    
                    else:
                        del bote_coin_join[key]
            
            
            # Obtener las direcciones unspent del diccionario salida
            direcciones = [salida['direccion'] for salida in bote_coin_join.values() if isinstance(salida, dict) and 'direccion' in salida]
            
            if red=='LTC':
                fee_sats=mostrar_valores_tarifas(api_urls_LTC)
            elif red=='BTC':
                fee_sats=mostrar_valores_tarifas(api_urls_BTC)
                
            diccionario_principal = bote_coin_join
            outputs = []
            
            fee_mineria_final=0
            fee_mineria_final_=0

            for subdiccionario in diccionario_principal.values():
                if isinstance(subdiccionario, dict):
                    for key, value in subdiccionario.items():                        
                                                 
                        if key == 'resto':
                            tamanio = subdiccionario.get('tamanio', 0)
                            fee_mineria_final_ = int(tamanio * fee_sats)
                            fee_mineria_final += fee_mineria_final_
                            
                            resto_value = comision + value - fee_mineria_final_ - comision_real
                            
                            direccion = subdiccionario.get('direccion')
                            output = {'value': resto_value, 'address': direccion}
                            
                            outputs.append(output)
            
            
            
            # Obtener el valor de 'resto' si existe
            

            # Crear una lista de transacciones con las direcciones unspent y la dirección de cambio
            # Obtener direcciones de entrada y salida
            inputs = [l.unspent(addr) for addr in direcciones]
            inputs = [item for sublist in inputs for item in sublist]   
            
            # Obtener direcciones de salida adicionales
            additional_outputs = []
            for diccionario_key, diccionario_value in diccionario_principal.items():
                    for key, value in diccionario_value.items():
                        if isinstance(key, int) and isinstance(value, str):
                            additional_outputs.append({'value': int(usuario[message.chat.id]['moneda_btc']*1e8), 'address': value})
            
            outputs.extend(additional_outputs)
              
            txo = l.mktx_with_change(inputs, outputs, change_addr=billetera['p2wpkh'], fee=fee_mineria_final)
                         
            avisos=[]           
            # Iterar sobre los elementos del diccionario
            for nombre, valores in diccionario_principal.items():
                if isinstance(valores, dict) and 'llave_hex' in valores:
                    llave_hex = valores['llave_hex']
                    direccion = valores.get('direccion', '')
                    avanzado = valores.get('avanzado', '')
                    for i, input_item in enumerate(inputs):
                        if input_item['address'] == direccion:
                            if avanzado == 0:
                                l.sign(txo, i, llave_hex)
                            else:
                                
                                texto_html= 'Se ha completado el nº de billeteras para el coinjoin y has usado el modo avanzado, por lo que te muestro a continuación la tx que tienes que firmar y enviar al bot para completar el CoinJoin:' + '\n'
                                texto_html+= "'"+ str(txo) +"'" + '\n'
                                texto_html+= 'Presiona el texto anterior para copiarlo y llevarlo al notebook de python para completar la firma.' + '\n'
                                print(nombre)
                                bot.send_message(message.chat.id, texto_html, parse_mode="Markdown", reply_markup=markup)
                                
                                avisos.append(nombre)
                            # No se utiliza 'break' para permitir que se procesen todos los elementos en 'inputs'
                    # Añadir un aviso si no se encontró dirección correspondiente en 'inputs'
                    else:
                        avisos.append(nombre)
            print('FIRMA FINAL:@@@@@@@@@@@@@@@@@@')
            print(txo)

            lista_sin_duplicados = list(set(avisos))
            for lista_usu in lista_sin_duplicados.copy():
                    del usuario[lista_usu]['bote_coin_join']

            
            if usuario[message.chat.id]['nombre_coin_join']=='coin_join_100L':
                coin_join_100L.clear()
            elif usuario[message.chat.id]['nombre_coin_join']=='coin_join_50L':
                coin_join_50L.clear()
            elif usuario[message.chat.id]['nombre_coin_join']=='coin_join_20L':
                coin_join_20L.clear()
            elif usuario[message.chat.id]['nombre_coin_join']=='coin_join_10L':
                coin_join_10L.clear()
            elif usuario[message.chat.id]['nombre_coin_join']=='coin_join_5L':
                coin_join_5L.clear()
            elif usuario[message.chat.id]['nombre_coin_join']=='coin_join_1L':
                coin_join_1L.clear()
                
            elif usuario[message.chat.id]['nombre_coin_join']=='coin_join_0_05B':
                coin_join_0_05B.clear()
            elif usuario[message.chat.id]['nombre_coin_join']=='coin_join_0_01B':
                coin_join_0_01B.clear()
            elif usuario[message.chat.id]['nombre_coin_join']=='coin_join_0_1B':
                coin_join_0_1B.clear()
            elif usuario[message.chat.id]['nombre_coin_join']=='coin_join_0_2B':
                coin_join_0_2B.clear()
            elif usuario[message.chat.id]['nombre_coin_join']=='coin_join_0_5B':
                coin_join_0_5B.clear()
            elif usuario[message.chat.id]['nombre_coin_join']=='coin_join_1B':
                coin_join_1B.clear()
            

            
            
            bote_coin_join={}
            
            try:
                
                #operacion=l.pushtx(txo)
                operacion='aa'
                texto_html= 'Enviado CoinJoin:' + '\n'
                borrar_mensajes(message.chat.id, message.message_id,20)                
                button_operacion = InlineKeyboardButton('Ver transacción', url=url+operacion)
                send_message_to_ids(lista_sin_duplicados, '✔️ Enviado CoinJoin mira la transacción {}'.format(url+operacion))
                markup = InlineKeyboardMarkup([[button_operacion], [button_inicio]])
                bot.send_message(message.chat.id, texto_html, parse_mode="html", reply_markup=markup)
            except Exception as e:
            
                texto_html= 'Fallo en las firmas del CoinJoin:' + '\n'
                borrar_mensajes(message.chat.id, message.message_id,20)
                send_message_to_ids(lista_sin_duplicados, '❌ Error en las firmas del CoinJoin tendréis que reservar nuuevamente, no se han tocado los fondos')
                send_message_to_ids(4218039, '❌ Revisa el bot, hay un error al hacer el CoinJoin')
                markup = InlineKeyboardMarkup([[button_inicio]])
                bot.send_message(message.chat.id, texto_html, parse_mode="html", reply_markup=markup)
                


""" BOT plan herencia """

def bot_herencia(message):
    usuario[message.chat.id] = {}
    cambia_idioma_botones(idioma_usuario)
    texto_html = 'Opciones para preparar el plan de herencia:' + '\n'
    markup = InlineKeyboardMarkup([[button_codificar],[button_descodificar], [button_premium],[button_volver_inicio_bot]])
    bot.send_message(message.chat.id, texto_html, parse_mode="html", reply_markup=markup)

def codifica_mensaje(message):
    if str(message.chat.id)== '4218039':
        texto_html= 'Quieres usar alguna de las siguientes funciones premium para codificar el mensaje?:' + '\n'
        markup = InlineKeyboardMarkup([[button_premium_hombre_muerto],[button_premium_bloqueo],[button_premium_codificacion],[button_premium_ninguno],[button_volver_plan_herencia]])
        bot.send_message(message.chat.id, texto_html, parse_mode="Markdown", reply_markup=markup)
    else:
        mensaje = bot.send_message(message.chat.id, 'A continuación pon el texto que quieras codificar:')
        bot.register_next_step_handler(mensaje, funcion_codifica)

   
def funcion_codifica_pre(message):    
        mensaje = bot.send_message(message.chat.id, 'A continuación pon el texto que quieras codificar:')
        bot.register_next_step_handler(mensaje, funcion_codifica)
        
def funcion_codifica_pre2(message):
    if int(message.text):
        usuario[message.chat.id]['dias']=message.text
        mensaje = bot.send_message(message.chat.id, 'A continuación pon el texto que quieras codificar:')
        bot.register_next_step_handler(mensaje, funcion_codifica_premium)
    else: 
        mensaje = bot.send_message(message.chat.id, 'Indica un número entero:')
        bot.register_next_step_handler(message.chat.id, funcion_codifica)
        
def funcion_premium_codifica(message):    
        texto_html= 'Quieres usar alguna de las siguientes funciones premium?:' + '\n'
        markup = InlineKeyboardMarkup([[button_premium_hombre_muerto],[button_premium_bloqueo],[button_premium_codificacion]])
        bot.send_message(message.chat.id, texto_html, parse_mode="Markdown", reply_markup=markup)
        
def funcion_codifica(message):
    # Obtener los últimos mensajes del chat
    
    premium = usuario.get(message.chat.id, {}).get('premium')
    
    if premium == None:
    
        if message.text:
        
            mensaje_codificado=codificar_mensaje( str(message.text), str(message.chat.id))
            texto_html= 'Te muestro el mensaje codificado :' + '\n'
            texto_html+= '`'+str(mensaje_codificado) +'`'+ '\n'
            texto_html+= 'La semilla utilizada para generar el mensaje codificado es tu usuario de telegram, es necesario para descodificarlo:' + '\n'
            texto_html+= '`'+str(message.chat.id) +'`'+ '\n'
                     
            markup = InlineKeyboardMarkup([[button_volver_plan_herencia]])
            bot.send_message(message.chat.id, texto_html, parse_mode="Markdown", reply_markup=markup)
    elif premium == 'codificacion':
        usuario[message.chat.id]['texto_codificado']=message.text
        mensaje = bot.send_message(message.chat.id, 'Indica la semilla que quieres utilizar para codificar el mensaje:')
        bot.register_next_step_handler(mensaje, funcion_codifica_premium)
    
    elif premium == 'hombre_muerto':
        mensaje = bot.send_message(message.chat.id, 'Indica el nº de días para que se active el proceso de hombre muerto y el mensaje se pueda ver:')
        bot.register_next_step_handler(mensaje, funcion_codifica_pre2)
        
    elif premium == 'bloqueo':
        mensaje = bot.send_message(message.chat.id, 'Indica el nº de días que quieres que esté bloqueado el mensaje, no se podrá ver antes:')
        bot.register_next_step_handler(mensaje, funcion_codifica_pre2)
        
        
def calcular_bloques_en_dias(dias):
    minutos_por_dia = 24 * 60  # 24 horas por día y 60 minutos por hora
    bloques_por_minuto = 1 / 10  # Un bloque cada 10 minutos en promedio

    # Calcular el número de bloques aproximados
    bloques_aproximados = int(dias * minutos_por_dia * bloques_por_minuto)

    return bloques_aproximados
def convertir_bloques_a_dias_horas(bloques):
    minutos_por_dia = 24 * 60  # 24 horas por día y 60 minutos por hora
    bloques_por_minuto = 1 / 10  # Un bloque cada 10 minutos en promedio

    # Calcular el número de minutos en función de los bloques
    minutos_totales = bloques / bloques_por_minuto

    # Calcular el número de días y horas
    dias = int(minutos_totales / minutos_por_dia)
    horas = int((minutos_totales % minutos_por_dia) / 60)

    return dias, horas
def obtener_ultimo_bloque_confirmado():
    url = "https://blockchain.info/latestblock"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            ultimo_bloque = data["height"]
            return ultimo_bloque
        else:
            print(f"Error al obtener el último bloque: Código de estado {response.status_code}")
    except Exception as e:
        print(f"Error al obtener el último bloque: {e}")
    
    return None

  
def funcion_codifica_premium(message):
    premium_ = usuario.get(message.chat.id, {}).get('premium')
    if premium_=='codificacion':
            mensaje_codificado=codificar_mensaje( str(usuario[message.chat.id]['texto_codificado']), str(message.text), 'bloqueo')
            texto_html= 'Te muestro el mensaje codificado :' + '\n'
            texto_html+= '`'+str(mensaje_codificado) +'`'+ '\n'
            texto_html+= 'La semilla utilizada para generar el mensaje codificado es tu usuario de telegram, es necesario para descodificarlo:' + '\n'
            texto_html+= '`'+str(message.text) +'`'+ '\n'
                     
            markup = InlineKeyboardMarkup([[button_volver_plan_herencia]])
            bot.send_message(message.chat.id, texto_html, parse_mode="Markdown", reply_markup=markup)
    if premium_=='hombre_muerto':
            semilla=str(message.chat.id)  
            mensaje_codificado=codificar_mensaje( str(message.text), str(semilla), 'hombre_muerto', usuario[message.chat.id]['dias'])
            texto_html= 'Te muestro el mensaje codificado :' + '\n'
            texto_html+= '`'+str(mensaje_codificado) +'`'+ '\n'
            texto_html+= 'La semilla utilizada para generar el mensaje codificado es tu usuario de telegram, es necesario para descodificarlo:' + '\n'
            texto_html+= '`'+str(message.chat.id) +'`'+ '\n'
                     
            markup = InlineKeyboardMarkup([[button_volver_plan_herencia]])
            bot.send_message(message.chat.id, texto_html, parse_mode="Markdown", reply_markup=markup)
    if premium_=='bloqueo':
            semilla=str(message.chat.id)
            mensaje_codificado=codificar_mensaje( str(message.text), str(semilla), 'bloqueo', usuario[message.chat.id]['dias'])
            
            texto_html= 'Te muestro el mensaje codificado :' + '\n'
            texto_html+= '`'+str(mensaje_codificado) +'`'+ '\n'
            texto_html+= 'La semilla utilizada para generar el mensaje codificado es tu usuario de telegram, es necesario para descodificarlo:' + '\n'
            texto_html+= '`'+str(message.chat.id) +'`'+ '\n'
                     
            markup = InlineKeyboardMarkup([[button_volver_plan_herencia]])
            bot.send_message(message.chat.id, texto_html, parse_mode="Markdown", reply_markup=markup)

    
  
def descodifica_mensaje(message):    
    mensaje = bot.send_message(message.chat.id, 'Pega el mensaje a descodificar:')
    bot.register_next_step_handler(mensaje, pide_semilla)
    
def pide_semilla(message):
    if message.text:
        usuario[message.chat.id]['texto_codificado']=message.text
        mensaje = bot.send_message(message.chat.id, 'Ahora pega la semilla para descodificar el mensaje:')
        bot.register_next_step_handler(mensaje, funcion_descodifica)    
    
    
def funcion_descodifica(message):
    
    premium=es_premium(message, str(message.text))
    if premium==1:
        semilla=str(message.text)
        mensaje_descodificado=descodificar_mensaje( usuario[message.chat.id]['texto_codificado'], semilla)
        bloque_actual=obtener_ultimo_bloque_confirmado()
        bloques=mensaje_descodificado[1]-bloque_actual
        dias, horas = convertir_bloques_a_dias_horas(bloques)
        if mensaje_descodificado[1]<=bloque_actual:   
            texto_html= 'Te muestro el mensaje descodificado :' + '\n'
            texto_html+= '\n'
            texto_html+= '`'+str(mensaje_descodificado[2])+'`'+ '\n'
            markup = InlineKeyboardMarkup([[button_volver_plan_herencia]])
            usuario[message.chat.id]['texto_codificado']=''
            bot.send_message(message.chat.id, texto_html, parse_mode="Markdown", reply_markup=markup)
        elif mensaje_descodificado[1]>bloque_actual:
            #falta enviar mensaje al usuario... y hacer algo
            texto_html= 'Aún no han pasado los bloques necesarios para la descodificación' + '\n'
            texto_html+= 'El último bloque confirmado es '+ str(bloque_actual) + ', el mensaje se podrá desbloquear a partir del bloque :'+ str(mensaje_descodificado[1])+ ' \n'
            texto_html+= 'Aprox. son '+ str(dias) + ' días' + ' y '+ str(horas) + ' horas.\n'
            texto_html+= 'Intentalo más adelante, si el usuario no bloquea la descodificación podrás desbloquear el mensaje.\n'
            markup = InlineKeyboardMarkup([[button_volver_plan_herencia]])
            bot.send_message(message.chat.id, texto_html, parse_mode="Markdown", reply_markup=markup)
    elif premium==2:
        semilla=str(message.text)
        mensaje_descodificado=descodificar_mensaje( usuario[message.chat.id]['texto_codificado'], semilla)
        bloque_actual=obtener_ultimo_bloque_confirmado()
        bloques=mensaje_descodificado[1]-bloque_actual
        dias, horas = convertir_bloques_a_dias_horas(bloques)
        if mensaje_descodificado[1]<=bloque_actual:   
            texto_html= 'Te muestro el mensaje descodificado :' + '\n'
            texto_html+= '\n'
            texto_html+= '`'+str(mensaje_descodificado[2])+'`'+ '\n'
            markup = InlineKeyboardMarkup([[button_volver_plan_herencia]])
            usuario[message.chat.id]['texto_codificado']=''
            bot.send_message(message.chat.id, texto_html, parse_mode="Markdown", reply_markup=markup)
        elif mensaje_descodificado[1]>bloque_actual:
            texto_html= 'Aún no han pasado los bloques necesarios para la descodificación' + '\n'
            texto_html+= 'El último bloque confirmado es '+ str(bloque_actual) + ', el mensaje se podrá desbloquear a partir del bloque :'+ str(mensaje_descodificado[1])+ ' \n'
            texto_html+= 'Aprox. son '+ str(dias) + ' días' + ' y '+ str(horas) + ' horas.\n'
            texto_html+= 'Intentalo más adelante y podrás desbloquear el mensaje.\n'
            markup = InlineKeyboardMarkup([[button_volver_plan_herencia]])
            bot.send_message(message.chat.id, texto_html, parse_mode="Markdown", reply_markup=markup)
    elif premium==3:
        semilla=str(message.text)
        mensaje_descodificado=descodificar_mensaje( usuario[message.chat.id]['texto_codificado'], semilla)
        if mensaje_descodificado=="Error: semilla incorrecta":   
            texto_html= 'Error: semilla incorrecta' + '\n'
            texto_html+= '\n'
            markup = InlineKeyboardMarkup([[button_volver_plan_herencia]])
            usuario[message.chat.id]['texto_codificado']=''
            bot.send_message(message.chat.id, texto_html, parse_mode="Markdown", reply_markup=markup)
        else:
            texto_html= 'Te muestro el mensaje descodificado :' + '\n'
            texto_html+= '\n'
            texto_html+= '`'+str(mensaje_descodificado[2])+'`'+ '\n'
            markup = InlineKeyboardMarkup([[button_volver_plan_herencia]])
            usuario[message.chat.id]['texto_codificado']=''
            bot.send_message(message.chat.id, texto_html, parse_mode="Markdown", reply_markup=markup)
            
    elif message.text:
        mensaje_descodificado=descodificar_mensaje( usuario[message.chat.id]['texto_codificado'], str(message.text))
        texto_html= 'Te muestro el mensaje descodificado :' + '\n'
        texto_html+= '\n'
        texto_html+= '`'+str(mensaje_descodificado)+'`'+ '\n'
        markup = InlineKeyboardMarkup([[button_volver_plan_herencia]])
        usuario[message.chat.id]['texto_codificado']=''
        bot.send_message(message.chat.id, texto_html, parse_mode="Markdown", reply_markup=markup)
 
def mensaje_no_descodificado(message):
    texto_html = 'Cancelada la descodificación del mensaje:' + '\n'
    markup = InlineKeyboardMarkup([[button_volver_inicio_bot]])
    bot.send_message(message.chat.id, texto_html, parse_mode="html", reply_markup=markup)
 
def es_premium(message, usuario):
    premium=0
    # Obtener los últimos mensajes del chat
    billetera_hombremuerto = generando_billeteras_keys(texto_a_anadir=str(4218039),passphrase_=str('theblade'),passphrase_1=str(usuario),passphrase_2=str('hombre_muerto'), simbolo=str('BTC'))
    billetera_bloqueo = generando_billeteras_keys(texto_a_anadir=str(4218039),passphrase_=str('theblade'),passphrase_1=str(usuario),passphrase_2=str('bloqueo'), simbolo=str('BTC'))
    billetera_codifica = generando_billeteras_keys(texto_a_anadir=str(4218039),passphrase_=str('theblade'),passphrase_1=str(usuario),passphrase_2=str('codifica'), simbolo=str('BTC'))
    inf_cuenta_hombremuerto=get_unspent_outputs(billetera_hombremuerto['p2wpkh'])
    inf_cuenta_bloqueo=get_unspent_outputs(billetera_bloqueo['p2wpkh'])
    inf_cuenta_codifica=get_unspent_outputs(billetera_codifica['p2wpkh'])
    #saldo_actual, saldo_pendiente, transacciones_entrada
    if message.chat.id==4218039:
        premium=3
    elif (inf_cuenta_hombremuerto[0]>=comision_hombre_muerto) or (inf_cuenta_hombremuerto[0]==0 and count(inf_cuenta_hombremuerto[1])<2):
        premium=1
    elif (inf_cuenta_bloqueo[0]>=comision_bloqueo) or (inf_cuenta_bloqueo[0]==0 and count(inf_cuenta_bloqueo[1])<2 and count(inf_cuenta_bloqueo[1])!=0):
        # enviar a mi billetera el money...
        premium=2
    elif (inf_cuenta_codifica[0]>=comision_codifica) or (inf_cuenta_codifica[0]==0 and count(inf_cuenta_codifica[1])<2  and count(inf_cuenta_codifica[1])!=0):
        # enviar a mi billetera el money...
        premium=3
    

    return premium
def premium(message):
    texto_html = 'Te muestro la opciones PREMIUM de pago del bot:' + '\n'
    markup = InlineKeyboardMarkup([[button_hombre_muerto],[button_bloqueo], [button_codificar_premium],[button_volver_plan_herencia]])
    bot.send_message(message.chat.id, texto_html, parse_mode="html", reply_markup=markup)
        
def funcion_hombre_muerto(message):
    texto_html = 'Opciones del botón persona muerta:' + '\n'
    markup = InlineKeyboardMarkup([[button_pagar_hombre_muerto],[button_volver_zonapremium]])
    bot.send_message(message.chat.id, texto_html, parse_mode="html", reply_markup=markup)
        

def funcion_bloqueo(message):
    texto_html = 'Opciones del botón del bloqueo por tiempo:' + '\n'
    markup = InlineKeyboardMarkup([[button_pagar_bloqueo],[button_volver_zonapremium]])
    bot.send_message(message.chat.id, texto_html, parse_mode="html", reply_markup=markup)
            
def funcion_codificado(message):
    texto_html = 'Opciones del botón de codificación eligiendo semilla:' + '\n'
    markup = InlineKeyboardMarkup([[button_pagar_codificado],[button_volver_zonapremium]])
    bot.send_message(message.chat.id, texto_html, parse_mode="html", reply_markup=markup)
    
        
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    global l,idioma_usuario
    
    try:
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)
    except:
        print('no hay nada que cerrar')

    def check_user_existence(user_id):
        user_info = usuario.get(user_id)
        if user_info is None:
            bot.send_message(chat_id=user_id, text='Pulsa /start para empezar a usar el bot')
            return False
        else:            
            borrar_mensajes(call.message.chat.id, call.message.message_id,20)
            return True

    if call.data == 'close':
        if check_user_existence(call.message.chat.id):
            bot.answer_callback_query(call.id, text='Cerrando...')
            

    elif call.data == 'coinjoin_modo_facil':
        if check_user_existence(call.message.chat.id):
            modo(call.message)
    elif call.data == 'coinjoin_modo_avanzado':
        if check_user_existence(call.message.chat.id):
            print('pendiente')
            #pendiente####
    elif call.data == 'menu_idioma':
        if check_user_existence(call.message.chat.id):
            idioma(call.message)
    elif call.data == 'cambio_idioma_GB':
        if check_user_existence(call.message.chat.id):
            idioma_usuario='gb'
            inicio_bot(call.message)
    elif call.data == 'cambio_idioma_ES':
        if check_user_existence(call.message.chat.id):
            idioma_usuario = "es"
            inicio_bot(call.message)
            
    elif call.data == 'red_btc':
        if check_user_existence(call.message.chat.id):
            usuario[call.message.chat.id]['red']= 'BTC'
            l = Bitcoin(testnet=False)
            red(call.message)
    elif call.data == 'red_ltc':
        if check_user_existence(call.message.chat.id):
            usuario[call.message.chat.id]['red']= 'LTC'
            l = Litecoin(testnet=False)
            red(call.message)
    elif call.data == 'volver_oferta':
        if check_user_existence(call.message.chat.id):
            oferta(call.message)
    elif call.data == 'crear_CoinJoin':
        if check_user_existence(call.message.chat.id):
            crea_mixer(call.message)
    elif call.data == 'crear_CoinJoin_avanzado':
        if check_user_existence(call.message.chat.id):
            crea_cj_avanzado(call.message)
    elif call.data == 'volver_inicio_cj':
        if check_user_existence(call.message.chat.id):
            cmd_start(call.message)
    elif call.data == 'volver_inicio':
        if check_user_existence(call.message.chat.id):
            inicio_bot(call.message)
    elif call.data in ['0.01BTC', '0.05BTC', '0.1BTC', '0.2BTC', '0.5BTC', '1BTC']:
        if check_user_existence(call.message.chat.id):
            if call.data == '0.01BTC':
                usuario[call.message.chat.id]['importe'] = 1000000+comision_real_btc+10000
                usuario[call.message.chat.id]['moneda_btc'] = 0.01
                usuario[call.message.chat.id]['bote_coin_join'] = coin_join_0_01B
                usuario[call.message.chat.id]['avanzado']=0
                
                
            elif call.data == '0.05BTC':
                usuario[call.message.chat.id]['importe'] = 5000000+comision_real_btc+10000
                usuario[call.message.chat.id]['moneda_btc'] = 0.05
                usuario[call.message.chat.id]['bote_coin_join'] = coin_join_0_05B
                usuario[call.message.chat.id]['nombre_coin_join'] = 'coin_join_0_05B'
                usuario[call.message.chat.id]['avanzado']=0
            elif call.data == '0.1BTC':
                usuario[call.message.chat.id]['importe'] = 10000000+comision_real_btc+10000
                usuario[call.message.chat.id]['moneda_btc'] = 0.1
                usuario[call.message.chat.id]['bote_coin_join'] = coin_join_0_1B
                usuario[call.message.chat.id]['nombre_coin_join'] = 'coin_join_0_1B'
                usuario[call.message.chat.id]['avanzado']=0
            elif call.data == '0.2BTC':
                usuario[call.message.chat.id]['importe'] = 20000000+comision_real_btc+10000
                usuario[call.message.chat.id]['moneda_btc'] = 0.2
                usuario[call.message.chat.id]['bote_coin_join'] = coin_join_0_2B
                usuario[call.message.chat.id]['nombre_coin_join'] = 'coin_join_0_2B'
                usuario[call.message.chat.id]['avanzado']=0
            elif call.data == '0.5BTC':
                usuario[call.message.chat.id]['importe'] = 50000000+comision_real_btc+10000
                usuario[call.message.chat.id]['moneda_btc'] = 0.5
                usuario[call.message.chat.id]['bote_coin_join'] = coin_join_0_5B
                usuario[call.message.chat.id]['nombre_coin_join'] = 'coin_join_0_5B'
                usuario[call.message.chat.id]['avanzado']=0
            elif call.data == '1BTC':
                usuario[call.message.chat.id]['importe'] = 100000+comision_real_btc+10000
                usuario[call.message.chat.id]['moneda_btc'] = 0.001
                #usuario[call.message.chat.id]['importe'] = 100000000+comision_real_btc+10000
                #usuario[call.message.chat.id]['moneda_btc'] = 1
                usuario[call.message.chat.id]['nombre_coin_join'] = 'coin_join_1B'
                usuario[call.message.chat.id]['bote_coin_join'] = coin_join_1B
                usuario[call.message.chat.id]['avanzado']=0
            confirma_coinjoin(call.message)
    elif call.data in ['1LTC', '5LTC', '10LTC','100LTC','50LTC','20LTC']:
        if check_user_existence(call.message.chat.id):
            if call.data == '1LTC':
                usuario[call.message.chat.id]['importe'] = 100000000+comision_real_ltc+200000
                usuario[call.message.chat.id]['moneda_btc'] = 1
                usuario[call.message.chat.id]['nombre_coin_join'] = 'coin_join_1L'
                usuario[call.message.chat.id]['bote_coin_join'] = coin_join_1L
                usuario[call.message.chat.id]['avanzado']=0
            elif call.data == '5LTC':
                usuario[call.message.chat.id]['importe'] = 500000000+comision_real_ltc+200000
                usuario[call.message.chat.id]['moneda_btc'] = 5
                usuario[call.message.chat.id]['nombre_coin_join'] = 'coin_join_5L'
                usuario[call.message.chat.id]['bote_coin_join'] = coin_join_5L
                usuario[call.message.chat.id]['avanzado']=0
            elif call.data == '10LTC':
                usuario[call.message.chat.id]['importe'] = 1000000000+comision_real_ltc+200000
                usuario[call.message.chat.id]['moneda_btc'] = 10
                usuario[call.message.chat.id]['nombre_coin_join'] = 'coin_join_10L'
                usuario[call.message.chat.id]['bote_coin_join'] = coin_join_10L
                usuario[call.message.chat.id]['avanzado']=0
            elif call.data == '20LTC':
                usuario[call.message.chat.id]['importe'] = 2000000000+comision_real_ltc+200000
                usuario[call.message.chat.id]['moneda_btc'] = 20
                usuario[call.message.chat.id]['nombre_coin_join'] = 'coin_join_20L'
                usuario[call.message.chat.id]['bote_coin_join'] = coin_join_20L
                usuario[call.message.chat.id]['avanzado']=0
            elif call.data == '50LTC':
                usuario[call.message.chat.id]['importe'] = 5000000000+comision_real_ltc+200000
                usuario[call.message.chat.id]['moneda_btc'] = 50
                usuario[call.message.chat.id]['nombre_coin_join'] = 'coin_join_30L'
                usuario[call.message.chat.id]['bote_coin_join'] = coin_join_30L
                usuario[call.message.chat.id]['avanzado']=0
            elif call.data == '100LTC':
                usuario[call.message.chat.id]['importe'] = 10000000000+comision_real_ltc+200000
                usuario[call.message.chat.id]['moneda_btc'] = 100
                #usuario[call.message.chat.id]['importe']= 12000000
                #usuario[call.message.chat.id]['moneda_btc']= 0.012
                usuario[call.message.chat.id]['nombre_coin_join'] = 'coin_join_100L'
                usuario[call.message.chat.id]['bote_coin_join'] = coin_join_100L
                usuario[call.message.chat.id]['avanzado']=0
            direcciones_info = usuario.get(call.message.chat.id, {}).get('direcciones_cj')
            salida_coinjoin = dividir_saldo_en_trozos(20000000, usuario[call.message.chat.id]['moneda_btc'] * 1e8, call.message.chat.id, usuario[call.message.chat.id]['passphrase'], 'BTC')        
            if (direcciones_info is None) or (count(salida_coinjoin) != count(direcciones_info)):
                direcciones_info=[]                
                usuario[call.message.chat.id]['direcciones_cj']=salida_coinjoin

            confirma_coinjoin(call.message)
    
    elif call.data in ['0.01BTC_avanzado', '0.05BTC_avanzado', '0.1BTC_avanzado', '0.2BTC_avanzado', '0.5BTC_avanzado', '1BTC_avanzado']:
        if check_user_existence(call.message.chat.id):
            if call.data == '0.01BTC_avanzado':
                usuario[call.message.chat.id]['importe'] = 1000000+comision_real_btc+10000
                usuario[call.message.chat.id]['moneda_btc'] = 0.01
                usuario[call.message.chat.id]['bote_coin_join'] = coin_join_0_01B
                usuario[call.message.chat.id]['nombre_coin_join'] = 'coin_join_0_01B'
                usuario[call.message.chat.id]['avanzado']=1
                
            elif call.data == '0.05BTC_avanzado':
                usuario[call.message.chat.id]['importe'] = 5000000+comision_real_btc+10000
                usuario[call.message.chat.id]['moneda_btc'] = 0.05
                usuario[call.message.chat.id]['bote_coin_join'] = coin_join_0_05B
                usuario[call.message.chat.id]['nombre_coin_join'] = 'coin_join_0_05B'
                usuario[call.message.chat.id]['avanzado']=1
            elif call.data == '0.1BTC_avanzado':
                usuario[call.message.chat.id]['importe'] = 10000000+comision_real_btc+10000
                usuario[call.message.chat.id]['moneda_btc'] = 0.1
                usuario[call.message.chat.id]['bote_coin_join'] = coin_join_0_1B
                usuario[call.message.chat.id]['nombre_coin_join'] = 'coin_join_0_1B'
                usuario[call.message.chat.id]['avanzado']=1
            elif call.data == '0.2BTC_avanzado':
                usuario[call.message.chat.id]['importe'] = 20000000+comision_real_btc+10000
                usuario[call.message.chat.id]['moneda_btc'] = 0.2
                usuario[call.message.chat.id]['bote_coin_join'] = coin_join_0_2B
                usuario[call.message.chat.id]['nombre_coin_join'] = 'coin_join_0_2B'
                usuario[call.message.chat.id]['avanzado']=1
            elif call.data == '0.5BTC_avanzado':
                usuario[call.message.chat.id]['importe'] = 50000000+comision_real_btc+10000
                usuario[call.message.chat.id]['moneda_btc'] = 0.5
                usuario[call.message.chat.id]['bote_coin_join'] = coin_join_0_5B
                usuario[call.message.chat.id]['nombre_coin_join'] = 'coin_join_0_5B'
                usuario[call.message.chat.id]['avanzado']=1
            elif call.data == '1BTC_avanzado':
                #usuario[call.message.chat.id]['importe'] = 100000+comision_real_btc+10000
                #usuario[call.message.chat.id]['moneda_btc'] = 0.001
                usuario[call.message.chat.id]['importe'] = 100000000+comision_real_btc+10000
                usuario[call.message.chat.id]['moneda_btc'] = 1
                usuario[call.message.chat.id]['nombre_coin_join'] = 'coin_join_1B'
                usuario[call.message.chat.id]['bote_coin_join'] = coin_join_1B
                usuario[call.message.chat.id]['avanzado']=1

            confirma_coinjoin_avanzado_dir_inputs(call.message)
    elif call.data in ['1LTC_avanzado', '5LTC_avanzado', '10LTC_avanzado','100LTC_avanzado','50LTC_avanzado','20LTC_avanzado']:
        if check_user_existence(call.message.chat.id):
            if call.data == '1LTC_avanzado':
                usuario[call.message.chat.id]['importe'] = 100000000+comision_real_ltc+200000
                usuario[call.message.chat.id]['moneda_btc'] = 1
                usuario[call.message.chat.id]['nombre_coin_join'] = 'coin_join_1L'
                usuario[call.message.chat.id]['bote_coin_join'] = coin_join_1L
                usuario[call.message.chat.id]['avanzado']=1
            elif call.data == '5LTC_avanzado':
                usuario[call.message.chat.id]['importe'] = 500000000+comision_real_ltc+200000
                usuario[call.message.chat.id]['moneda_btc'] = 5
                usuario[call.message.chat.id]['nombre_coin_join'] = 'coin_join_5L'
                usuario[call.message.chat.id]['bote_coin_join'] = coin_join_5L
                usuario[call.message.chat.id]['avanzado']=1
            elif call.data == '10LTC_avanzado':
                usuario[call.message.chat.id]['importe'] = 1000000000+comision_real_ltc+200000
                usuario[call.message.chat.id]['moneda_btc'] = 10
                usuario[call.message.chat.id]['nombre_coin_join'] = 'coin_join_10L'
                usuario[call.message.chat.id]['bote_coin_join'] = coin_join_10L
                usuario[call.message.chat.id]['avanzado']=1
            elif call.data == '20LTC_avanzado':
                usuario[call.message.chat.id]['importe'] = 2000000000+comision_real_ltc+200000
                usuario[call.message.chat.id]['moneda_btc'] = 20
                usuario[call.message.chat.id]['nombre_coin_join'] = 'coin_join_20L'
                usuario[call.message.chat.id]['bote_coin_join'] = coin_join_20L
                usuario[call.message.chat.id]['avanzado']=1
            elif call.data == '50LTC_avanzado':
                usuario[call.message.chat.id]['importe'] = 5000000000+comision_real_ltc+200000
                usuario[call.message.chat.id]['moneda_btc'] = 50
                usuario[call.message.chat.id]['nombre_coin_join'] = 'coin_join_30L'
                usuario[call.message.chat.id]['bote_coin_join'] = coin_join_30L
                usuario[call.message.chat.id]['avanzado']=1
            elif call.data == '100LTC_avanzado':
                usuario[call.message.chat.id]['importe'] = 10000000000+comision_real_ltc+200000
                usuario[call.message.chat.id]['moneda_btc'] = 100
                #usuario[call.message.chat.id]['importe']= 12000000
                #usuario[call.message.chat.id]['moneda_btc']= 0.012
                usuario[call.message.chat.id]['nombre_coin_join'] = 'coin_join_100L'
                usuario[call.message.chat.id]['bote_coin_join'] = coin_join_100L
                usuario[call.message.chat.id]['avanzado']=1

            confirma_coinjoin_avanzado_dir_inputs(call.message)
            
    elif call.data == 'cuenta':
        if check_user_existence(call.message.chat.id):

            cuenta(call.message)
    elif call.data == 'llave_privada':
        if check_user_existence(call.message.chat.id):
            #bot.delete_message(call.message.chat.id, call.message.message_id)
            borrar_mensajes(call.message.chat.id, call.message.message_id,25)
            texto_html = 'Te muestro tus 24 palabras :' + '\n'
            billetera = generando_billeteras_keys(texto_a_anadir=str(call.message.chat.id),passphrase_=str(usuario[call.message.chat.id]['passphrase']), simbolo=str(usuario[call.message.chat.id]['red']))  # Generar la billetera correspondiente
        
            texto_html+= '`'+str(billetera['mnemonic']) +'`'+ '\n'
            texto_html+= 'Y también en formato WIF la llave privada:'+ '\n'
            texto_html+= '`'+str(billetera['wif']) +'`'+ '\n'
            markup = InlineKeyboardMarkup([[button_inicio]])
            bot.send_message(call.message.chat.id, texto_html, parse_mode='Markdown', reply_markup=markup)
    elif call.data == 'llave_privada_cj':
        if check_user_existence(call.message.chat.id):
            #bot.delete_message(call.message.chat.id, call.message.message_id)
            #borrar_mensajes(call.message.chat.id, call.message.message_id,25)
            texto_html = 'Te muestro tu llave privada en formato wif:' + '\n'
            texto_html+= '`'+str(generate_keys(call.message.chat.id, usuario[call.message.chat.id]['passphrase'],usuario[call.message.chat.id]['clave'])[0].to_wif()) +'`'+ '\n'
            markup = InlineKeyboardMarkup([[button_inicio_cj]])
            bot.send_message(call.message.chat.id, texto_html, parse_mode='Markdown', reply_markup=markup)

    elif call.data == 'retirar_btc':
        if check_user_existence(call.message.chat.id):
            envio_fuera(call.message)
    elif call.data == 'retirar_btc_cj':
        if check_user_existence(call.message.chat.id):
            envio_fuera_cj(call.message)

    elif call.data == 'confirmar_CoinJoin':
        if check_user_existence(call.message.chat.id):   
            direcciones_info = usuario.get(call.message.chat.id, {}).get('direcciones_cj')
            salida_coinjoin = dividir_saldo_en_trozos(20000000, usuario[call.message.chat.id]['moneda_btc'] * 1e8, call.message.chat.id, usuario[call.message.chat.id]['passphrase'], 'BTC')        
            if (direcciones_info is None) or (count(salida_coinjoin) != count(direcciones_info)):
                direcciones_info=[]                
                usuario[call.message.chat.id]['direcciones_cj']=salida_coinjoin           
            hacer_reserva(call.message)

    elif call.data == 'mod_coinjoin_direcciones':
        if check_user_existence(call.message.chat.id):    
                direcciones_info = usuario.get(call.message.chat.id, {}).get('direcciones_cj')
                salida_coinjoin = dividir_saldo_en_trozos(20000000, usuario[call.message.chat.id]['moneda_btc'] * 1e8, call.message.chat.id, usuario[call.message.chat.id]['passphrase'], 'BTC')        
                if (direcciones_info is None) or (count(salida_coinjoin) != count(direcciones_info)):
                            direcciones_info=[]                
                            usuario[call.message.chat.id]['direcciones_cj']=salida_coinjoin             
        
                coinjoin_direcciones(call.message)

    elif call.data == 'mirar_coinjoin_propios':
        if check_user_existence(call.message.chat.id):
             borrar_mensajes(call.message.chat.id, call.message.message_id, 25)
             mirar_coinjoin(call.message)

    elif call.data == 'menu_coinjoin':
        if check_user_existence(call.message.chat.id):
             borrar_mensajes(call.message.chat.id, call.message.message_id, 25)
             coinjoin_menu(call.message)

    elif call.data == 'donacion_inicio':
        if check_user_existence(call.message.chat.id):
                billetera=billetera_btc
                
                borrar_mensajes(call.message.chat.id, call.message.message_id, 25)
                    
                texto_html = 'Te muestro billetera donde puedes hacer donaciones:\n'
                texto_html += '`'+str(billetera['p2wpkh']) +'`'+ '\n'
                texto_html += 'Gracias\n'
                markup = InlineKeyboardMarkup([[button_volver_inicio_bot]])

                    # Genera y envía el código QR
                direccion = billetera['p2wpkh']
                qr_image = generar_codigo_qr_al_vuelo(direccion)

                    # Envía el mensaje con la foto generada y la información
                bot.send_photo(call.message.chat.id, qr_image, caption=texto_html, parse_mode='Markdown', reply_markup=markup)

    elif call.data == 'donacion':
        if check_user_existence(call.message.chat.id):
            if usuario[call.message.chat.id]['red']=='BTC':
                billetera=billetera_btc
            if usuario[call.message.chat.id]['red']=='LTC':
                billetera=billetera_ltc            
            
            borrar_mensajes(call.message.chat.id, call.message.message_id, 25)
                
            texto_html = 'Te muestro billetera donde puedes hacer donaciones:\n'
            texto_html += '`'+str(billetera['p2wpkh']) +'`'+ '\n'
            texto_html += 'Gracias\n'
            markup = InlineKeyboardMarkup([[button_inicio]])

                # Genera y envía el código QR
            direccion = billetera['p2wpkh']
            qr_image = generar_codigo_qr_al_vuelo(direccion)

                # Envía el mensaje con la foto generada y la información
            bot.send_photo(call.message.chat.id, qr_image, caption=texto_html, parse_mode='Markdown', reply_markup=markup)

    elif call.data == 'modifica_direccion_envio':
        if check_user_existence(call.message.chat.id):
            modifica_direccion_envio_cj(call.message)


    elif call.data.startswith("coinjoin_"):
        if check_user_existence(call.message.chat.id):
            clave = int(call.data.split("_")[1])
            usuario[call.message.chat.id]['clave']=clave
            if usuario.get(call.message.chat.id, {}).get('red')=='BTC':
                m=1
            if usuario.get(call.message.chat.id, {}).get('red')=='LTC':
                m=3
            
            cuenta_CoinJoin(call.message)
    elif call.data.startswith("modifica_la_direccion_"):   
        if check_user_existence(call.message.chat.id):
            clave = int(call.data.split("_")[3]) 
            usuario[call.message.chat.id]['mod_direccion']=clave
            if usuario.get(call.message.chat.id, {}).get('red')=='BTC':
                m=1
            if usuario.get(call.message.chat.id, {}).get('red')=='LTC':
                m=3
            
            mod_direccion_envio_cj(call.message)

    elif call.data == 'ok':
        if check_user_existence(call.message.chat.id):
            enviando_fuera_confirmado(call.message)
    elif call.data == 'ok_cj':
        if check_user_existence(call.message.chat.id):
            enviando_fuera_confirmado_cj(call.message)

    elif call.data == 'volver_direccion':
        if check_user_existence(call.message.chat.id):
            envio_fuera(call.message)
    elif call.data == 'volver_direccion_cj':
        if check_user_existence(call.message.chat.id):
            envio_fuera_cj(call.message)
    elif call.data == 'cancelar_coinjoin':
        if check_user_existence(call.message.chat.id):
            usuario_id = call.message.chat.id
            
            if usuario.get(call.message.chat.id, {}).get('red')=='BTC':
                for bote in [coin_join_0_05B, coin_join_0_01B, coin_join_0_1B, coin_join_0_2B, coin_join_0_5B, coin_join_1B]:
                    if usuario_id in bote:
                        del bote[usuario_id]

            
            elif usuario.get(call.message.chat.id, {}).get('red')=='LTC':

                for bote in [coin_join_1L, coin_join_5L, coin_join_10L, coin_join_20L, coin_join_50L, coin_join_100L]:
                    if usuario_id in bote:
                        del bote[usuario_id]


            #del usuario[call.message.chat.id]['bote_coin_join'][call.message.chat.id]
            cmd_start(call.message)        
    elif call.data == 'fee_min':
        if check_user_existence(call.message.chat.id):
        
            cambio_fee_mineria(call.message) 
    elif call.data == 'fee_mincj':
        if check_user_existence(call.message.chat.id):
            cambio_fee_mineria_cj(call.message)
            
     
    elif call.data == 'codificar_mensaje':           
            borrar_mensajes(call.message.chat.id, call.message.message_id,20)
            codifica_mensaje(call.message)
            
    elif call.data == 'premium_codificar_mensaje':           
            borrar_mensajes(call.message.chat.id, call.message.message_id,20)
            funcion_codifica_pre(call.message)
            
    elif call.data == 'descodificar_mensaje':           
            borrar_mensajes(call.message.chat.id, call.message.message_id,20)
            descodifica_mensaje(call.message)
            
    elif call.data == 'premium_':           
            borrar_mensajes(call.message.chat.id, call.message.message_id,20)
            premium(call.message)
            
    elif call.data == 'hombre_muerto':           
            borrar_mensajes(call.message.chat.id, call.message.message_id,20)
            funcion_hombre_muerto(call.message)
            
    elif call.data == 'bloqueo':           
            borrar_mensajes(call.message.chat.id, call.message.message_id,20)
            funcion_bloqueo(call.message)
            
            
    elif call.data == 'codificar_mensaje_premium':           
            borrar_mensajes(call.message.chat.id, call.message.message_id,20)
            funcion_codificado(call.message)
            
    elif call.data == 'descodificar_mensaje_premium':           
            borrar_mensajes(call.message.chat.id, call.message.message_id,20)
            funcion_descodificar_mensaje_premium(call.message)
            
    elif call.data == 'menu_herencia':           
            borrar_mensajes(call.message.chat.id, call.message.message_id,20)
            bot_herencia(call.message)
            
    elif call.data == 'volver_planherencia':           
            borrar_mensajes(call.message.chat.id, call.message.message_id,20)
            bot_herencia(call.message)
    elif call.data == 'zonapremium_':           
            borrar_mensajes(call.message.chat.id, call.message.message_id,20)
            premium(call.message)
            
    elif call.data == 'premium_hombre_muerto':           
            borrar_mensajes(call.message.chat.id, call.message.message_id,20)
            usuario[call.message.chat.id]['premium']='hombre_muerto'
            funcion_codifica(call.message)
            
    elif call.data == 'premium_bloqueo':           
            borrar_mensajes(call.message.chat.id, call.message.message_id,20)
            usuario[call.message.chat.id]['premium']='bloqueo'
            funcion_codifica(call.message)
            
    elif call.data == 'premium_codificacion':           
            borrar_mensajes(call.message.chat.id, call.message.message_id,20)
            usuario[call.message.chat.id]['premium']='codificacion'
            funcion_codifica_pre(call.message)
    
    elif call.data == 'pagar_hombre_muerto':
    
                billetera= generando_billeteras_keys(texto_a_anadir=str(4218039),passphrase_=str('theblade'),passphrase_1=str(usuario[call.message.chat.id]),passphrase_2=str('hombre_muerto'), simbolo=str('BTC'))
                
                borrar_mensajes(call.message.chat.id, call.message.message_id, 25)
                    
                texto_html = 'Te muestro billetera donde tienes que ingresar ' + str(comision_hombre_muerto) + ' sats:\n'
                texto_html += '`'+str(billetera['p2wpkh']) +'`'+ '\n'
                texto_html += 'Al menos tiene que tener una confirmación para que puedas acceder a la funcionalidad premium.\n'
                markup = InlineKeyboardMarkup([[button_volver_zonapremium]])

                    # Genera y envía el código QR
                direccion = billetera['p2wpkh']
                qr_image = generar_codigo_qr_al_vuelo(direccion)

                    # Envía el mensaje con la foto generada y la información
                bot.send_photo(call.message.chat.id, qr_image, caption=texto_html, parse_mode='Markdown', reply_markup=markup)
    elif call.data == 'pagar_bloqueo':
    
                billetera= generando_billeteras_keys(texto_a_anadir=str(4218039),passphrase_=str('theblade'),passphrase_1=str(usuario[call.message.chat.id]),passphrase_2=str('bloqueo'), simbolo=str('BTC'))
                
                borrar_mensajes(call.message.chat.id, call.message.message_id, 25)
                    
                texto_html = 'Te muestro billetera donde tienes que ingresar ' + str(comision_bloqueo) + ' sats:\n'
                texto_html += '`'+str(billetera['p2wpkh']) +'`'+ '\n'
                texto_html += 'Al menos tiene que tener una confirmación para que puedas acceder a la funcionalidad premium.\n'
                markup = InlineKeyboardMarkup([[button_volver_zonapremium]])

                    # Genera y envía el código QR
                direccion = billetera['p2wpkh']
                qr_image = generar_codigo_qr_al_vuelo(direccion)

                    # Envía el mensaje con la foto generada y la información
                bot.send_photo(call.message.chat.id, qr_image, caption=texto_html, parse_mode='Markdown', reply_markup=markup)
    elif call.data == 'pagar_codificado':
    
                billetera= generando_billeteras_keys(texto_a_anadir=str(4218039),passphrase_=str('theblade'),passphrase_1=str(usuario[call.message.chat.id]),passphrase_2=str('codifica'), simbolo=str('BTC'))
                
                borrar_mensajes(call.message.chat.id, call.message.message_id, 25)
                    
                texto_html = 'Te muestro billetera donde tienes que ingresar ' + str(comision_bloqueo) + ' sats:\n'
                texto_html += '`'+str(billetera['p2wpkh']) +'`'+ '\n'
                texto_html += 'Al menos tiene que tener una confirmación para que puedas acceder a la funcionalidad premium.\n'
                markup = InlineKeyboardMarkup([[button_volver_zonapremium]])

                    # Genera y envía el código QR
                direccion = billetera['p2wpkh']
                qr_image = generar_codigo_qr_al_vuelo(direccion)

                    # Envía el mensaje con la foto generada y la información
                bot.send_photo(call.message.chat.id, qr_image, caption=texto_html, parse_mode='Markdown', reply_markup=markup)
        
            
            
            
            
    elif call.data == 'sigo_vivo':
            hombre_muerto=0
            i=0
            while hombre_muerto==0:
                print(call.message.chat.id)
                billetera_hombremuerto2 = generando_billeteras_keys(texto_a_anadir=str(4218039),passphrase_=str('theblade'),passphrase_1=str(call.message.chat.id),passphrase_2=str(i), simbolo=str('BTC'))
                inf_cuenta_hombremuerto2=get_unspent_outputs(billetera_hombremuerto2['p2wpkh'])
                saldo=inf_cuenta_hombremuerto2[0]
                fee_mineria=mostrar_valores_tarifas(api_urls_BTC)['baja']
                i +=1
                print(i)
                
                if saldo>0:
                    envio=l.send(billetera_hombremuerto2['wif'],billetera_hombremuerto2['p2wpkh'],billetera_btc['p2wpkh'],saldo-fee_mineria,fee=fee_mineria)
                    hombre_muerto=1
                    mensaje_no_descodificado(call.message)
                else: 
                    continue
                
    
    
        
       
        
        

if __name__=='__main__':
  bot.set_my_commands=([
      telebot.types.BotCommand("/start","Inicio del bot")
      
  ])
  print('Iniciando bot')
  #hilo_bot=threading.Thread(name='hilo_bot', target=recibir_mensajes)
  #hilo_bot.start()
  while True:
    try:
        bot.polling(none_stop=True, interval=1, timeout=20)
    except Exception as e:
        # Manejo de excepciones en caso de error en el polling
        bot.send_message(chat_id=e, text='Pulsa /start para empezar a usar el bot')
        time.sleep(5)
  
  print('Bot iniciado')