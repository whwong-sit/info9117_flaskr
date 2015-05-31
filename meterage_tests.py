import os
import unittest
import tempfile
import time

import meterage

from flask_bcrypt import generate_password_hash


class MeterageBaseTestClass(unittest.TestCase):
    """
    Base class for unit tests, with some convenient methods to inherit.
    """

    def setUp(self):
        """
        create a new test client, initialise a database and activate TESTING mode
        """
        self.db_fd, meterage.app.config['DATABASE'] = tempfile.mkstemp()
        meterage.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + meterage.app.config['DATABASE']
        meterage.app.config['TESTING'] = True

        # We cannot be in debug mode or Flask raises an AssertionError
        # TODO investigate this further; it is to do with imports into a central location upon initialisation
        meterage.app.config['DEBUG'] = False

        # Make this True to see all of the SQL queries fly by in the console
        meterage.app.config['SQLALCHEMY_ECHO'] = False
        meterage.db = meterage.SQLAlchemy(meterage.app)
        reload(meterage.models)
        self.app = meterage.app.test_client()

        meterage.db.create_all()

        usernames = ["admin", "hari"]
        passwords = ["default", "seldon"]
        gravataremails = ["daisy22229999@gmail.com", "nongravataremailaddress@gmail.com"]
        self.users = zip(usernames, passwords, gravataremails)

        for username, password, gravataremail in self.users:
            if username == 'admin':
                user = meterage.User(username, password, gravataremail, True)
            else:
                user = meterage.User(username, password, gravataremail)
            meterage.db.session.add(user)
        meterage.db.session.commit()

    def tearDown(self):
        """
        close temporary file and remove from filesystem
        """
        os.unlink(meterage.app.config['DATABASE'])

        # Some useful functions

    def login(self, username, password):
        """
        login as the user specified by username and password
        :param username: username to post
        :param password: password to post
        :return: the page that you are redirected to upon login
        """
        return self.app.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def logout(self):
        """
        log out
        """
        return self.app.get('/logout', follow_redirects=True)

    def generic_post(self):
        """
        make a generic post
        """
        return self.app.post('/add', data=dict(
            title='<Hello>',
            text='<strong>HTML</strong> allowed here',
            start_time='<15:00>',
            end_time='<17:30>'
        ), follow_redirects=True)


class BasicTests(MeterageBaseTestClass):

    def test_no_messages(self):
        """
        When we only have the userPassword table in the database populated,
        make sure that 'No entries here yet' is present in the data when
        we check show_entries.html (i.e. the root page)
        """
        rv = self.app.get('/')
        self.assertIn('No entries here yet', rv.get_data(), 'Incorrect page displayed when there are no messages')

    def test_login_logout(self):
        """
        Test that all users may log in and log out
        """
        for user in self.users:
            rv = self.login(user[0], user[1])
            self.assertIn('You were logged in', rv.get_data(), 'Login failed')
            rv = self.logout()
            self.assertIn('You were logged out', rv.get_data(), 'Logout failed')

    def test_invalid(self):
        """
        Test that we get appropriate responses for invalid usernames and/or passwords
        """
        # test for invalid user
        rv = self.login('adminx', 'default')
        self.assertIn('Invalid username', rv.get_data())

        # test for invalid password
        rv = self.login('admin', 'defaultx')
        self.assertIn('Invalid password', rv.get_data())

        # test for invalid username and password
        rv = self.login('adminx', 'defaultx')
        self.assertIn('Invalid username', rv.get_data())

    def test_messages(self):
        """
        Test all users may make posts, and the appropriate data are in the
        page returned.
        Check that HTML is allowed in the text but not in the title"
        """
        for username, password, gravataremail in self.users:
            self.login(username, password)
            rv = self.generic_post()
            self.assertNotIn('No entries here so far', rv.get_data(), 'Post unsuccessful')
            self.assertIn('&lt;Hello&gt;', rv.get_data())
            self.assertIn('<strong>HTML</strong> allowed here', rv.get_data())
            with self.app.session_transaction() as sess:
                # see http://flask.pocoo.org/docs/0.10/testing/#accessing-and-modifying-sessions for
                # an explanation of accessing sessions during testing.
                self.assertIn(sess['username'], rv.get_data())
            self.assertIn('15:00', rv.get_data())
            self.assertIn('17:30', rv.get_data())

    def test_message_maps_to_username(self):
        """
        check that username is printed along with message, and that
        the username is the right one
        """
        self.login('admin', 'default')
        rv = self.generic_post()
        self.assertIn("by admin", rv.get_data())

    def test_read_log_without_login(self):
        """
        Ensure that someone who is not logged in can still read the logs
        """
        self.login('admin', 'default')
        self.generic_post()
        self.logout()
        rv = self.app.get('/')
        assert "&lt;Hello&gt" in rv.get_data()
        assert "by admin" in rv.get_data()


class ChangePasswordsTests(MeterageBaseTestClass):

    def test_change_password(self):
        """
        Test that the admin can change an existing user's password
        """
        self.login(username='admin', password='default')

        rv = self.app.post('/change_password', data=dict(
            username='hari',
            password='1234',
            confirm_password='1234'
        ), follow_redirects=True)

        self.assertIn('Successfully changed user password', rv.get_data())

    def test_change_non_exist_password(self):
        """
        Test that trying to change the password of a user that does not exist
        behaves as we expect
        """
        self.login(username='admin', password='default')

        rv = self.app.post('/change_password', data=dict(
            username='nonexist',
            password='test',
            confirm_password='test'
        ), follow_redirects=True)

        self.assertIn('User does not exist', rv.get_data())

    def test_login_after_change(self):
        """
        Test for behaviour following a change of password.

        """
        # log in as the admin; only the admin can change passwords
        self.login(username='admin', password='default')

        # change hari's password
        self.app.post('/change_password', data=dict(
            username='hari',
            password='1234',
            confirm_password='1234'
        ), follow_redirects=True)

        # Test hari login with old password
        rv = self.login('hari', 'seldon')
        self.assertIn('Invalid password', rv.get_data())

        # Test hari login with new password
        rv = self.login('hari', '1234')
        self.assertIn('You were logged in', rv.get_data())


class HashedPasswordsTests(MeterageBaseTestClass):

    def test_User_password_hashed_upon_initialising(self):
        """
        Check that initialising a User object results in automatic hashing of the plaintext password
        """

        user = meterage.User("bilbo", "baggins", "bilbo@hobbiton.tolk")
        self.assertNotEqual(user.password, "baggins", "password has not been automatically hashed")

    def test_hashed_password_added_to_database(self):
        """
        Check that the hashed password is added to the database, not the plain text.
        """
        for user in self.users:
            u = meterage.User.query.filter_by(username=user[0]).first()
            self.assertFalse(u.password == user[1], "Hashed password has not been added to the database")

    def test_hashed_password_is_not_plaintext(self):
        """
        Check that the password is not plain text when we try to, for example, reset it.

        Check other aspects of changing User object's password
        """
        user = meterage.User("xXx_Supa_Saiyan_xXx", "password1", "swag@yolo.net")
        user.password = "dogsname"
        self.assertNotEqual(user.password, "password1", "password not reset, password is plain text")
        self.assertNotEqual(user.password, generate_password_hash("password1"), "password not reset")
        self.assertNotEqual(user.password, "dogsname", "password is plain text")
        self.assertTrue(user.check_password("dogsname"), "password not changed successfully")

    def test_entering_hash_does_not_succeed(self):
        """
        Test that entering the actual hash into the "password" box does not result in a successful login.
        """
        for user in self.users:
            u = meterage.User.query.filter_by(username=user[0]).first()
            rv = self.login(u.username, u.password)
            self.assertIn("Invalid password", rv.get_data(), "Login did not fail as it should have")


class TimeAndCommentTests(MeterageBaseTestClass):

    def test_time(self):
        self.login('admin', 'default')
        curr_time = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
        rv = self.app.post('/add', data=dict(
            title='<Hello>',
            text='<strong>HTML</strong> allowed here',
            start_time='<15:00>',
            end_time=curr_time
        ), follow_redirects=True)
        self.assertNotIn('No entries here so far', rv.get_data(), 'Post unsuccessful')
        self.assertIn('&lt;Hello&gt;', rv.get_data())
        self.assertIn('by admin', rv.get_data())
        self.assertIn(curr_time, rv.get_data())

    def test_comment(self):
        self.login('admin', 'default')
        self.generic_post()
        rv = self.app.post('/1/add_comments', data=dict(
            comment_input='<FinalVERSION>'
        ), follow_redirects=True)
        self.assertNotIn('No entries here so far', rv.get_data(), 'Post unsuccessful')
        self.assertIn('&lt;FinalVERSION&gt;', rv.get_data())
        self.assertIn('by admin', rv.get_data())

    def test_end_time(self):
        self.login('admin', 'default')
        self.generic_post()
        rv = self.app.post('/1/add_end_time', follow_redirects=True)
        curr_time = time.strftime("%Y-%m-%d %H:%M:", time.localtime())
        self.assertNotIn('No entries here so far', rv.get_data(), 'Post unsuccessful')
        self.assertIn('&lt;Hello&gt;', rv.get_data())
        self.assertIn('by admin', rv.get_data())
        self.assertIn('End at: ' + curr_time, rv.get_data())


class GravatarTests(MeterageBaseTestClass):

    def test_avatar(self):
        """
        Test that meterage.gravatar object does produce the correct Gravatar
        """
        known_url = 'http://www.gravatar.com/avatar/bf6c2e089dbd27ec1868027525bc42fe?s=50&d=retro&r=g'
        self.assertEqual(meterage.views.gravatar("daisy22229999@gmail.com"),
                         known_url, "Gravatar URL produced is incorrect")

    def test_gravatar_shown(self):
        """
        Test that the gravatar is shown on show_entries.html
        """
        self.login('admin', 'default')
        rv = self.generic_post()
        image = '<i><img src="http://www.gravatar.com/avatar/bf6c2e089dbd27e' \
                'c1868027525bc42fe?s=50&amp;d=retro&amp;r=g"></i>'
        self.assertIn(image, rv.get_data(), "image is displayed incorrectly on show_entries.html")

    def test_non_gravatar_user(self):
        """
        Test that non-gravatar users still get some kind of image
        """
        self.login("hari", "seldon")
        rv = self.generic_post()
        some_image = '<i><img src="http://www.gravatar.com/avatar/'
        self.assertIn(some_image, rv.get_data(), "image is displayed incorrectly on show_entries.html")


class UserWebInterfaceTests(MeterageBaseTestClass):

    def test_web_interface_accessible(self):
        raise NotImplementedError('Daisy said she wrote these tests on the master branch')

    def test_can_change_username(self):
        raise NotImplementedError('Daisy said she wrote these tests on the master branch')

    def test_can_change_gravatar_email(self):
        raise NotImplementedError('Daisy said she wrote these tests on the master branch')

    def test_username_unique(self):
        raise NotImplementedError('Daisy said she wrote these tests on the master branch')

if __name__ == '__main__':
    unittest.main()
