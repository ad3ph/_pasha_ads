import random
import time

def dummy_1():
    logger.info("1")
    time.sleep(2)

def dummy_2():
    logger.info("2")    
    time.sleep(2)

def dummy_3():
    logger.info("3")
    time.sleep(2)
    if random.random() > 0.8:
        raise NotImplementedError