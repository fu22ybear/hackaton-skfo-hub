"""
Config values
"""

import os


class Config:
    def __init__(self):
        self.__app_name = os.getenv('APP_NAME')

        self.__log_level = os.getenv('LOG_LEVEL', 'INFO')

        self.__oscillograms_store_dir = os.getenv('OSCILLOGRAMS_STORE_DIR')

        self.__kafka_host = os.getenv('KAFKA_HOST')
        self.__kafka_port = os.getenv('KAFKA_PORT')
        self.__kafka_oscillograms_topic_name = os.getenv('KAFKA_OSCILLOGRAMS_TOPIC_NAME')

    @property
    def app_name(self) -> str:
        return self.__app_name

    @property
    def log_level(self) -> str:
        return self.__log_level

    @property
    def oscillograms_store_dir(self) -> str:
        return self.__oscillograms_store_dir

    @property
    def kafka_host(self) -> str:
        return self.__kafka_host

    @property
    def kafka_port(self) -> int:
        return int(self.__kafka_port)

    @property
    def kafka_oscillograms_topic_name(self) -> str:
        return self.__kafka_oscillograms_topic_name
