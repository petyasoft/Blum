import sys
from loguru import logger


def logging_setup():
    format_info = "<green>{time:HH:mm:ss.SS}</green> | <blue>{level}</blue> | <level>{message}</level>"
    logger.remove()

    logger.add(sys.stdout, colorize=True, format=format_info, level="INFO")
    
    logger.add("blum_bot.log", rotation="50 MB", compression="zip", format=format_info, level="TRACE")

logging_setup()
