from flask import Flask, render_template, g, request
import logging

import config
import queries
from queries import Message, MessageSource
import db

log = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = config.SECRET_KEY

# set up jade
app.jinja_env.add_extension('pyjade.ext.jinja.PyJadeExtension')

class Deps: pass
deps = Deps()
deps.GetMessages = queries.GetMessages
deps.AddMessages = queries.AddMessages
deps.get_connection = db.get_connection

@app.route('/')
def show_index():
    log.info('index')
    get_messages = deps.GetMessages(deps.get_connection())
    messages = get_messages()
    return render_template('index.jade', messages=messages)

def create_message_instance(json):
    fields = dict.fromkeys(Message._fields)
    fields.update(json)
    fields['source'] = MessageSource(int(fields['source']), None,None,None)
    return Message(**fields)

@app.route('/messages', methods=['POST'])
def add_message():
    add_messages = deps.AddMessages(deps.get_connection())
    json = request.get_json(force=True)
    message = create_message_instance(json)
    result = add_messages([message])
    return 'added', 201, {'location': '{}/messages/{}'.format(request.base_url,
                            result[0])}

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    host, port = config.BASE_URL.split(':')
    app.run(host=host, port=int(port))
