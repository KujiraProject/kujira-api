"""This module is responsible for handling specific events from salt event bus"""

# Import python libs
import sys
import json
import logging
import re

# Import salt lib
import salt.utils.event
import salt.config

from kujira.store.events_queue import RedisQueue
from kujira.store.exceptions import ConnectionError

logger = logging.getLogger('kujira parser')

opts = salt.config.client_config('/etc/salt/master')

redis_event_cache = []


def get_connected_redis_handler():
    """
    Create redis handler and try to connect it to redis server

    :return: Instance of RedisQueue ready to use
    """
    redis = RedisQueue()
    redis.connect()
    if not redis.is_connected():
        logger.critical('Cannot connect to Redis. Exiting...')
        sys.exit(1)
    return redis


def get_event_bus():
    """
    Initialize and return SaltEvent object for master.

    :return: SaltEvent object used for accessing event system
    """
    return salt.utils.event.get_event(
        'master',
        sock_dir=opts['sock_dir'],
        transport=opts['transport'],
        opts=opts)


def put_event_data_in_redis_queue(event_data, redis_handler):
    """
    Push data about events into redis queue

    :param event_data: event data to push
    :param redis_handler: RedisQueue object
    """
    try:
        if redis_event_cache:
            put_all_cached_events_to_redis_queue(redis_handler)
        redis_handler.push(event_data)
        logger.debug('Pushed event to event_queue')
    except ConnectionError:
        logger.warning('No connection to Redis. Caching event data')
        cache_event(event_data)
        redis_handler.connect()


def cache_event(event_data):
    redis_event_cache.append(event_data)


def put_all_cached_events_to_redis_queue(redis_handler):
    """
    Put all cached events to redis queue

    :param redis_handler: RedisQueue object
    """
    try:
        while redis_event_cache:
            put_cached_event_data_in_redis_queue(redis_event_cache[0], redis_handler)
            redis_event_cache.pop(0)
    except ConnectionError:
        logger.warning('No connection to Redis while putting cached events to queue')
        redis_handler.connect()


def put_cached_event_data_in_redis_queue(event_data, redis_handler):
    """
    Put event data in redis queue. No exceptions are handled

    :param event_data: event data in json format
    :param redis_handler: RedisQueue object
    """
    redis_handler.push(event_data)
    logger.debug('Pushed cached event to event_queue. Event: ' + event_data)


def calamari_event_handler(event, _): # redis_handler
    """
    Handle salt event from calamari

    :param event: event to handle
    """
    logger.debug('calamari_event_handler - event: ' + json.dumps(event))


def kujira_event_handler(event, redis_handler):
    """
    Handle event from Kujira

    :param event: event to handle
    :param redis_handler: RedisQueue object
    """
    logger.debug('kujira_event_handler - event: ' + json.dumps(event))

    redis_event_tags = ('kujira/osd/fail',
                        'kujira/osd/add')

    if any(tag in event['tag'] for tag in redis_event_tags):
        json_event = json.dumps(event)
        put_event_data_in_redis_queue(json_event, redis_handler)


def salt_auth_event_handler(event, redis_handler):
    """
    Detect salt/auth event with variable act set to pend and push it to redis queue
    :param event: salt event with salt/auth tag
    :param redis_handler: RedisQueue object
    """
    logger.debug('salt_auth_event_handler - event: ' + json.dumps(event))

    if 'data' in event and 'act' in event['data'] and event['data']['act'] == 'pend':
        json_event = json.dumps(event)
        put_event_data_in_redis_queue(json_event, redis_handler)


def configure_logger():
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler = logging.FileHandler('/var/log/kujira/event_parser.log')
    handler.setFormatter(formatter)
    logger.addHandler(handler)


def main():
    """Listen to events and handle them"""
    configure_logger()
    logger.info("Kujira parser started")

    event_bus = get_event_bus()

    redis_handler = get_connected_redis_handler()

    calamari_event_pattern = re.compile('^ceph*')
    kujira_event_pattern = re.compile('^kujira*')
    salt_auth_event_pattern = re.compile('^salt/auth*')

    while True:
        event = event_bus.get_event(full=True)

        if event and 'tag' in event:
            if calamari_event_pattern.match(event['tag']) is not None:
                calamari_event_handler(event, redis_handler)
            elif kujira_event_pattern.match(event['tag']) is not None:
                kujira_event_handler(event, redis_handler)
            elif salt_auth_event_pattern.match(event['tag']) is not None:
                salt_auth_event_handler(event, redis_handler)


if __name__ == "__main__":
    main()
