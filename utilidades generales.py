# Módulo de Utilidades Generales

import requests
import time

def validar_direccion_bitcoin(address, moneda):
    """Valida si una dirección de Bitcoin es válida."""
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

def send_message_to_ids(id_list, message_text):
    """Envía un mensaje a cada ID en la lista proporcionada."""
    for id in id_list:
        bot.send_message(id, message_text)

def obtener_informacion_direccion(direccion, criptomoneda):
    """Obtiene información sobre una dirección de criptomoneda."""
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

  