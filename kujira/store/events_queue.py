'''events queue module'''
from . import redis_db


class RedisQueue(redis_db. RedisConnection):
    '''management of tasks in Redis database '''
    def __init__(self):
        '''init'''
        super(RedisQueue, self).__init__()
        self.connection_adress = 'localhost'
        self.connection_port = 6379
        self.redis_connection = None

    def connect(self):
        '''connecting'''
        super(RedisQueue, self).connect()

    def push(self, event):
        '''pushes event to redis store into list'''
        try:
            self.redis_connection.lpush('event_queue', event)
        except redis_db.redis.ConnectionError:
            raise Exception('Cannot connect to database!')

    def pop(self):
        '''pops oldest event in redis list, inf there is none, waits till any appear'''
        try:
            return self.redis_connection.brpop('event_queue')[1].replace("\'", "\"")
        except redis_db.redis.ConnectionError:
            raise Exception('Cannot connect to database!')

    def is_not_empty(self):
        '''checks if there is any event in list'''
        try:
            return bool(self.redis_connection.llen('event_queue') > 0)
        except redis_db.redis.ConnectionError:
            raise Exception('Cannot connect to database!')

    def is_connected(self):
        '''checks connections'''
        return super(RedisQueue, self).is_connected()

