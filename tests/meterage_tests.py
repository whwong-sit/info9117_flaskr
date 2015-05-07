import os
import meterage
import unittest
import tempfile
from contextlib import closing


class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        """
        create a new test client, initialise a database and activate TESTING mode
        """
        self.db_fd, meterage.app.config['DATABASE'] = tempfile.mkstemp()
        meterage.app.config['TESTING'] = True
        self.app = meterage.app.test_client()
        meterage.init_db()

        # add users to the temporary database
        # Note that an admin and a normal user are added.
        with closing(meterage.connect_db()) as db:
            db.execute('insert into userPassword (username, password, gravataremail) values (?, ?, ?)',
                       ['admin', 'default', 'daisy22229999@gmail.com'])
            db.execute('insert into userPassword (username, password, gravataremail) values (?, ?, ?)',
                       ['hari', 'seldon', 'tt@gmail.com'])
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

    def test_no_messages(self):
        """
        When we only have the userPassword table in the database populated,
        make sure that 'No entries here yet' is present in the data when
        we check show_entries.html (i.e. the root page)
        """
        rv = self.app.get('/')
        assert 'No entries here yet' in rv.get_data()

    def userPassword_content(self):
        """
        Get all the data in the userPassword table
        """
        with closing(meterage.connect_db()) as db:
            cur = db.execute('select username, password, gravataremail from userPassword')
            return [dict(username=row[0], password=row[1], gravataremail=row[2]) for row in cur.fetchall()]

    #### Basic tests

    def test_login_logout(self):
        """
        Test that all users may log in and log out
        """
        for entry in self.userPassword_content():
            rv = self.login(entry['username'], entry['password'])
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
        for entry in self.userPassword_content():
            self.login(entry['username'], entry['password'])
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

    #### Gravatar Tests

    # def test_email_address_in_returned_data(self):
    #     """
    #     test whether an email address posted to the login page is returned in the results
    #     """
    #     for email in ["daisy22229999@gmail.com", "daisy200029@gmail.com", "tt@gmail.com"]:
    #         self.login('admin', 'default')
    #         rv = self.app.post('/add', data=dict(
    #             title='<Hello>',
    #             text='<strong>HTML</strong> allowed here',
    #             username='admin',
    #             email=email
    #         ), follow_redirects=True)
    #         assert 'No entries here so far' not in rv.get_data()
    #         assert '&lt;Hello&gt;' in rv.get_data()
    #         assert '<strong>HTML</strong> allowed here' in rv.get_data()
    #         assert 'admin' in rv.get_data()
    #         assert 'daisy22229999@gmail.com' in rv.get_data()

if __name__ == '__main__':
    unittest.main()
