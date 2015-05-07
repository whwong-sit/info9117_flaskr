from behave import *

#### GIVENS

@given(u'the User is logged in')
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

#### WHENS

@when(u'the User makes a post')
def step_impl(context):
    raise NotImplementedError(u'STEP: When the User makes a post')


#### THENS