import logging

logging.basicConfig(filename='weather_alert.log', level=logging.INFO)
logger = logging.getLogger("weather_alert")


def get_logger():
    return logger
