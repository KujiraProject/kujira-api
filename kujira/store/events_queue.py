'''events queue module'''
from store import redis_db

class Redis(redis_db. RedisConnection):
    '''management of tasks in Redis database '''
    def __init__(self):
        '''init'''
        super(Redis, self).__init__()
        self.connection = False
        self.connection_adress = 'localhost'
        self.connection_port = 6379
        self.redis_connection = None

    def connect(self):
        '''connecting'''
        super(Redis, self).connect()

    def push(self, event):
        '''pushes event to redis store into list'''
        self.redis_connection.lpush('event_queue', event)

    def pop(self):
        '''pops oldest event in redis list, inf there is none, waits till any appear'''
        return self.redis_connection.brpop('event_queue')[1].replace("\'", "\"")

    def is_not_empty(self):
        '''checks if there is any event in list'''
        return bool(self.redis_connection.llen('event_queue') > 0)

    def is_connected(self):
        '''checks connections'''
        super(Redis, self).is_connected()
