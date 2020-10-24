import logging


logging.basicConfig(
    format=u'[%(asctime)s] %(levelname)s %(message)s',
    level=logging.DEBUG
)
logger = logging.getLogger('HEALTHCHECK')

logger.info('HEALTHCHECK')
