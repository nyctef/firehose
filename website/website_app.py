from flask import Flask, render_template
import config

app = Flask(__name__)
app.config['SECRET_KEY'] = config.SECRET_KEY

# set up jade
app.jinja_env.add_extension('pyjade.ext.jinja.PyJadeExtension')

@app.route('/')
def show_index():
    return render_template('index.jade')

if __name__ == '__main__':
    app.run()
