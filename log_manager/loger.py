import logging

HISTORY_LOG = 'history_work.log'
LAST_CLEANING_HISTORY = 'last_cleaning_log.txt'

logging.basicConfig(filename=HISTORY_LOG, level=logging.INFO)

def write_error(description_error):
    logging.error('''
    Error: {error} 
    '''.format(error=description_error))

def check_log_size():
    if (getsize(HISTORY_LOG) >= 1048576):
        run(['rm', HISTORY_LOG])

        last_cleaning_log = datetime.datetime.today().strftime('%d.%m.%Y in %H:%M')

        file = open(LAST_CLEANING_HISTORY, 'w')
        file.write(str(last_cleaning_log))
        file.close()

check_log_size()