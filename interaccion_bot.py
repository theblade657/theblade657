import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

# Inicialización del bot
bot = telebot.TeleBot('6284649:AWwb2zdKibE-IY23LU')

def envio_fuera(message):
    #bot.delete_message(message.chat.id, message.message_id )
    money=obtener_informacion_direccion(usuario[message.chat.id]['direccion'], usuario[message.chat.id]['red'])[0]
    if money > 0:
        msg = bot.send_message(message.chat.id, 'Indica la dirección donde quieres que se te envien los fondos\n\n⚠️⚠️ la dirección compruébala 3 veces, los fondos enviados no se pueden recuperar \n\n ✔️ En el siguiente paso te muestro la información para que lo revises ️')
        bot.register_next_step_handler(msg, confirmacion_envio_fuera)
    else:
        markup = InlineKeyboardMarkup([[button_inicio]])
        bot.send_message(message.chat.id, 'Actualmente no tienes saldo confirmado en tu cuenta', reply_markup=markup)

def confirmacion_envio_fuera(message):
    if message.text:
        usuario[message.chat.id]['direccion_envio']= message.text
        red=usuario[message.chat.id]['red']
        destino=usuario[message.chat.id]['direccion_envio']
        saldo=usuario[message.chat.id]['money']
        llave=usuario[message.chat.id]['llave_hex']
        direccion=usuario[message.chat.id]['direccion']
        
        # ... (resto del código de la función)

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

    # ... (resto del código de la función)

# ... (cualquier otra función relacionada con la interacción del bot)
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
    
                