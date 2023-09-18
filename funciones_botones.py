# 3. Funciones de Botones
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