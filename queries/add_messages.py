class AddMessages:
    def __init__(self, connection):
        self._connection = connection

    def __call__(self, messages):
        cursor = self._connection.cursor()
        result = []
        for message in messages:
            cursor.execute('''
            select add_message(%s, %s, %s, %s, %s, %s, %s)
            ''', message)
            result.append(cursor.fetchone()[0])
        return result