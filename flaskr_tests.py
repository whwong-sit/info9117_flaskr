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

<<<<<<< HEAD
    #test for multiple users
    def test_multiple_login_logout(self):
	# test admin login
	rv = self.login('admin','default')
	assert 'You were logged in' in rv.data
	rv = self.logout()
	assert 'You were logged out' in rv.data
	
	#test adam login
	rv = self.login('adam','alpha')
	assert 'You were logged in' in rv.data
	rv = self.logout()
	assert 'You were logged out' in rv.data

	#test bob login
	rv = self.login('bob','bravo')
	assert 'You were logged in' in rv.data
	rv = self.logout()
	assert 'You were logged out' in rv.data
	
	#test cat login
	rv = self.login('cat','charlie')
	assert 'You were logged in' in rv.data
	rv = self.logout()
	assert 'You were logged out' in rv.data

	#test for invalid user
	rv = self.login('adminx','default')
	assert 'Invalid username' in rv.data
	rv = self.login('admin','defaultx')
	assert 'Invalid password' in rv.data
=======
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
>>>>>>> 967bfd00bad2cace6dccfaf0261d0c390953b733

    def test_login_logout(self):
        rv = self.login('admin', 'default')
        assert 'You were logged in' in rv.data
        rv = self.logout()
        assert 'You were logged out' in rv.data
        rv = self.login('adminx', 'default')
        assert 'Invalid username' in rv.data
        rv = self.login('admin', 'defaultx')
        assert 'Invalid password' in rv.data

	#test for adding message by admin
    def test_messages_admin(self):
        self.login('admin', 'default')
        rv = self.app.post('/add', data=dict(
            title='<Hello admin>',
            text='<strong>HTML</strong> allowed here',
			username='admin',
			sdate='2015-01-01',
			stime='09:00:00',
			edate='2015-01-01',
			etime='13:00:00'
        ), follow_redirects=True)
        assert 'No entries here so far' not in rv.data
        assert '&lt;Hello admin&gt;' in rv.data
        assert '<strong>HTML</strong> allowed here' in rv.data
        assert 'admin' in rv.data
        assert '2015-01-01' in rv.data
        assert '09:00:00' in rv.data
        assert '2015-01-01' in rv.data
        assert '13:00:00' in rv.data
		
	#test for adding message by adam
    def test_messages_adam(self):
        self.login('adam', 'alpha')
        rv = self.app.post('/add', data=dict(
            title='<Hello adam>',
            text='<strong>HTML</strong> allowed here',
			username='adam',
			sdate='2015-01-01',
			stime='09:00:00',
			edate='2015-01-02',
			etime='13:00:00'
        ), follow_redirects=True)
        assert 'No entries here so far' not in rv.data
        assert '&lt;Hello adam&gt;' in rv.data
        assert '<strong>HTML</strong> allowed here' in rv.data
        assert 'adam' in rv.data
        assert '2015-01-01' in rv.data
        assert '09:00:00' in rv.data
        assert '2015-01-02' in rv.data
        assert '13:00:00' in rv.data

	#test for adding message by bob
    def test_messages_bob(self):
        self.login('bob', 'bravo')
        rv = self.app.post('/add', data=dict(
            title='<Hello bob>',
            text='<strong>HTML</strong> allowed here',
			username='bob',
			sdate='2015-01-02',
			stime='10:00:00',
			edate='2015-01-03',
			etime='16:00:00'
        ), follow_redirects=True)
        assert 'No entries here so far' not in rv.data
        assert '&lt;Hello bob&gt;' in rv.data
        assert '<strong>HTML</strong> allowed here' in rv.data
        assert 'bob' in rv.data
        assert '2015-01-02' in rv.data
        assert '10:00:00' in rv.data
        assert '2015-01-03' in rv.data
        assert '16:00:00' in rv.data
		
	#test for adding message by cat
    def test_messages_cat(self):
        self.login('cat', 'charlie')
        rv = self.app.post('/add', data=dict(
            title='<Hello cat>',
            text='<strong>HTML</strong> allowed here',
			username='cat',
			sdate='2015-01-02',
			stime='16:00:00',
			edate='2015-01-03',
			etime='20:00:00'
        ), follow_redirects=True)
        assert 'No entries here so far' not in rv.data
        assert '&lt;Hello cat&gt;' in rv.data
        assert '<strong>HTML</strong> allowed here' in rv.data
        assert 'cat' in rv.data
        assert '2015-01-02' in rv.data
        assert '16:00:00' in rv.data
        assert '2015-01-03' in rv.data
        assert '20:00:00' in rv.data

if __name__ == '__main__':
    unittest.main()

