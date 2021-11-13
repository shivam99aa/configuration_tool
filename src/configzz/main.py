import logging

logging.basicConfig(level='INFO') # update this from config file. If not defined default will be INFO
logger = logging.getLogger("configzz")


def main():
    logger.info("This is a sample log.")
