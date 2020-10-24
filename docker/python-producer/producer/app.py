import os

from logging import Logger

from injector import Injector
from kafka.admin import KafkaAdminClient, NewTopic
from kafka import KafkaProducer
from kafka.errors import TopicAlreadyExistsError, KafkaTimeoutError

from producer.di import DI
from producer.config import Config


di = Injector(modules=[DI()])

PRODUCED_FILES_MARK = '__'

logger = di.get(Logger)
config = di.get(Config)
kafka_admin_client = di.get(KafkaAdminClient)
kafka_producer = di.get(KafkaProducer)

topic_name = config.kafka_oscillograms_topic_name
try:
    topic_list = [NewTopic(name=topic_name, num_partitions=1, replication_factor=1)]
    kafka_admin_client.create_topics(new_topics=topic_list, validate_only=False)
except TopicAlreadyExistsError as e:
    logger.info(f'kafka topic \'{topic_name}\' already exists, creation passed')

oscillograms_dir = config.oscillograms_store_dir
oscillograms_full_dir = os.path.join(os.getcwd(), oscillograms_dir)

while True:
    for oscillogram_file_name in os.listdir(oscillograms_full_dir):
        if oscillogram_file_name[-2:] == PRODUCED_FILES_MARK:
            # already produced
            continue

        oscillograms_full_file_name = os.path.join(os.getcwd(), oscillograms_dir, oscillogram_file_name)
        with open(oscillograms_full_file_name, 'rb') as binary_oscillogram_file:
            try:
                kafka_producer.send(
                    topic_name,
                    key=bytes(oscillogram_file_name, encoding='utf8'),
                    value=binary_oscillogram_file.read()
                )
                kafka_producer.flush()
            except KafkaTimeoutError as e:
                # на ошибку можно не реагировать,
                # так как файл не будет переименован и попытка перезаписи будет при повторной итерации
                logger.error(f'cannot write into kafka topic \'{topic_name}\'')
            else:
                os.rename(
                    oscillograms_full_file_name,
                    oscillograms_full_file_name + PRODUCED_FILES_MARK,
                )
                logger.info(f'oscillogram \'{oscillogram_file_name}\' successfully produced')
