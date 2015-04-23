from behave import *

@given('we have behave installed')
def step_impl(context):
    pass

@when('we implement a test')
def step_impl(context):
    assert True is not False

@then('behave will test it for us!')
def step_impl(context):
    assert context.failed is False




@given(u'the User is logged in')
def step_impl(context):
    """
    Admin login to the /login_admin page and changing the password of jim
    """
    context.app.post('/login_admin', data=dict(
        username='jim',
        passwordtochange='1234'
    ), follow_redirects=True)

    with context.app.session_transaction() as sess:
        assert sess['changing jim password']





@given(u'the User is logged in')
def step_impl(context):
    """
     try to login with the old password - this should fail.
    """
    context.app.post('/login', data=dict(
        username='jim',
        password='bean'
    ), follow_redirects=True)

    with context.app.session_transaction() as sess:
        assert sess['logged_in_fail']



@given(u'the User is logged in')
def step_impl(context):
    """
   Then try to login with the new password - this should pass.
    """
    context.app.post('/login', data=dict(
        username='jim',
        password='1234'
    ), follow_redirects=True)

    with context.app.session_transaction() as sess:
        assert sess['logged_in_pass']
