from .message import Message
from .message_source import MessageSource

class GetMessages:
    def __init__(self, connection):
        self._connection = connection

    def __call__(self):
        cursor = self._connection.cursor()
        cursor.execute('''
        select messages.id as message_id
             , source_id
             , type
             , service
             , "group"
             , sender
             , priority
             , body
             , format
             from messages
             inner join message_sources on (messages.source_id = message_sources.id)
        ''')
        result = []
        for row in cursor.fetchall():
            # TODO: cache MessageSource objects?
            source = MessageSource(row[1], row[2], row[3], None)
            message = Message(source, row[0], row[4], row[5], row[6], row[7], row[8])
            result.append(message)
        return result
