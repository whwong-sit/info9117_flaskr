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
    """
    Check in the database to see that the new value for the user's flag_admin is as it should be.
    """
    assert 'Successfully granted admin privileges to hari' in context.rv.get_data()
    assert meterage.User.query.filter_by(username='hari').first().admin, "User is not an admin"


@then(u'the add fails')
def step_impl(context):
    assert 'User jim does not exist' in context.rv.get_data()


@then(u'the revoke fails')
def step_impl(context):
    assert 'User is not an admin' in context.rv.get_data()
    """
    Check in the database to see that the value for the user's flag_admin is as it should be.
    """

    assert meterage.User.query.filter_by(username='hari').first().admin, 'user is not an admin'


@then(u'the admin is revoking privilege from another admin')
def step_impl(context):
    context.rv = context.app.post('/revoke_admin', data=dict(
        username='spock'
    ), follow_redirects=True)


@then(u'the revoke succeeds')
def step_impl(context):
    """
    Check in the database to see that the new value for the user's flag_admin is as it should be.
    """
    assert 'Successfully revoked admin privileges from spock' in context.rv.get_data()
    assert not meterage.User.query.filter_by(username='spock').first().admin, 'User is an admin'
