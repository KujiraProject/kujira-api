"""This module is responsible for handling specific events from salt event bus
"""

# Import python libs
import json
import logging
import re

# Import salt lib
import salt.utils.event
import salt.config

from redis_lib import Redis

logger = logging.getLogger('kujira parser')

opts = salt.config.client_config('/etc/salt/master')
event_bus = None
redis_handler = None


def get_connected_redis_handler():
    """Create redis handler and try to connect it to redis server

    :return: Instance of Redis ready to use
    """
    redis = Redis()
    redis.connect()
    return redis


def get_event_bus():
    """Initialize and return SaltEvent object for master.

    :return: SaltEvent object used for accessing event system
    """
    return salt.utils.event.get_event(
        'master',
        sock_dir=opts['sock_dir'],
        transport=opts['transport'],
        opts=opts)


def put_event_data_in_redis_queue(event_data):
    """Push data about events into redis queue

    :param event_data: event data to push
    """
    redis_handler.push_event_to_queue(event_data)
    logger.debug('Pushed event to event_queue. Event: ' + event_data)


def calamari_event_handler(event):
    """Handle salt event from calamari

    :param event: event to handle
    """
    logger.debug('calamari_event_handler - event: ' + json.dumps(event))


def kujira_event_handler(event):
    """Handle event from Kujira

    :param event: event to handle
    """
    logger.debug('kujira_event_handler - event: ' + json.dumps(event))

    redis_event_tags = ('kujira/osd/fail',
                        'kujira/osd/add')

    if any(tag in event['tag'] for tag in redis_event_tags):
        json_event = json.dumps(event)
        put_event_data_in_redis_queue(json_event)


def configure_logger():
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler = logging.FileHandler('/var/log/kujira/event_parser.log')
    handler.setFormatter(formatter)
    logger.addHandler(handler)


def main():
    """Listen to events and handle them
    """
    configure_logger()
    logger.info("Kujira parser started")

    global event_bus
    event_bus = get_event_bus()

    global redis_handler
    redis_handler = get_connected_redis_handler()

    calamari_event_pattern = re.compile('^ceph*')
    kujira_event_pattern = re.compile('^kujira*')

    while True:
        event = event_bus.get_event(full=True)
        if event and 'tag' in event:
            if calamari_event_pattern.match(event['tag']) is not None:
                calamari_event_handler(event)
            elif kujira_event_pattern.match(event['tag']) is not None:
                kujira_event_handler(event)

if __name__ == "__main__":
    main()
