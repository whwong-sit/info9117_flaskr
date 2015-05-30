import os
import datetime
import meterage
import unittest
import tempfile
from contextlib import closing
from models import User
from flask_bcrypt import generate_password_hash
from time import gmtime, strftime, time


class MeterageBaseTestClass(unittest.TestCase):
    """
    Base class for unit tests, with some convenient methods to inherit.
    """

    def setUp(self):
        """
        create a new test client, initialise a database and activate TESTING mode
        """
        self.db_fd, meterage.app.config['DATABASE'] = tempfile.mkstemp()
        meterage.app.config['TESTING'] = True
        self.app = meterage.app.test_client()
        meterage.init_db()

        global users
        usernames = ["admin", "hari"]
        passwords = ["default", "seldon"]
        gravataremails = ["daisy22229999@gmail.com", "nongravataremailaddress@gmail.com"]
        users = zip(usernames, passwords, gravataremails)

        # add an admin and a normal user to the database
        with closing(meterage.connect_db()) as db:
            for username, password, gravataremail in users:
                user = User(username, password, gravataremail)
                db.execute('insert into userPassword (username, password, gravataremail) values (?, ?, ?)',
                           [user.username, user.password, user.gravataremail])
            db.commit()

    def tearDown(self):
        """
        close temporary file and remove from filesystem
        """
        os.close(self.db_fd)
        os.unlink(meterage.app.config['DATABASE'])

        #### Some useful functions

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
            end_time=strftime("%Y-%m-%d %H:%M:%S", gmtime()),
            task_des='hahahahah',
            ), follow_redirects=True)

    def userPassword_content(self):
        """
        Get all the data in the userPassword table
        """
        with closing(meterage.connect_db()) as db:
            cur = db.execute('select username, password, gravataremail from userPassword')
            return [dict(username=row[0], password=row[1], gravataremail=row[2]) for row in cur.fetchall()]


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
        for user in users:
            rv = self.login(users[1][0], users[1][1])
            self.assertIn('You were logged in', rv.get_data())
            rv = self.logout()
            self.assertIn('You were logged out', rv.get_data())

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
        for username, password, gravataremail in users:
            self.login(username, password)
            rv = self.generic_post()
            self.assertNotIn('No entries here so far', rv.get_data(), 'Post unsuccessful')
            self.assertIn('&lt;Hello&gt;', rv.get_data())
            self.assertIn('<strong>HTML</strong> allowed here', rv.get_data())
            with self.app.session_transaction() as sess:
                # see http://flask.pocoo.org/docs/0.10/testing/#accessing-and-modifying-sessions for
                # an explanation of accessing sessions during testing.
                self.assertIn(sess['username'], unicode(rv.get_data(), 'utf-8'))

    def test_message_maps_to_username(self):
        """
        check that username is printed along with message, and that
        the username is the right one
        """
        self.login('admin', 'default')
        rv= self.generic_post()
        assert "by admin" in rv.get_data()

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

        user = User("bilbo", "baggins", "bilbo@hobbiton.tolk")
        self.assertNotEqual(user.password, "baggins", "password has not been automatically hashed")

    def test_hashed_password_added_to_database(self):
        """
        Check that the hashed password is added to the database, not the plain text.
        """
        with closing(meterage.connect_db()) as db:
            for user in users:
                cur = db.execute('select username, password from userPassword where username=?', [user[0]])
                row = cur.fetchone()
                self.assertFalse(row[1] == user[1], "Hashed password has not been added to the database")
                cur.close()

    def test_hashed_password_is_not_plaintext(self):
        """
        Check that the password is not plain text when we try to, for example, reset it.

        Check other aspects of changing User object's password
        """
        user = User("xXx_Supa_Saiyan_xXx", "password1", "swag@yolo.net")
        user.password = "dogsname"
        self.assertNotEqual(user.password, "password1", "password not reset, password is plain text")
        self.assertNotEqual(user.password, generate_password_hash("password1"), "password not reset")
        self.assertNotEqual(user.password, "dogsname", "password is plain text")
        self.assertTrue(user.check_password("dogsname"), "password not changed successfully")

    def test_entering_hash_does_not_succeed(self):
        """
        Test that entering the actual hash into the "password" box does not result in a successful login.
        """

        with closing(meterage.connect_db()) as db:
            for user in users:
                cur = db.execute('select username, password from userPassword where username=?', [user[0]])
                row = cur.fetchone()
                rv = self.login(row[0], row[1])
                self.assertIn("Invalid password", rv.get_data(), "Login did not fail as it should have")
                cur.close()


class TimeAndCommentTests(MeterageBaseTestClass):

    def test_start_time(self):
        self.login('admin', 'default')
        rv = self.app.post('/add', data=dict(
            title='<Hello>',
            text='<strong>HTML</strong> allowed here',
            task_des= ' hahahahah',
            start_time='<15:00>',
        ), follow_redirects=True)
        self.assertNotIn('No entries here so far', rv.get_data(), 'Post unsuccessful')
        self.assertIn('by admin', rv.get_data())
        self.assertIn(' hahahahah', rv.get_data())

    def test_comment(self):
        self.login('admin', 'default')
        self.generic_post()
        rv = self.app.post('/1/add_comments', data= dict(
            comment_input='<FinalVERSION>'
        ), follow_redirects=True)
        self.assertNotIn('No entries here so far', rv.get_data(), 'Post unsuccessful')
        self.assertIn('&lt;FinalVERSION&gt;', rv.get_data())
        self.assertIn('by admin', rv.get_data())

    def test_end_time(self):
        self.login('admin', 'default')
        self.generic_post()
        rv = self.app.post('/1/add_end_time', follow_redirects=True)
        curr_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.assertNotIn('No entries here so far', rv.get_data(), 'Post unsuccessful')
        self.assertIn('&lt;Hello&gt;', rv.get_data())
        self.assertIn('by admin', rv.get_data())
        self.assertIn(curr_time, rv.get_data())

    def test_User_Role(self):
        self.login('admin', 'default')
        self.generic_post()
        rv=self.app.post('/1/add_roles', data=dict(
            user_role='<fathima>',
            ), follow_redirects=True)
        assert '&lt;fathima&gt;' in rv.data


    def test_description(self):
        self.login('admin', 'default')
        self.generic_post()
        rv = self.app.post('/add', data=dict(
            title='<Hi>',
            text='<strong>HTML</strong> allowed here',
            start_time= '<15:00>',
            task_des='User is talking about food'
            ), follow_redirects=True)
        assert 'No entries here so far' not in rv.data
        assert 'User is talking about food' in rv.data

class GravatarTests(MeterageBaseTestClass):

    def test_avatar(self):
        """
        Test that meterage.avatar() method does return the correct Gravatar
        """
        known_url = "http://www.gravatar.com/avatar/bf6c2e089dbd27ec1868027525bc42fe?s=50&d=monsterid"
        self.assertEqual(meterage.avatar("daisy22229999@gmail.com"), known_url, "Gravatar URL produced is incorrect")

    def test_gravatar_shown(self):
        """
        Test that the gravatar is shown on show_entries.html
        """
        self.login("admin", "default")
        rv = self.generic_post()
        image = '<i><img src="http://www.gravatar.com/avatar/bf6c2e089dbd27ec1868027525bc42fe?s=50&amp;d=monsterid">'
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
        self.login(username='hari', password='seldon')

        rv = self.app.get('/user/<username>')
        self.assertFalse(rv.status_code == 404, "We are unable to access the manage details page")
        # self.assertIn('hari', rv.get_data())
        # self.assertIn('nongravataremailaddress@gmail.com', rv.get_data())

    def test_can_change_username(self):

        self.login(username='hari', password='seldon')

        rv = self.app.post('/user/<username>', data=dict(
            username='hary',
            gravataremail='hary@gmail.com',
            save='save',
        ), follow_redirects=True)

        self.assertIn('hary', rv.get_data())

        with closing(meterage.connect_db()) as db:
            cur = db.execute('select username, gravataremail from userPassword where username=?', ['hary'])
            row = cur.fetchone()
            self.assertFalse(row[0] == 'hari', "username has not been added to the database")
            cur.close()

    def test_can_change_gravatar_email(self):

        self.login(username='hari', password='seldon')

        rv = self.app.post('/user/<username>', data=dict(
            username='hary',
            gravataremail='hary@gmail.com',
            save='save',
        ), follow_redirects=True)

        self.assertIn('hary@gmail.com', rv.get_data())

        with closing(meterage.connect_db()) as db:
            cur = db.execute('select username, gravataremail from userPassword where username=?', ['hary'])
            row = cur.fetchone()
            self.assertFalse(row[1] == "nongravataremailaddress@gmail.com", "gravataremail has not been added to the database")
            cur.close()



    def test_username_unique(self):
        with closing(meterage.connect_db()) as db:
            for user in users:
                cur = db.execute('select count(username) from userPassword where username=?', [user[0]])
                row = cur.fetchone()
                self.assertTrue(row[0] == 1, "The username is unique")
                cur.close()

if __name__ == '__main__':
    unittest.main()
