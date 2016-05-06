'''library to acces Mongo database allowing to insert and get tokens.'''
from . import redis_db

class RedisTokens(redis_db.RedisConnection):
    '''token management class '''
    def __init__(self):
        '''init'''
        super(RedisTokens, self).__init__()
        self.connection_adress = 'localhost'
        self.connection_port = 6379
        self.redis_connection = None

    def connect(self):
        '''connecting'''
        super(RedisTokens, self).connect()

    def push(self, user_name, random_value):
        '''pushes user token as pair user_name, some random_value'''
        try:
            self.redis_connection.lpush('token_queue',
                                        [user_name, str(random_value)])
        except redis_db.redis.ConnectionError:
            raise Exception('Cannot connect to database!')

    def pop(self):
        '''gets oldest token'''
        try:
            return self.redis_connection.rpop('token_queue')
        except redis_db.redis.ConnectionError:
            raise Exception('Cannot connect to database!')

    def get_token(self, user_name):
        '''gets specified by user name token'''
        try:
            test_dl = self.redis_connection.llen('token_queue')
            for char in range(0, test_dl):
                token_string = self.redis_connection.lindex('token_queue', char)
                if token_string.split("'")[1] == user_name:
                    return token_string.split("'")[3]
        except redis_db.redis.ConnectionError:
            raise Exception('Cannot connect to database!')


    def is_connected(self):
        '''checks connections'''
        super(RedisTokens, self).is_connected()

