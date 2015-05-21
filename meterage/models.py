from flask_bcrypt import generate_password_hash, check_password_hash
from . import db
from sqlalchemy.ext.hybrid import hybrid_property
from datetime import datetime


class User(db.Model):
    """
    Defines a user with associated username, password and Gravatar email address.

    I am treating _username, _password and _gravataremail as private fields of the class, but this is purely an
    implementation detail.  You simply need to make an assignment to a User object's "password"
    field like so:

    user.password = "newpassword"

    and the setter function is automatically called.
    """

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    _username = db.Column(db.String(64), index=True, unique=True)
    _password = db.Column(db.String(128))
    _gravataremail = db.Column(db.String(120), index=True, unique=True)

    def __repr__(self):
        return '<User {0}>'.format(self.username)

    def __init__(self, username, password, gravataremail):
        self.username = username
        self.password = password
        self.gravataremail = gravataremail

    #### username

    @hybrid_property
    def username(self):
        """
        :return: The username
        """
        return self._username

    @username.setter
    def username(self, newname):
        """
        Set the username.

        This is as simple as it looks, simply making an assignment to
        the _username field so it can be returned in the getter.
        """
        self._username = newname

    #### password

    @hybrid_property
    def password(self):
        """
        Getter method for password.

        :return: The User object's hashed password
        """
        return self._password

    @password.setter
    def password(self, plaintext):
        """
        Sets the user's password, converting the plain text argument to a hashed password.

        :param plaintext: the plain text being entered by the user, to be hased
        "
        """
        self._password = generate_password_hash(plaintext)

    #### Gravatar email address

    @hybrid_property
    def gravataremail(self):
        """
        :return: The Gravatar email address
        """
        return self._gravataremail

    @gravataremail.setter
    def gravataremail(self, newemail):
        """
        Set the Gravatar email

        This is as simple as it looks, simply making an assignment to
        the _gravataremail field so it can be returned in the getter.
        """
        self._gravataremail = newemail

    #### check password

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
    title = db.Column(db.String(128))
    text = db.Column(db.Text)
    username = db.Column(db.String(64), db.ForeignKey("users._username"))
    # start_time = db.Column(db.DateTime)
    # end_time = db.Column(db.DateTime)
    start_time = db.Column(db.String(16))
    end_time = db.Column(db.String(16))
    # gravataremail = db.Column(db.String(120), db.ForeignKey("_gravataremail"))

    def __repr__(self):
        return "<Entry {0}>".format(self.title)

    def __init__(self, title, text, start_time=None, end_time=None):
        self.title = title
        self.text = text
        # TODO do some parsing of the incoming time data
        if start_time is None or start_time is "":
            self.start_time = datetime.now()
        else:
            self.start_time = start_time
        self.end_time = end_time
