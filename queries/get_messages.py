from collections import namedtuple

Message = namedtuple('Message', 
        'type service group sender priority body format')

class GetMessages:
    def __init__(self, connection):
        self._connection = connection

    def __call__(self):
        cursor = self._connection.cursor()
        cursor.execute('''
        select type
             , service
             , "group"
             , sender
             , priority
             , body
             , format
             from messages
        ''')
        result = []
        for row in cursor.fetchall():
            result.append(Message(*row))
        return result
