from behave import *
import meterage

# GIVENS

@given(u'a user is logged in')
def step_impl(context):
    """
    log in as user "hari"
    """
    context.app.post('/login', data=dict(
        username='hari',
        password='seldon'
    ), follow_redirects=True)

    with context.app.session_transaction() as sess:
        # see http://flask.pocoo.org/docs/0.10/testing/#accessing-and-modifying-sessions for
        # an explanation of accessing sessions during testing.
        assert sess['logged_in'], "The user is not logged in."

@given(u'a user can log in')
def step_impl(context):
    """
    log in as user "hari"
    """
    context.app.post('/login', data=dict(
        username='hari',
        password='seldon'
    ), follow_redirects=True)

    with context.app.session_transaction() as sess:
        # see http://flask.pocoo.org/docs/0.10/testing/#accessing-and-modifying-sessions for
        # an explanation of accessing sessions during testing.
        assert sess['logged_in'], "The user is not logged in."
    
    context.rv = context.app.get('/logout', follow_redirects=True)
    assert 'You were logged out' in context.rv.get_data()
	
@given(u'admin is logged in')
def step_impl(context):
    """
    log in as admin
    """
    context.app.post('/login', data=dict(
        username='admin',
        password='default'
    ), follow_redirects=True)

    with context.app.session_transaction() as sess:
        # see http://flask.pocoo.org/docs/0.10/testing/#accessing-and-modifying-sessions for
        # an explanation of accessing sessions during testing.
        assert sess['logged_in'], "The user is not logged in."
        assert sess['username']=='admin', "Admin is not logged in"

# WHENS

@when(u'the user is trying to access change password')
def step_impl(context):
    context.rv = context.app.get('/change_password',follow_redirects=True)

@when(u'admin is logged in')
def step_impl(context):
    """
    log in as admin
    """
    context.app.post('/login', data=dict(
        username='admin',
        password='default'
    ), follow_redirects=True)

    with context.app.session_transaction() as sess:
        # see http://flask.pocoo.org/docs/0.10/testing/#accessing-and-modifying-sessions for
        # an explanation of accessing sessions during testing.
        assert sess['logged_in'], "The user is not logged in."
        assert sess['username']=='admin', "Admin is not logged in"

@when(u'admin changes the password of this user')
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

@when(u'admin is trying to change password for a non-existing user')
def step_impl(context):
    """
    change a non-existing user password to 1234
    """
    context.rv = context.app.post('/change_password', data=dict(
        username='nonexist',
        password='1234',
        confirm_password='1234'
    ), follow_redirects=True)

# THENS

@then(u'the user should not be able to access it')
def step_impl(context):
    assert context.rv.status_code == 200, print(context.rv.status_code)


@then(u'once admin is logged in')
def step_impl(context):
    """
    log in as admin
    """
    context.app.post('/login', data=dict(
        username='admin',
        password='default'
    ), follow_redirects=True)

    with context.app.session_transaction() as sess:
        # see http://flask.pocoo.org/docs/0.10/testing/#accessing-and-modifying-sessions for
        # an explanation of accessing sessions during testing.
        assert sess['logged_in'], "The user is not logged in."
        assert sess['username']=='admin', "Admin is not logged in"

@then(u'admin should be able to access change password')
def step_impl(context):
    context.rv = context.app.get('/change_password', follow_redirects=True)
    assert context.rv.status_code != 404, "Admin cannot access change password"

@then(u'the user should not be able to log in with stale password')
def step_impl(context):
    """
    log in as user "hari" with stale password "seldon"
    """
    context.rv = context.app.post('/login', data=dict(
        username='hari',
        password='seldon'
    ), follow_redirects=True)

    assert "Invalid password" in context.rv.get_data()

@then(u'the change should fail')
def step_impl(context):
    assert "User does not exist" in context.rv.get_data(), print (context.rv.get_data())
    context.rv = context.app.get('/logout', follow_redirects=True)
    assert 'You were logged out' in context.rv.get_data()