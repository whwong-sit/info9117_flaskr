from behave import *
import meterage
from contextlib import closing


#### GIVENS
# Given the admin is logged in
# See genericsteps.py


#### WHENS

@when(u'the Admin grant admin privilege to an existing user')
def step_impl(context):
    context.rv = context.app.post('/add_new_admin', data=dict(
        username='hari',
    ), follow_redirects=True)

@when(u'the Admin enters an invalid admin name')
def step_impl(context):
    context.rv = context.app.post('/add_new_admin', data=dict(
        username='jim'
    ), follow_redirects=True)

@when(u'the admin is revoking privilege from a normal user')
def step_impl(context):
    context.rv = context.app.post('/revoke_admin', data=dict(
        username='test'
    ), follow_redirects=True)

#### THENS

@then(u'the user become an admin successfully')
def step_impl(context):
    assert 'Successfully granted admin privilege to user' in context.rv.get_data()
    """
    Check in the database to see that the new value for the user's flag_admin is as it should be.
    """
    with closing(meterage.connect_db()) as db:
        cur = db.execute('select flag_admin from userPassword where username=?', ['hari'])
        row = cur.fetchone()
        assert row[0] == 1, "User is not an admin"

@then(u'the add fails')
def step_impl(context):
    assert 'User does not exist' in context.rv.get_data()

@then(u'the revoke fails')
def step_impl(context):
    assert 'User is not an admin' in context.rv.get_data()
    """
    Check in the database to see that the value for the user's flag_admin is as it should be.
    """
    with closing(meterage.connect_db()) as db:
        cur = db.execute('select flag_admin from userPassword where username=?', ['test'])
        row = cur.fetchone()
        assert row[0] == 0, "User is an admin"

@then(u'the admin is revoking privilege from another admin')
def step_impl(context):
    context.rv = context.app.post('/revoke_admin', data=dict(
        username='spock'
    ), follow_redirects=True)

@then(u'the revoke succeeds')
def step_impl(context):
    assert 'Successfully revoked admin privilege from user' in context.rv.get_data()
    """
    Check in the database to see that the new value for the user's flag_admin is as it should be.
    """
    with closing(meterage.connect_db()) as db:
        cur = db.execute('select flag_admin from userPassword where username=?', ['spock'])
        row = cur.fetchone()
        assert row[0] == 0, "User is an admin"
