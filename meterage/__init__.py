__all__ = ['app', 'connect_db', 'init_db', 'User', 'avatar']

from flask import Flask
from sqlite3 import dbapi2 as sqlite3
from contextlib import closing
from os.path import isfile, abspath, dirname
import urllib
import hashlib

import config

# create application
app = Flask("Meterage",
            instance_relative_config=True,
            template_folder=abspath(dirname(__file__))+ "/templates",
            static_folder=abspath(dirname(__file__))+ "/static")
app.config.from_object(config)
app.config.from_pyfile('config.py')
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

# useful functions
def connect_db():
    """
    Make a connection to the database

    database specified in the config.
    """
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
    """
    For initialising the database using schemal.sql.

    This is usually called manually.
    """
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

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

# imports
from models import User
import views

# generate database
if not isfile(str(app.config['DATABASE'])):
    app.logger.debug('creating database')
    init_db()

    usernames = ["admin", "hari", "jim", "spock"]
    passwords = ["default", "seldon", "bean", "vulcan"]
    gravataremails = ['daisy22229999@gmail.com', 'daisy200029@gmail.com', "jimbean@whisky.biz", "livelong@prosper.edu.au"]

    with closing(connect_db()) as db:
        for username, password, gravataremail in zip(usernames, passwords, gravataremails):
            user = User(username, password, gravataremail)
            app.logger.debug("Adding {0} to the database.".format(user))
            db.execute('insert into userPassword (username, password, gravataremail) values (?, ?, ?)',
                       [user.username, user.password, user.gravataremail])
        db.commit()
