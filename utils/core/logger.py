import sys
import requests
from loguru import logger
from data import config

TELEGRAM_API_URL = f"https://api.telegram.org/bot{config.BOT_TOKEN}/sendMessage"
def send_log_to_telegram(message):
    try:
        response = requests.post(TELEGRAM_API_URL, data={'chat_id': config.CHAT_ID, 'text': message})
        if response.status_code != 200:
            logger.error(f"Failed to send log to Telegram: {response.text}")
    except Exception as e:
        logger.error(f"Failed to send log to Telegram: {e}")

def logging_setup():
    format_info = "<green>{time:HH:mm:ss.SS}</green> | <blue>{level}</blue> | <level>{message}</level>"
    logger.remove()

    logger.add(sys.stdout, colorize=True, format=format_info, level="INFO")
    logger.add("blum_bot.log", rotation="50 MB", compression="zip", format=format_info, level="TRACE")
    if config.USE_TG_BOT:
        logger.add(lambda msg: send_log_to_telegram(msg), format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}", level="INFO")

logging_setup()
