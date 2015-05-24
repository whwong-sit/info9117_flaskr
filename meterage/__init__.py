__all__ = ['app', 'connect_db', 'User', 'avatar', 'db', 'Entry', 'session', 'Comment']

from flask import Flask, session
from os.path import isfile, abspath, dirname, join
import urllib
import hashlib
from flask_sqlalchemy import SQLAlchemy
import config

basedir = abspath(dirname(__file__))

# create application
app = Flask("Meterage",
            instance_relative_config=True,
            template_folder=join(basedir, "templates"),
            static_folder=join(basedir, "static"))
app.config.from_object(config)
app.config.from_pyfile('config.py')
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

# database object, for database interaction
db = SQLAlchemy(app)

# useful functions
def connect_db():
    """
    Make a connection to the database.

    """
    # TODO redo this
    # return sqlite3.connect(app.config['DATABASE'])

def avatar(email, size=50):
    """
    generate gravatar url from email

    :param email: email address for gravatar
    :param size: size of the image, deafaults to 50
    :return: url of gravatar
    """
    gravatar_url = "http://www.gravatar.com/avatar/" + hashlib.md5(email.lower()).hexdigest()+"?"
    gravatar_url += urllib.urlencode({'d':"monsterid",'s':str(size)})
    return gravatar_url

# imports; these seem to have to be *here*
from models import User, Entry, Comment
import views

# generate database
if not isfile(str(app.config['DATABASE'])):
    app.logger.debug('creating database')
    db.create_all()

    usernames = ["admin", "hari", "jim", "spock"]
    passwords = ["default", "seldon", "bean", "vulcan"]
    gravataremails = ['daisy22229999@gmail.com', 'daisy200029@gmail.com', "jimbean@whisky.biz", "livelong@prosper.edu.au"]

    for username, password, gravataremail in zip(usernames, passwords, gravataremails):
        if username == 'admin':
            user = User(username, password, gravataremail, True)
        else:
            user = User(username, password, gravataremail)
        app.logger.debug("Adding {0} to the database.".format(user))
        db.session.add(user)
    db.session.commit()
