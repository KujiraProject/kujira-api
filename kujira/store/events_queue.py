"""events queue module"""
from . import redis_db
from . import exceptions


class RedisQueue(redis_db.RedisConnection):
    """management of tasks in Redis database"""

    def __init__(self):
        super(RedisQueue, self).__init__('localhost', 6379)

    def push(self, event):
        """pushes event to redis as list
        :param event: list of atributes
        """
        try:
            self.connection.lpush('event_queue', event)
        except redis_db.redis.ConnectionError:
            raise exceptions.ConnectionError(
                'Cannot connect to database!')

    def pop(self):
        """pops oldest event in redis list,
        :returns: single event
        """
        try:
            return self.connection.brpop('event_queue')[1].replace("\'", "\"")
        except redis_db.redis.ConnectionError:
            raise exceptions.ConnectionError(
                'Cannot connect to database!')

    def is_not_empty(self):
        """checks if there is any event in queue
        :returns: true if collection is not empty
        """
        try:
            return bool(self.connection.llen('event_queue') > 0)
        except redis_db.redis.ConnectionError:
            raise exceptions.ConnectionError(
                'Cannot connect to database!')
