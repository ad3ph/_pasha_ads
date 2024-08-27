from random import sample, randint
import time
from config import WebSettings, purpose_keywords
from src.logger import logger
from datetime import datetime, timedelta

def get_tmp_name(length=12):
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    return "".join(sample(chars, length))

first = lambda x: x[list(x.keys())[0]]

remove_spaces = lambda x: "".join([y for y in x if y != " "])

def random_wait():
    wait = randint(WebSettings.avito_random_time_min, WebSettings.avito_random_time_max)
    logger.info(f"Waiting {wait} seconds...")
    time.sleep(wait)

def get_dates_span(date_offset):
    today = datetime.now()
    
    # Calculate the dates
    start_date = today - timedelta(days=date_offset)
    end_date = today + timedelta(days=date_offset)
    
    # Format the dates in "dd.mm.yyyy"
    start_date_str = start_date.strftime("%d.%m.%Y")
    end_date_str = end_date.strftime("%d.%m.%Y")
    
    return (start_date_str, end_date_str)

def understand_purpose(text):
    for purpose_name, purpose_words_list in purpose_keywords.items():
        if any([x in text for x in purpose_words_list]):    
            return purpose_name
    return ""