'''module for abstract redis management'''
import redis


class RedisConnection(object):
    """base class for redis management"""
    def __init__(self, connection_adress, connection_port):
        self.connection_adress = connection_adress
        self.connection = None
        self.connection_port = connection_port

    def connect(self):
        """sets connection details"""
        self.connection = redis.Redis(self.connection_adress)

    def is_connected(self):
        """checks connections state
        :returns: true if connected
        """
        try:
            return bool(self.connection.ping())
        except redis.ConnectionError:
            return False
