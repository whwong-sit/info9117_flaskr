from behave import *

##### GIVENS

@given(u'the User is logged in')
def step_impl(context):
    """
    log in as user "jim"
    """
    context.app.post('/login', data=dict(
        username='jim',
        password='bean'
    ), follow_redirects=True)


##### WHENS

@when(u'the User navigates to the web interface')
def step_impl(context):
    """
    navigate to a page named /user/<username>
    """
    context.rv = context.app.get('/user/<username>')


@when(u'the User clicks "change username"')
def step_impl(context):
    raise NotImplementedError(u'STEP: When the User clicks "change username"')


@when(u'the User clicks "change password"')
def step_impl(context):
    raise NotImplementedError(u'STEP: When the User clicks "change password"')


#### THENS

@then(u'account details are displayed')
def step_impl(context):
    """
    Assert that the string "Username: <username>" is present somewhere in rv.get_data()

    We also need to assert that any other information associated with a user is displayed on the page;
    at the moment, the only thing associated with a user is their username (and also their posts, but this
    is not perhaps what we might display on the account settings page)
    """
    with context.app.session_transaction() as sess:
        # see http://flask.pocoo.org/docs/0.10/testing/#accessing-and-modifying-sessions for
        # an explanation of accessing sessions during testing.
        assert "Username: " + sess['username'] in context.rv.get_data()


@then(u'the User is able to edit username')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then the User is able to edit username')


@then(u'the User is able to commit the new value successfully')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then the User is able to commit the new value successfully')


@then(u'the User is able to edit password')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then the User is able to edit password')


