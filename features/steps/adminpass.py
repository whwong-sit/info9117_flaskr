from behave import *
import meterage
from contextlib import closing


#### GIVENS

#### WHENS

@when(u'the user login with old password')
def step_impl(context):
    context.app.post('/login', data=dict(
        username='hari',
        password='seldon'
    ), follow_redirects=True)


@then(u'user login should fail')
def step_impl(context):
    with context.app.session_transaction() as sess:
     assert sess['logged_in'], "The user is not logged in."


@given(u'the Admin is logged in')
def step_impl(context):
    context.app.post('/login', data=dict(
        username='admin',
        password='default'
    ), follow_redirects=True)


@when(u'the Admin goes to change password')
def step_impl(context):
    context.rv = context.app.get('/change_password')
    assert context.rv.status_code != 404


@then(u'a changing password form is displayed')
def step_impl(context):

"""
 I am not sure about this~~~XD
"""
     with context.app.session_transaction() as sess:
        assert "Username: " + sess['username'] in context.rv.get_data(), "'Username: {0}' " \
                                                                         "is not on the page".format(sess['username'])
        assert "Password: " + sess['password'] in context.rv.get_data(), "Password: {0}' " \
                                                                         "is not on the page".format(sess['password'])
        assert "Confirm_Password: " + sess['confirm_password'] in context.rv.get_data(), "Confirm_Password: {0}' " \
                                                                         "is not on the page".format(sess['confirm_password'])


@when(u'the Username given does not exist')
def step_impl(context):
    with context.app.session_transaction() as sess:
        assert "Username: " + sess['username'] in context.rv.get_data(), "'Username: {0}' " \
                                                                         "is not on the page".format(sess['username'])


@then(u'the change should fail')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then the change should fail')
