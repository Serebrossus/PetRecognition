import telebot as tb
import log_manager.loger as lgr
from time import sleep

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

@bot.message_handler(commands=['log'])
def send_log(message):
    log = open(lgr.HISTORY_LOG, 'r')
    bot.send_document(message.chat.id, log)
    try:
        file = open(lgr.LAST_CLEANING_HISTORY, 'r')
    except FileNotFoundError:
        bot.send_message(message.chat.id, 'last cleaning history not found')
    else:
        date_last_cleaning_log = file.read()
        file.close()
    
    bot.send_message(message.chat.id, '''
    Last cleaning history in {}
    '''.format(date_last_cleaning_log))

try:
    bot.polling()
except OSError as e:
    bot.stop_polling()
    lgr.write_error(type(e).__name__)
    sleep(10)
    bot.polling()