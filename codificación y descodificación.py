
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
