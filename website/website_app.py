from flask import Flask, render_template, g
import config

from queries import GetMessages
from db import get_connection

app = Flask(__name__)
app.config['SECRET_KEY'] = config.SECRET_KEY

# set up jade
app.jinja_env.add_extension('pyjade.ext.jinja.PyJadeExtension')

class Deps: pass
deps = Deps()
deps.GetMessages = GetMessages
deps.get_connection = get_connection

@app.route('/')
def show_index():
    messages = deps.GetMessages(deps.get_connection())
    return render_template('index.jade', messages=messages())

if __name__ == '__main__':
    app.run()
