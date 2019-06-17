import telebot as tb
import log_manager.loger

BOT_TOKEN = ''

bot = tb.Telebot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id,
    '''
    Hello. Press any text...
    ''')

@bot.message_handler(content_types=['text'])
def repeat_all_messages(message):
    bot.reply_to(message, 'I do not know what is it!')


try:
    bot.polling()
except OSError as e:
    bot.stop_polling()
    loger.write_error(type(e).__name__)
    sleep(10)
    bot.polling()