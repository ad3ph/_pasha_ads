from loguru import logger
logger.add("log/log.txt", level="DEBUG", rotation="1day")