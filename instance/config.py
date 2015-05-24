from meterage import basedir
import os.path

SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "db", "") + "meterage.db"
SQLALCHEMY_ECHO = True

# this needs to be set for sessions to be enabled.
# See http://flask.pocoo.org/docs/0.10/quickstart/#sessions
# Also it is best set in instance/config.py as it should be private
SECRET_KEY = 'development key'