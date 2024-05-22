import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

import logging

log_filename = "application.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(filename)s:%(lineno)d #%(levelname)-8s "
    "[%(asctime)s] - %(name)s - %(message)s",
    handlers=[logging.FileHandler(log_filename), logging.StreamHandler()],
)
logger = logging.getLogger("AhrefsApiLogger")

from dotenv import load_dotenv


class DataManager:
    __instance = None

    @staticmethod
    def get_instance():
        if DataManager.__instance is None:
            DataManager()
        return DataManager.__instance

    def __init__(self):
        if DataManager.__instance is not None:
            raise Exception("DataManger is a singleton class")
        else:
            load_dotenv()
            self.token = self.get_token()
            DataManager.__instance = self

    def get_token(self):
        token = os.getenv("TOKEN")
        return token
