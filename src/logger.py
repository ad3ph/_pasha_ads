from loguru import logger
logger.add("log/log.txt", level="TRACE", rotation="1day")