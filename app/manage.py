from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask.ext.script import Manager

app = Flask(__name__)
manager = Manager(app)
bootstrap = Bootstrap(app)

if __name__ == '__main__':
    manager.run()