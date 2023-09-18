from cryptos import *
from bitcoin import *
import requests
import json
from statistics import median
from datetime import datetime
from hdwallet import HDWallet
from hdwallet.utils import generate_entropy
from hdwallet.symbols import BTC as SYMBOL
import time

objetivo_coinjoin=2
comision_real_ltc=5000000
comision_real_btc=18000
comision_hombre_muerto=50000
comision_bloqueo=50000
comision_codifica=50000

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
  
def mirar_coinjoin(message):
    buttons = []
    mixer_reservados = {}
    i = 1
    red = usuario[message.chat.id]['red']
    if red == 'BTC':
        criptomoneda = 'BTC'
        billetera = 1
    elif red == 'LTC':
        criptomoneda = 'LTC'
        billetera = 3
    coin_joins_activos, saldos = generar_lista_billeteras(message.chat.id, usuario[message.chat.id]['passphrase'], red, message)
    elementos = {}  # Diccionario para almacenar los elementos con nombres dinámicos
    for i, elemento in enumerate(coin_joins_activos):
        print(elemento)
        nombre_direcc = 'direcc_btc_' + str(i)
        nombre_llave_hex = 'llave_hex_' + str(i)
        saldo = 'saldos_' + str(i)
        elementos[nombre_direcc] = elemento['p2wpkh']
        elementos[nombre_llave_hex] = elemento['wif']
        elementos[saldo] = saldos[i]
        button_text = "✔️ CoinJoin de {} {}".format(elementos['saldos_' + str(i)] / 1e8, criptomoneda)
        buttons.append([InlineKeyboardButton(text=button_text, callback_data="coinjoin_" + str(i))])
    usuario[message.chat.id]['coinjoin'] = elementos
    if len(coin_joins_activos) > 0:
        for clave, valor in mixer_reservados.items():
            llave = valor['llave_CJ']
            direccion = valor['direccion_CJ']
            saldo = valor['datos'][0]
            button_text = "✔️ YA Disponible mixer para {} billetereras, tamaño {} {}".format(datos[0], datos[1], criptomoneda)
            buttons.append([InlineKeyboardButton(text=button_text, callback_data="muestra_mixer_" + str(reserva))])
        if buttons:
            reply_markup = InlineKeyboardMarkup(buttons + [[button_inicio]])
            bot.send_message(message.chat.id, "Selecciona la moneda que quieras recuperar:", reply_markup=reply_markup)
    else:
        texto_html = 'No tienes ningún CoinJoin' + '\n'
        markup = InlineKeyboardMarkup([[button_inicio]])
        bot.send_message(message.chat.id, texto_html, parse_mode="html", reply_markup=markup)
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