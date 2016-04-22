'''module docString'''

import redis

class Redis(object):
    '''class '''
    def __init__(self):
        '''init'''
        self.connection = False
        self.connection_adress = 'localhost'
        self.connection_port = 6379
        self.redis_connection = None

    def connect(self):
        '''connecting'''
        self.redis_connection = redis.Redis(self.connection_adress)
    def push_event_to_queue(self, event):
        '''pushes event to redis database into list'''
        self.redis_connection.lpush('event_queue', event)

    def pop_event_from_queue(self):
        '''pops oldest event in redis list, inf there is none, waits till any appear'''
        return self.redis_connection.brpop('event_queue').replace("\'", "\"")

    def is_any_event_in_queue(self):
        '''checks if there is any event in list'''
        return bool(self.redis_connection.llen('event_queue') > 0)

    def is_connected(self):
        '''checks connections'''
        return bool(self.redis_connection.ping())

    def push_token(self, user_name, random_value):
        '''pushes user token as pair user_name, some random_value'''
        self.redis_connection.lpush('token_queue', [user_name, str(random_value)])

    def pop_token(self):
        '''gets oldest token'''
        return self.redis_connection.rpop('token_queue')

    def get_token(self, user_name):
        '''gets specified by user name token'''
        test_dl = self.redis_connection.llen('token_queue')
        for char in range(0, test_dl):
            token_string = self.redis_connection.lindex('token_queue', char)
            if token_string.split("'")[1] == user_name:
                return  token_string.split("'")[3]
