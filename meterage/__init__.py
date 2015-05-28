__all__ = ['app', 'User', 'db', 'Entry', 'session', 'Comment', 'time']

from flask import Flask, session
from os.path import isfile, abspath, dirname, join
from flask_sqlalchemy import SQLAlchemy
import config
import time

basedir = abspath(dirname(__file__))

# create application
app = Flask("Meterage",
            instance_relative_config=True,
            template_folder=join(basedir, "templates"),
            static_folder=join(basedir, "static"))
app.config.from_object(config)
app.config.from_pyfile('config.py')
app.config.from_envvar('FLASKR_SETTINGS', silent=True)
db = SQLAlchemy(app)

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
