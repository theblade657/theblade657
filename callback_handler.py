      
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
                