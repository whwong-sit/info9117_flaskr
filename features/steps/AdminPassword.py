from behave import *
import meterage
from contextlib import closing


#### GIVENS

@given(u'admin has changed a user password')
def step_impl(context):

    context.execute_steps(u'''
        given the Admin is logged in
        when the Admin goes to change password
        and admin changes a user password
        then the password successfully changed
    ''')

#### WHENS

@when(u'the user login with old password')
def step_impl(context):
    context.app.post('/login', data=dict(
        username='hari',
        password='seldon'
    ), follow_redirects=True)

# assert rv. data password sucessfully change  (refer adminpassword unit test)
@when(u'the Admin goes to change password')
def step_impl(context):
    context.rv = context.app.get('/change_password')
    assert context.rv.status_code != 404, "change password page does not exist"

@when(u'admin changes a user password')
def step_impl(context):
    """
    POST a new password to the change_password page for the user hari
    """
    context.rv = context.app.post('/change_password', data=dict(
        username='hari',
        password='potter',
        confirm_password='potter'
    ), follow_redirects=True)

    assert 'Successfully changed user password' in context.rv.get_data()

@when(u'the Admin enters an invalid username')
def step_impl(context):
    """
    Admin enters a username of a non-existent user
    """
    context.rv = context.app.post('/change_password', data=dict(
        username='h',
        password='potter',
        confirm_password='potter'
    ), follow_redirects=True)

#### THENS

@then(u'the password successfully changed')
def step_impl(context):
    """
    Check in the database to see that the new value for the user's password is as it should be.
    """
    with closing(meterage.connect_db()) as db:
        cur = db.execute('select password from userPassword where username=?', ['hari'])
        assert len(cur.fetchall()) == 1, "username is not unique"
        for pw in [row[0] for row in cur.fetchall()]:
            assert pw == "potter", "Password has not been changed successfully"

@then(u'the change fails')
def step_impl(context):

    with closing(meterage.connect_db()) as db:
        cur = db.execute('select password from userPassword where username=?', ['h'])
        assert len(cur.fetchall()) == 0, "the username entered by the admin corresponds to a user in the database"

    errorstring = "<p class=error><strong>Error:</strong>User does not exist</p>"
    assert errorstring in context.rv.get_data(), "the error is not being displayed"

@then(u'user login fails')
def step_impl(context):

    # logout of Admin account
    context.app.get('/logout')

    # attempt a login as user 'hari'
    context.app.post('/login', data=dict(
        username='hari',
        password='seldon'
    ), follow_redirects=True)

    with context.app.session_transaction() as sess:
        assert 'logged_in' not in sess.keys(), "The user is able to log in"
