"""
Config values
"""

import os


class Config:
    def __init__(self):
        self.__app_name = os.getenv('APP_NAME')

        self.__log_level = os.getenv('LOG_LEVEL', 'INFO')

        self.__oscillograms_tmp_store_dir = os.getenv('OSCILLOGRAMS_TMP_STORE_DIR')

        self.__kafka_host = os.getenv('KAFKA_HOST')
        self.__kafka_port = os.getenv('KAFKA_PORT')
        self.__kafka_oscillograms_topic_name = os.getenv('KAFKA_OSCILLOGRAMS_TOPIC_NAME')

        self.__minio_host = os.getenv('MINIO_HOST')
        self.__minio_port = os.getenv('MINIO_PORT')
        self.__minio_access_key = os.getenv('MINIO_ACCESS_KEY')
        self.__minio_secret_key = os.getenv('MINIO_SECRET_KEY')
        self.__minio_bucket_name = os.getenv('MINIO_BUCKET_NAME')

        # self.__clickhouse_host = os.getenv('CLICKHOUSE_HOST')
        # self.__clickhouse_port = os.getenv('CLICKHOUSE_PORT')
        # self.__clickhouse_http_port = os.getenv('CLICKHOUSE_HTTP_PORT')
        # self.__clickhouse_user = os.getenv('CLICKHOUSE_USER')
        # self.__clickhouse_password = os.getenv('CLICKHOUSE_PASSWORD')

    @property
    def app_name(self) -> str:
        return self.__app_name

    @property
    def log_level(self) -> str:
        return self.__log_level

    @property
    def oscillograms_tmp_store_dir(self) -> str:
        return self.__oscillograms_tmp_store_dir

    @property
    def kafka_host(self) -> str:
        return self.__kafka_host

    @property
    def kafka_port(self) -> int:
        return int(self.__kafka_port)

    @property
    def kafka_oscillograms_topic_name(self) -> str:
        return self.__kafka_oscillograms_topic_name

    @property
    def minio_host(self) -> str:
        return self.__minio_host

    @property
    def minio_port(self) -> int:
        return int(self.__minio_port)

    @property
    def minio_access_key(self) -> str:
        return self.__minio_access_key

    @property
    def minio_secret_key(self) -> str:
        return self.__minio_secret_key

    @property
    def minio_bucket_name(self) -> str:
        return self.__minio_bucket_name

    # @property
    # def clickhouse_host(self) -> str:
    #     return self.__clickhouse_host
    #
    # @property
    # def clickhouse_port(self) -> int:
    #     return int(self.__clickhouse_port)
    #
    # @property
    # def clickhouse_http_port(self) -> int:
    #     return int(self.__clickhouse_http_port)
    #
    # @property
    # def clickhouse_user(self) -> str:
    #     return self.__clickhouse_user
    #
    # @property
    # def clickhouse_password(self) -> str:
    #     return self.__clickhouse_password
