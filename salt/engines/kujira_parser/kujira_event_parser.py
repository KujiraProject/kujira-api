# -*- coding: utf-8 -*-
"""Salt engine responsible for catching all events from calamari and putting them in Redis.
Salt engines are a new feature in 2015.8.0

Example master configuration:\n
extension_modules: srv/salt\n
engines_dir: srv/salt/engines/kujira_parser\n
engines:
    \- kujira_event_parser
"""

# Import python libs
from __future__ import absolute_import
import sys
import json
import logging

# Import salt lib
import salt.utils.event

# import local module
from .redisDbLib import RedisHandler

log = logging.getLogger(__name__)


def get_connected_redis_handler():
    """Create redis handler and try to connect it to redis server

    :return: Instance of RedisHandler ready to use
    """
    redis_handler = RedisHandler()
    if not redis_handler.connect():
        log.error("Unable to connect to redis")
        sys.exit()
    return redis_handler


def get_event_bus():
    """Initialize and return SaltEvent object for master.

    :return: SaltEvent object used for accessing event system
    """
    event_bus = salt.utils.event.get_master_event(
            __opts__,
            __opts__['sock_dir'],
            listen=True)

    return event_bus


def put_event_data_in_redis_queue(event_data, redis_handler):
    """Push data about events into redis queue

    :param event_data: event data to push
    :param redis_handler: RedisHandler used to push event data
    """
    redis_handler.pushEventToQueue(event_data)
    log.debug('Pushed event to event_queue. Event: ' + event_data)


def start():
    """Listen to calamari events and put them into redis queue
    in form of json strings
    """
    log.info("Engine started")

    event_bus = get_event_bus()
    redis_handler = get_connected_redis_handler()

    while True:
        event = event_bus.get_event(tag='ceph')
        if event:
            json_event = json.dumps(event)
            put_event_data_in_redis_queue(json_event, redis_handler)