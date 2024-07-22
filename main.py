from src.logger import logger
from src.handlers import dev_gov_ru, dev

REQUESTS = [
    "TORGI_1_INVESTMOSCOW",
    "TORGI_2_INVESTMOSCOW",
    "TORGI_ROSSII",
    "TBANKROT",
    "TORGI_GOV_RU",
    "AVITO",
    "CYAN"
    ]

def main():
    ...
    
if __name__ == "__main__":
    # dev()
    dev_gov_ru()