# These are just for prototyping purposes
from contextlib import closing
import tempfile
import os
from sqlite3 import dbapi2 as sqlite3

from flask_bcrypt import generate_password_hash, check_password_hash


class User(object):
    """
    Defines a user with associated username and password.

    I am treating _username and _password as private fields of the class, but this is purely an
    implementation detail.  You simply need to make an assignment to a User object's "password"
    field like so:

    user.password = "newpassword"

    and the setter function is automatically called.
    """

    def __init__(self, username, password):
        self.username = username
        self.password = password

    #### username

    @property
    def username(self):
        """

        :return: The
        """
        return self._username

    @username.setter
    def username(self, newname):
        """
        Set the username.  This is as simple as it looks, simply making an assignment to
        the _username field so it can be returned in the getter.
        """
        self._username = newname

    #### password

    @property
    def password(self):
        """
        Getter function for password.
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
        # print "setter of password called"
        self._password = generate_password_hash(plaintext)

if __name__ == '__main__':

    # initialise temporary database
    db_fd, DATABASE = tempfile.mkstemp()
    with closing(sqlite3.connect(DATABASE)) as db:
        with file('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

    # define some User objects
    users = [User("admin", "default"), User("hari", "seldon")]

    # add users to temporary database
    with closing(sqlite3.connect(DATABASE)) as db:
        for user in users:
            print("Adding user {0} to the database".format(user.username))
            db.execute('insert into userPassword (username, password) values (?, ?)',
                       [user.username, user.password])
        db.commit()

    # close resources
    os.close(db_fd)
    os.unlink(DATABASE)