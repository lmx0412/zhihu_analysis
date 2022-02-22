import logging
from logging import handlers
import time
import settings
import datetime


format_dict = {
   "complex" : logging.Formatter('%(asctime)s [%(threadName)s:%(thread)d] [%(name)s:%(lineno)d] [%(module)s:%(funcName)s] [%(levelname)s]- %(message)s'),
   "standard" : logging.Formatter('%(asctime)s [%(name)s:%(lineno)d] [%(module)s:%(funcName)s] [%(levelname)s]- %(message)s'),
   "simple" : logging.Formatter('[%(levelname)s][%(asctime)s][%(filename)s:%(lineno)d]%(message)s'),
   "simplest" : logging.Formatter('[%(asctime)s][%(levelname)s]- %(message)s'),
}

def get_filename():
    return "logs/" + time.strftime('%Y-%m-%d', time.localtime(time.time())) + ".log"

def init_logging():
    # 初始化日志文件handler
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    file_handler = handlers.TimedRotatingFileHandler(get_filename(), when='D', interval=1, backupCount=5)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(format_dict["complex"])
    logger.addHandler(file_handler)

    # 初始化日志console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    formatter_console = format_dict["standard"]
    console_handler.setFormatter(formatter_console)
    logger.addHandler(console_handler)

init_logging()
