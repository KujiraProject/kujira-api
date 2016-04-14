import redis

class RedisHandler():
    def __init__(self):
        self.connection = False
        self.connectionAdress = 'localhost'
        self.connectionPort = 6379
        self.redisConnection = None

    def connect(self):
        try:
            self.redisConnection = redis.Redis(self.connectionAdress)
            return True
        except redis.ConnectionError:
            return False

    def pushEventToQueue(self, event):
        self.redisConnection.lpush('eventQueue',event)

    def popEventFromQueue(self):
        return self.redisConnection.rpop('eventQueue')

    def isConnected(self):
        if self.redisConnection.ping() == True:
            return True
        else:
            return False

    def pushToken(self, userName, randomValue):
        self.redisConnection.lpush('tokenQueue', [userName,str(randomValue)])

    def popToken(self):
        return self.redisConnection.rpop('tokenQueue')

    def getToken(self, userName):
        testDl = self.redisConnection.llen('tokenQueue')
        for x in range(0,testDl):
            zmiennnna = self.redisConnection.lindex('tokenQueue', x)
            if zmiennnna.split("'")[1]==userName:
                return  zmiennnna.split("'")[3]
                break

  #  def disconnect(self):
   #     self.redisConnection = None
