from queries import GetMessageSources
import jabber

source_handlers = {
    'jabber': jabber.run,
}

def run(connection):
    get_message_sources = GetMessageSources(connection)
    message_sources = get_message_sources()
    for source in message_sources:
        if source.type in source_handlers:
            source_handlers[source.type](source)
        else:
            raise Exception('unknown source type: '+source.type)

if __name__ == '__main__':
    import logging
    logging.basicConfig(level=logging.DEBUG)
    from db import get_connection
    run(get_connection())
