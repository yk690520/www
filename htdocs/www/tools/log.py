from logging import Logger
logger=None
'''
debug
infor
waring
error
critical

'''
def set_logger(temp_logger):
    global logger
    logger=temp_logger

def get_logger():
    global logger
    return logger