from .message_source import MessageSource

class GetMessageSources:
    def __init__(self, connection):
        self._connection = connection

    def __call__(self):
        cursor = self._connection.cursor()
        cursor.execute('''
        select id
             , type
             , service
             , config
        from message_sources
        ''')
        result = []
        for row in cursor.fetchall():
            source = MessageSource(*row)
            result.append(source)
        return result
