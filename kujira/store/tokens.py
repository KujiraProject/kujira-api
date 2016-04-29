'''library to acces Mongo database allowing to insert and get tokens.'''
from store import redis_db

class Redis(redis_db.RedisConnection):
    '''token management class '''
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

    def push(self, user_name, random_value):
        '''pushes user token as pair user_name, some random_value'''
        self.redis_connection.lpush('token_queue',
                                    [user_name, str(random_value)])

    def pop(self):
        '''gets oldest token'''
        return self.redis_connection.rpop('token_queue')

    def get_token(self, user_name):
        '''gets specified by user name token'''
        test_dl = self.redis_connection.llen('token_queue')
        for char in range(0, test_dl):
            token_string = self.redis_connection.lindex('token_queue', char)
            if token_string.split("'")[1] == user_name:
                return token_string.split("'")[3]


    def is_connected(self):
        '''checks connections'''
        super(Redis, self).is_connected()

