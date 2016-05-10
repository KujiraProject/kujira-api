"""module with databases exceptions"""

class ConnectionError(Exception):
    """Error appearing if connection to datebase fails"""
    def __init__(self, message):
        self.message = message
        super(ConnectionError, self).__init__()

class TransactionError(Exception):
    """Error appears if transaction fails """
    def __init__(self, message):
        self.message = message
        super(TransactionError, self).__init__()

class CursorError(Exception):
    """Error appears if something happened with cursor"""
    def  __init__(self, message):
        self.message = message
        super(CursorError, self).__init__()
