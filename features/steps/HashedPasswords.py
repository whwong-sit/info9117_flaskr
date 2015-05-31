from contextlib import closing
from behave import *
import meterage


# GIVENS

@given(u'all the users and passwords in plain text')
def step_impl(context):
    # getting users in database
    assert context.users['admin'] == 'default'
    assert context.users['hari'] == 'seldon'
	
@given(u'the admin is login')
def step_impl(context):
    """
    log in as admin
    """
    context.app.post('/login', data=dict(
        username='admin',
        #please refer to environment.py for users
        password=context.users['admin']
    ), follow_redirects=True)

    with context.app.session_transaction() as sess:
        # see http://flask.pocoo.org/docs/0.10/testing/#accessing-and-modifying-sessions for
        # an explanation of accessing sessions during testing.
        assert sess['logged_in'], "Admin is not logged in."

@given(u'the user knows the hashed value of their passwords')
def step_impl(context):
    # getting users in database
    context.hasheduser = meterage.User.query.all()
    assert context.hasheduser[0].username == 'admin'
    assert context.hasheduser[0].password != 'default'
    assert context.hasheduser[1].username == 'hari'
    assert context.hasheduser[1].password != 'seldon'

# WHENS

@when(u'we compare them with passwords stored in database')
def step_impl(context):
    context.userObjects = meterage.User.query.all()
    assert context.userObjects, 'there are no users'
    # comparison will be performed in the next step

@when(u'the admin changed a user password')
def step_impl(context):
    """
    change hari's password to 1234
    """
    context.rv = context.app.post('/change_password', data=dict(
        username='hari',
        password='1234',
        confirm_password='1234'
    ), follow_redirects=True)

    assert "Successfully changed user password" in context.rv.get_data(), print (context.rv.get_data())
    context.rv = context.app.get('/logout', follow_redirects=True)
    assert 'You were logged out' in context.rv.get_data()

@when(u'the user is trying to log in with hashed string')
def step_impl(context):
    pass

# THENS

@then(u'they should not be the same')
def step_impl(context):
    assert context.users['admin'] != context.userObjects[0].password
    assert context.users['hari'] != context.userObjects[1].password

@then(u'the user should not be able to log in with old password')
def step_impl(context):
    """
    log in as hari with old password
    """
    context.rv = context.app.post('/login', data=dict(
        username='hari',
        #please refer to environment.py for users
        password=context.users['hari']
    ), follow_redirects=True)
    assert "Invalid password" in context.rv.get_data()

@then(u'the user should not be able to log in')
def step_impl(context):
    """
    log in as hari with hashed string
    """
    context.rv = context.app.post('/login', data=dict(
        username='hari',
        #please refer to environment.py for users
        password=context.hasheduser[1].password
    ), follow_redirects=True)
    assert "Invalid password" in context.rv.get_data()
