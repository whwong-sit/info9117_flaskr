import os
import flaskr
import unittest
import tempfile

class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, flaskr.app.config['DATABASE'] = tempfile.mkstemp()
        flaskr.app.config['TESTING'] = True
        self.app = flaskr.app.test_client()
        flaskr.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink( flaskr.app.config['DATABASE'] )

    def test_empty_db(self):
        rv = self.app.get('/')
        assert 'No entries here yet' in rv.data

    def login(self, username, password):
        return self.app.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)

    def test_multiple_login_logout(self):
        # Test admin login
        rv = self.login('admin', 'default')
        assert 'You were logged in' in rv.data
        rv = self.logout()
        assert 'You were logged out' in rv.data

        # Test Jim login
        rv = self.login('jim', 'bean')
        assert 'You were logged in' in rv.data
        rv = self.logout()
        assert 'You were logged out' in rv.data

        # Test Spock login
        rv = self.login('spock', 'vulcan')
        assert 'You were logged in' in rv.data
        rv = self.logout()
        assert 'You were logged out' in rv.data


        # Test non-recognised users
        rv = self.login('adminx', 'default')
        assert 'Invalid username' in rv.data
        rv = self.login('admin', 'defaultx')
        assert 'Invalid password' in rv.data

    def test_login_logout(self):
        rv = self.login('admin', 'default')
        assert 'You were logged in' in rv.data
        rv = self.logout()
        assert 'You were logged out' in rv.data
        rv = self.login('adminx', 'default')
        assert 'Invalid username' in rv.data
        rv = self.login('admin', 'defaultx')
        assert 'Invalid password' in rv.data

    def test_messages(self):
        self.login('admin', 'default')
        rv = self.app.post('/add', data=dict(
            title='<Hi>',
            text='<strong>HTML</strong> allowed here',
            start_time= '<15:00>',
            end_time= '<17:30>',

        ), follow_redirects=True)
        assert 'No entries here so far' not in rv.data
        assert '&lt;Hi&gt;' in rv.data
        assert '<strong>HTML</strong> allowed here' in rv.data

    def test_message_other_user(self):
        self.login('jim', 'bean')
        rv = self.app.post('/add', data=dict(
            title='<C++Exercise01>',
            text='<strong>HTML</strong> allowed here',
        ), follow_redirects=True)
        assert 'No entries here so far' not in rv.data 
        assert '&lt;C++Exercise01&gt;' in rv.data
        assert '<strong>HTML</strong> allowed here' in rv.data
        assert 'jim' in rv.data


    def test_time(self):
        from time import gmtime, strftime
        self.login('admin', 'default')
        rv = self.app.post('/add', data=dict(
            title='<Hi>',
            text='<strong>HTML</strong> allowed here',
        ), follow_redirects=True)
        curr_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        assert 'No entries here so far' not in rv.data
        assert '&lt;Hi&gt;' in rv.data
        assert 'by admin' in rv.data
        assert curr_time in rv.data

    def test_comment(self):
        self.login('admin', 'default')
        self.app.post('/add', data=dict(
            title='Hi',
            text='<strong>HTML</strong> allowed here'
        ), follow_redirects=True)
        rv = self.app.post('/1/add_comments', data= dict(
            comment_input = '<FinalVERSION>'
        ), follow_redirects=True)
        assert 'No entries here so far' not in rv.data
        assert '&lt;FinalVERSION&gt;' in rv.data
        assert 'by admin' in rv.data
       
        
    def test_end_time(self):
        from time import gmtime, strftime


        self.login('admin', 'default')
        self.app.post('/add', data= dict(
            title='<Hi>',
            text='<strong>HTML</strong> allowed here'
        ), follow_redirects=True)
        rv = self.app.post('/1/add_end_time', follow_redirects=True)
        curr_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        assert 'No entries here so far' not in rv.data
        assert '&lt;Hi&gt;' in rv.data
        assert 'by admin' in rv.data
        assert 'End at: '+ curr_time in rv.data

        

if __name__ == '__main__':
    unittest.main()


