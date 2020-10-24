"""
DI container configuration
"""

import logging
from logging import Logger

from injector import singleton, Module, Binder
from kafka.admin import KafkaAdminClient
from kafka import KafkaProducer, KafkaConsumer

from .config import Config


class DI(Module):
    def configure(self, binder: Binder) -> None:
        injector = binder.injector

        binder.bind(
            interface=Config,
            to=Config(),
            scope=singleton
        )
        config = injector.get(Config)

        binder.bind(
            interface=Logger,
            to=self.__logger(config),
            scope=singleton
        )

        binder.bind(
            interface=KafkaAdminClient,
            to=KafkaAdminClient(
                bootstrap_servers=f'{config.kafka_host}:{config.kafka_port}',
                client_id=config.app_name
            ),
            scope=singleton
        )

        binder.bind(
            interface=KafkaProducer,
            to=KafkaProducer(
                client_id=config.app_name,
                bootstrap_servers=[f'{config.kafka_host}:{config.kafka_port}']
            ),
            scope=singleton
        )

        binder.bind(
            interface=KafkaConsumer,
            to=KafkaConsumer(
                config.kafka_oscillograms_topic_name,
                group_id=config.app_name,
                bootstrap_servers=[f'{config.kafka_host}:{config.kafka_port}'],
                enable_auto_commit=True
            ),
            scope=singleton
        )

    @staticmethod
    def __logger(config: Config) -> Logger:
        log_level = logging.getLevelName(config.log_level)
        logging.basicConfig(
            level=log_level if isinstance(log_level, int) else logging.INFO,
            format=u'[%(asctime)s] %(levelname)s %(message)s',
        )
        return logging.getLogger(config.app_name)
