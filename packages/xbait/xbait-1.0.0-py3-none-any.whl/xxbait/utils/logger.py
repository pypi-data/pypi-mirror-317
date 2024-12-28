# nyx/utils/logger.py
import logging

def setup_logging():
    logging.basicConfig(
        filename="script.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )
