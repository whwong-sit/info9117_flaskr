import os
import meterage
import unittest
import tempfile
from contextlib import closing
from models import User


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

        # flat dictionary of users, so we have access to the plain text versions of the passwords
        global users
        users = {"admin": "default", "hari": "seldon"}

        # add users to the temporary database, with their proper hashed passwords
        # Note that an admin and a normal user are added.
        with closing(meterage.connect_db()) as db:
            for user in [User("admin", users["admin"]), User("hari", users["hari"])]:
                db.execute('insert into userPassword (username, password) values (?, ?)',
                           [user.username, user.password])
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
            sdate='2015-01-01',
            stime='09:00:00',
            edate='2015-01-02',
            etime='13:00:00'
        ), follow_redirects=True)


class BasicTests(MeterageBaseTestClass):

    def test_no_messages(self):
        """
        When we only have the userPassword table in the database populated,
        make sure that 'No entries here yet' is present in the data when
        we check show_entries.html (i.e. the root page)
        """
        rv = self.app.get('/')
        assert 'No entries here yet' in rv.get_data()

    def test_login_logout(self):
        """
        Test that all users may log in and log out
        """
        for user in users:
            rv = self.login(user, users[user])
            assert 'You were logged in' in rv.get_data()
            rv = self.logout()
            assert 'You were logged out' in rv.get_data()

    def test_invalid(self):
        """
        Test that we get appropriate responses for invalid usernames and/or passwords
        """
        # test for invalid user
        rv = self.login('adminx', 'default')
        assert 'Invalid username' in rv.get_data()

        # test for invalid password
        rv = self.login('admin', 'defaultx')
        assert 'Invalid password' in rv.get_data()

        # test for invalid username and password
        rv = self.login('adminx', 'defaultx')
        assert 'Invalid username' in rv.get_data()

    def test_messages(self):
        """
        Test all users may make posts, and the appropriate data are in the
        page returned.
        Check that HTML is allowed in the text but not in the title"
        """
        for user in users:
            self.login(user, users[user])
            rv = self.generic_post()
            assert 'No entries here so far' not in rv.get_data()
            assert '&lt;Hello&gt;' in rv.get_data()
            assert '<strong>HTML</strong> allowed here' in rv.get_data()
            with self.app.session_transaction() as sess:
                # see http://flask.pocoo.org/docs/0.10/testing/#accessing-and-modifying-sessions for
                # an explanation of accessing sessions during testing.
                assert sess['username'] in rv.get_data()
            assert '2015-01-01' in rv.get_data()
            assert '09:00:00' in rv.get_data()
            assert '2015-01-02' in rv.get_data()
            assert '13:00:00' in rv.get_data()

    def test_message_maps_to_username(self):
        """
        check that username is printed along with message, and that
        the username is the right one
        """
        self.login('admin', 'default')
        rv = self.generic_post()
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

    #### Changing passwords tests

    # def test_change_password(self):
    #     """
    #     Test that the admin can change an existing user's password
    #     """
    #     # log in as the admin; only the admin can change passwords
    #     self.login(username='admin',password='default')
    #
    #     rv = self.app.post('/change_password', data=dict(
    #         username='hari',
    #         password='1234',
    #         confirm_password='1234'
    #     ), follow_redirects=True)
    #
    #     assert 'Successfully changed user password' in rv.get_data()
    #
    # def test_change_non_exist_password(self):
    #     """
    #     Test that trying to change the password of a user that does not exist
    #     behaves as we expect
    #     """
    #     # log in as the admin; only the admin can change passwords
    #     self.login(username='admin', password='default')
    #
    #     rv = self.app.post('/change_password', data=dict(
    #         username='nonexist',
    #         password='test',
    #         confirm_password='test'
    #     ), follow_redirects=True)
    #
    #     assert 'User does not exist' in rv.get_data()
    #
    # def test_login_after_change(self):
    #     """
    #     Test for behaviour following a change of password.
    #
    #     """
    #     # log in as the admin; only the admin can change passwords
    #     self.login(username='admin', password='default')
    #
    #     # change hari's password
    #     self.app.post('/change_password', data=dict(
    #         username='hari',
    #         password='1234',
    #         confirm_password='1234'
    #     ), follow_redirects=True)
    #
    #     # Test hari login with old password
    #     rv = self.login('hari', 'seldon')
    #     assert 'Invalid password' in rv.get_data()
    #
    #     # Test hari login with new password
    #     rv = self.login('hari', '1234')
    #     assert 'You were logged in' in rv.get_data()


class ChangePasswordsTests(MeterageBaseTestClass):

    def test_change_password(self):
        """
        Test that the admin can change an existing user's password
        """
        # log in as the admin; only the admin can change passwords
        self.login(username='admin',password='default')

        rv = self.app.post('/change_password', data=dict(
            username='hari',
            password='1234',
            confirm_password='1234'
        ), follow_redirects=True)

        assert 'Successfully changed user password' in rv.get_data()

    def test_change_non_exist_password(self):
        """
        Test that trying to change the password of a user that does not exist
        behaves as we expect
        """
        # log in as the admin; only the admin can change passwords
        self.login(username='admin', password='default')

        rv = self.app.post('/change_password', data=dict(
            username='nonexist',
            password='test',
            confirm_password='test'
        ), follow_redirects=True)

        assert 'User does not exist' in rv.get_data()

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
        assert 'Invalid password' in rv.get_data()

        # Test hari login with new password
        rv = self.login('hari', '1234')
        assert 'You were logged in' in rv.get_data()


class HashedPasswordsTests(MeterageBaseTestClass):

    def test_User_password_hashed_upon_initialising(self):
        """
        Check that initialising a User object results in automatic hashing of the plaintext password
        """
        raise NotImplementedError("Not implemented")

    def test_hashed_password_added_to_database(self):
        """
        Check that the hashed password is added to the database, not the plain text.
        """
        raise NotImplementedError("Not implemented")

    def test_hashed_password_is_not_plaintext(self):
        """
        Check that the password is not plain text when we try to, for example, reset it to something else.
        """
        raise NotImplementedError("Not implemented")

    def test_entering_hash_does_not_succeed(self):
        """
        Test that entering the actual hash into the "password" box does not result in a successful login.
        """
        raise NotImplementedError("Not implemented")

if __name__ == '__main__':
    unittest.main()
