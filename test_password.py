#####
import os
import flaskr
import unittest
import tempfile
from sqlite3 import dbapi2 as sqlite3

class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, flaskr.app.config['DATABASE'] = tempfile.mkstemp()
        flaskr.app.config['TESTING'] = True
        self.app = flaskr.app.test_client()
        flaskr.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(flaskr.app.config['DATABASE'] )

    def login(self, username, password):
        return self.app.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def change_password(self, username, password, confirm_password):
        return self.app.post('/change_password', data=dict(
            username=username,
            password=password,
            comfirm_password=confirm_password
        ), follow_redirects=True)

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)
 
    #test changing existing user password
    def test_change_password(self):
        db = sqlite3.connect(flaskr.app.config['DATABASE'])
        db.execute('insert into userPassword values(?,?)',['admin','default'])
        db.execute('insert into userPassword values(?,?)',['jim','bean'])
        db.commit()
        self.login(username='admin',password='default')
        self.app.get('/change_password', follow_redirects=True)
        rv = self.app.post('/change_password', data=dict(
            username='jim',
            password='1234',
            confirm_password='1234'
        ), follow_redirects=True)
        #print rv.data
        assert 'Successfully changed user password' in rv.data
        rv = self.logout()

    #test changing non-existing user password
    def test_change_non_exist_password(self):
        db = sqlite3.connect(flaskr.app.config['DATABASE'])
        db.execute('insert into userPassword values(?,?)',['admin','default'])
        db.commit()
        self.login(username='admin',password='default')
        self.app.get('/change_password', follow_redirects=True)
        rv = self.app.post('/change_password', data=dict(
            username='nonexist',
            password='test',
            confirm_password='test'
        ), follow_redirects=True)
        #print rv.data
        assert 'User does not exist' in rv.data
        rv = self.logout()
		
    #test login after administrator changed user password
    def test_multiple_login_logout(self):
        db = sqlite3.connect(flaskr.app.config['DATABASE'])
        db.execute('insert into userPassword values(?,?)',['jim','1234'])
        db.commit()
        # Test jim login with old password

        r = self.login('jim', 'bean')
        #print r.data
        assert 'Invalid password' in r.data

        # Test jim login with new password
        r = self.login('jim', '1234')
        assert 'You were logged in' in r.data
        r = self.logout()
        assert 'You were logged out' in r.data

if __name__ == '__main__':
    unittest.main()