from gevent.socket import wait_read

def wait_for_notify(connection, queue, notify_name):
    while True:
        connection.cursor().execute('''
            listen {};
        '''.format(notify_name));
        connection.commit()
        #print('waiting for {}...'.format(notify_name))
        wait_read(connection.fileno())
        #print('got response...')
        connection.poll()
        while connection.notifies:
            #print('notify get')
            queue.put(connection.notifies.pop())
