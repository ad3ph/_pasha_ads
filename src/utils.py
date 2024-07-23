from random import sample, randint
import time
from config import WebSettings
from src.logger import logger

def get_tmp_name(length=12):
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    return "".join(sample(chars, length))

first = lambda x: x[list(x.keys())[0]]

def random_wait():
    wait = randint(WebSettings.avito_random_time_min, WebSettings.avito_random_time_max)
    logger.info(f"Waiting {wait} seconds...")
    time.sleep(wait)