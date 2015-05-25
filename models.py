from flask_bcrypt import generate_password_hash, check_password_hash


class User(object):
    """
    Defines a user with associated username, password, Gravatar email address, admin privileges, and approval from admin for log in.

    I am treating _username, _password, _gravataremail, _flag_admin, and _flag_approval as private fiel, _flag_admin, and _flag_approvalds of the class, but this is purely an
    implementation detail.  You simply need to make an assignment to a User object's "password"
    field like so:

    user.password = "newpassword"

    and the setter function is automatically called.
    """

    def __init__(self, username, password, gravataremail, flag_admin, flag_approval):
        self.username = username
        self.password = password
        self.gravataremail = gravataremail
        self.flag_admin = flag_admin
        self.flag_approval = flag_approval

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
        self._password = generate_password_hash(plaintext)

    #### Gravatar email address

    @property
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

    #### identifier for admin privileges

    @property
    def flag_admin(self):
        """
        :return: The identifier for admin privileges
        """
        return self._flag_admin

    @flag_admin.setter
    def flag_admin(self, newflag_admin):
        """
        Set the identifier for admin privileges

        This is as simple as it looks, simply making an assignment to
        the _flag_admin field so it can be returned in the getter.
        """
        self._flag_admin = newflag_admin

    #### identifier for admin approval

    @property
    def flag_approval(self):
        """
        :return: The identifier for admin approval
        """
        return self._flag_approval

    @flag_approval.setter
    def flag_approval(self, newflag_approval):
        """
        Set the identifier for admin approval

        This is as simple as it looks, simply making an assignment to
        the _flag_admin field so it can be returned in the getter.
        """
        self._flag_approval = newflag_approval

    #### check password

    def check_password(self, plaintext):
        """
        Check that a plaintext password is equal to the hashed password.

        At this stage, this method is not being used except in testing.
        :param plaintext: plaintext password to check
        :return: Boolean value; if true, then the plaintext and hash correspond, else false.
        """
        return check_password_hash(self.password, plaintext)
