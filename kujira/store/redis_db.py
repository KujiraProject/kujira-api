'''module for abstract redis management'''
from abc import ABCMeta, abstractmethod
import redis

class RedisConnection:
    '''abstract class for redis management'''
    def __init__(self):
        self.connection_adress = None
        self.redis_connection = None
        self.connection_port = None

    __metaclass__ = ABCMeta

    @abstractmethod
    def connect(self):
        '''connecting'''
        self.redis_connection = redis.Redis(self.connection_adress)

    @abstractmethod
    def is_connected(self):
        '''checks connections'''
        try:
            return bool(self.redis_connection.ping())
        except redis.ConnectionError:
            raise Exception('Cannot connect to database!')
