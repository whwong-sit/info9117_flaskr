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

    @property
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
        # print "setter of password called"
        self._password = generate_password_hash(plaintext)

    #### check password
    def check_password(self, plaintext):
        """
        Check that a plaintext password is equal to the hashed password.

        At this stage, this method is not being used except in testing.
        :param plaintext: plaintext password to check
        :return: Boolean value; if true, then the plaintext and hash correspond, else false.
        """
        return check_password_hash(self.password, plaintext)
