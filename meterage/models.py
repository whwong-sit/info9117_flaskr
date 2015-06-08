from flask_bcrypt import generate_password_hash, check_password_hash
from . import db
from sqlalchemy.ext.hybrid import hybrid_property
import time
from datetime import datetime


class User(db.Model):
    """
    Defines a user with associated username, password and Gravatar email address.

    You simply need to make an assignment to a User object's "password" field like so:

        user.password = "newpassword"

    and the setter function is automatically called.
    """

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    username = db.Column(db.String(64), index=True, unique=True)
    __password = db.Column(db.String(128))
    gravataremail = db.Column(db.String(120), index=True, unique=True)
    admin = db.Column(db.Boolean)
    approved = db.Column(db.Boolean)

    def __repr__(self):
        if self.admin:
            return '<Admin {0}>'.format(self.username)
        else:
            return '<User {0}>'.format(self.username)

    def __init__(self, username, password, gravataremail, admin=False, approved=False):
        self.username = username
        self.password = password
        self.gravataremail = gravataremail
        self.admin = admin
        self.approved = approved


    @hybrid_property
    def password(self):
        """
        Getter method for password.

        :return: The User object's hashed password
        """
        return self.__password

    @password.setter
    def password(self, plaintext):
        """
        Sets the user's password, converting the plain text argument to a hashed password.

        :param plaintext: the plain text being entered by the user, to be hased
        "
        """
        self.__password = generate_password_hash(plaintext)

    def check_password(self, plaintext):
        """
        Check that a plaintext password is equal to the hashed password.

        At this stage, this method is not being used except in testing.
        :param plaintext: plaintext password to check
        :return: Boolean value; if true, then the plaintext and hash correspond, else false.
        """
        return check_password_hash(self.password, plaintext)

class Entry(db.Model):

    __tablename__ = "entries"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    author = db.relationship('User', backref='entries', lazy='joined')

    title = db.Column(db.String(128))
    text = db.Column(db.Text)
    start_time = db.Column(db.String(16))
    end_time = db.Column(db.String(16))
    task_des = db.Column(db.String)
    user_role = db.Column(db.PickleType)
    # TODO use DateTime types for the start_time and end_time
    # start_time = db.Column(db.DateTime)
    # end_time = db.Column(db.DateTime)

    def __repr__(self):
        return "<Entry {0}>".format(self.title)

    def __init__(self, title, text, uid, start_time=None, end_time=None, task_des=None, user_role=[]):
        self.title = title
        self.text = text
        self.user_id = uid
        # TODO do some parsing of the incoming time data
        if start_time is None or start_time is "":
            self.start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        else:
            self.start_time = start_time
        self.end_time = end_time
        self.task_des = task_des
        self.user_role = user_role

class Comment(db.Model):

    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    entry_id = db.Column(db.Integer, db.ForeignKey('entries.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    entry = db.relationship('Entry', backref='comments', lazy='joined')
    author = db.relationship('User', backref='comments', lazy='joined')

    text = db.Column(db.Text)
    posttime = db.Column(db.DateTime)

    def __repr__(self):
        return '<Comment by {0}>'.format(self.author)

    def __init__(self, user_id, text, entry_id):
        self.user_id = user_id
        self.text = text
        self.entry_id = entry_id
        self.posttime = datetime.now()
