import os
from logging import Logger

from injector import Injector
# from clickhouse_driver import Client
from kafka import KafkaConsumer
from minio import Minio
from minio.error import ResponseError, BucketAlreadyOwnedByYou, BucketAlreadyExists

from consumer.di import DI
from consumer.config import Config


di = Injector(modules=[DI()])

logger = di.get(Logger)
config = di.get(Config)
kafka_consumer = di.get(KafkaConsumer)
# clickhouse_client = di.get(Client)
minio_client = di.get(Minio)

minio_bucket_name = config.minio_bucket_name
try:
    minio_client.make_bucket(minio_bucket_name)
except BucketAlreadyOwnedByYou as err:
    logger.info(f'\'{minio_bucket_name}\' minio bucket already owned')
except BucketAlreadyExists as err:
    logger.info(f'minio bucket \'{minio_bucket_name}\' already exists, creation passed')
except ResponseError as e:
    logger.error(f'error on \'{minio_bucket_name}\' minio bucket creation')
    raise e

oscillograms_dir = config.oscillograms_tmp_store_dir
oscillograms_full_dir = os.path.join(os.getcwd(), oscillograms_dir)
for message in kafka_consumer:
    logger.debug(f"{message.topic}:{message.partition}:{message.offset}: key={message.key} value={message.value}")

    oscillogram_file_name = str(message.key, encoding='utf8')
    oscillogram_file_value = message.value
    oscillograms_full_file_name = os.path.join(os.getcwd(), oscillograms_dir, oscillogram_file_name)
    with open(oscillograms_full_file_name, 'wb') as binary_oscillogram_file:
        binary_oscillogram_file.write(oscillogram_file_value)

    try:
        minio_client.fput_object(minio_bucket_name, oscillogram_file_name, oscillograms_full_file_name)
    except ResponseError as e:
        # на ошибку можно не реагировать, так как файл отанется во временном хранилище.
        # можно будет сделать отдельный механизм, который по расписанию проверяет наличие файлов
        # во временном хранилище и сохраняет в minio.
        # это проще и даже надежнее обработчика с попытками перезаписи прямо во время ошибки
        logger.error(f'cannot save file to minio bucket \'{minio_bucket_name}\'')
    else:
        os.remove(oscillograms_full_file_name)
        logger.info(f'oscillogram \'{oscillogram_file_name}\' saved into minio bucket \'{minio_bucket_name}\'')
