from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask.ext.script import Manager

app = Flask(__name__)
manager = Manager(app)
bootstrap = Bootstrap(app)
@app.route('/')
def index():
    return render_template('home.html')

@app.route('/share')
def share():
    return render_template('share.html')

if __name__ == '__main__':
    manager.run()