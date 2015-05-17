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
    """
    make a generic post
    """
    context.rv = context.app.post('/add', data=dict(
        title='<Hello>',
        text='<strong>HTML</strong> allowed here',
        sdate='2015-01-01',
        stime='09:00:00',
        edate='2015-01-02',
        etime='13:00:00'
    ), follow_redirects=True)

    for s in ['&lt;Hello&gt;', '2015-01-01', '09:00:00', '2015-01-02', '13:00:00',
              '<strong>HTML</strong> allowed here']:
        assert s in context.rv.get_data()
    assert 'No entries here so far' not in context.rv.get_data()
    with context.app.session_transaction() as sess:
        # see http://flask.pocoo.org/docs/0.10/testing/#accessing-and-modifying-sessions for
        # an explanation of accessing sessions during testing.
        assert sess['username'] in context.rv.get_data()

#### THENS
