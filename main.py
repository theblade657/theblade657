import telebot
import time
# Importaciones adicionales que puedas necesitar

# Inicialización del bot
bot = telebot.TeleBot(TOKEN)  # Asegúrate de que TOKEN esté definido

if __name__=='__main__':
    bot.set_my_commands=([
        telebot.types.BotCommand("/start","Inicio del bot")
    ])
    print('Iniciando bot')
    while True:
        try:
            bot.polling(none_stop=True, interval=1, timeout=20)
        except Exception as e:
            bot.send_message(chat_id=e, text='Pulsa /start para empezar a usar el bot')
            time.sleep(5)
    print('Bot iniciado')
