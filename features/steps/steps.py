from behave import *
from time import gmtime, strftime
import meterage

# GIVENS

@given(u'the User is logged in')
def step_impl(context):
    """
    log in as user "jim"
    """
    context.app.post('/login', data=dict(
        username='hari',
        password='seldon'
    ), follow_redirects=True)

    with context.app.session_transaction() as sess:
        # see http://flask.pocoo.org/docs/0.10/testing/#accessing-and-modifying-sessions for
        # an explanation of accessing sessions during testing.
        assert sess['logged_in'], "The user is not logged in."


@given(u'the user has logged in already')
def step_impl(context):
    context.app.post('/login', data=dict(
            username='admin',
            password='default'
        ), follow_redirects=True)

# WHENS

@when(u'the User navigates to the web interface')
def step_impl(context):
    """
    navigate to a page named /user/<username>
    """
    context.rv = context.app.get('/user/<username>')

    # assert that this page actually exists
    assert context.rv.status_code != 404, "'/user/<username>/' page does not exist; you're getting a 404 error"


@when(u'the User clicks "change {detail}"')
def step_impl(context, detail):
    """
    Check that detail is on this page, and then go to the page to change <detail>
    """
    # assert that <detail> is on the current page.
    assert detail in context.rv.get_data(), "{0} is not on the current page".format(detail)

    # GET the page to change <detail>
    context.rv = context.app.get('/users/<username>/change_{0}'.format(detail))


@when(u'the user add a new entry to log')
def step_impl(context):
    # note that this is a post *with no start time specified*
    rv = context.app.post('/add', data=dict(
        title='<Hello>',
        text='<strong>HTML</strong> allowed here',
        sdate='2015-01-01',
        # start_time='<15:00>',
        start_time='',
        edate='2015-01-02',
        end_time='<17:30>'
    ), follow_redirects=True)
    context.response = rv


@when(u'click the entry, the user would be able to add a comment each time')
def step_impl(context):
    cv = context.app.post('/1/add_comments', data=dict(
        comment_input='<FinalVERSION>'
    ), follow_redirects=True)
    context.response = cv


@when(u'the user presses end_task')
def step_impl(context):
    rv = context.app.post('/1/add_end_time', follow_redirects=True)
    context.response=rv


# THENS

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
        assert "Username: " + sess['username'] in context.rv.get_data(), "'Username: {0}' " \
                                                                         "is not on the page".format(sess['username'])


@then(u'the User is able to edit and commit {detail}')
def step_impl(context, detail):
    """
    POST a new value for {detail} to the change_{detail} page, then check if flaskr.USERS dicitonary
    has been updated appropriately.  Of all the methods written so far this is the least robust,
    as it only deals with usernames and passwords (not any other details associated with a user's account)
    and it is relying on usernames and passwords being in the flat little dictionary they are currently in.
    This is bound to be one of the first things to change.
    """
    # create the data to be sent in the POST to the change_{detail} page's POST method
    data = {detail: "xXx_New_Detail_xXx"}

    # This should take the new value of <detail> and put it through the
    # POST method of /users/<username>/change_{detail}
    context.app.post('/users/<username>/change_{0}'.format(detail), data=data, follow_redirects=True)

    # this ensures that the session's username is still functioning
    context.execute_steps(u'''
        when the User navigates to the web interface
        then account details are displayed
    ''')

    # TODO this needs to be made more robust, as at the moment it only deals with the flat dictionary
    # TODO mapping usernames to passwords; this is bound to soon change to a proper database implementation
    if detail == "password":
        assert data[detail] in meterage.USERS.values(), "new password is not in the USERS dictionary"
    elif detail == "username":
        assert data[detail] in meterage.USERS.keys(), "new username is not in the USERS dictionary"


@then(u'the comment should appear right after added')
def step_impl(context):
    assert '&lt;FinalVERSION&gt;' in context.response.get_data()


@then(u'the username should displayed right next to the comment')
def step_impl(context):
    assert 'by admin' in context.response.get_data()


@then(u'start time will auto sign')
def step_impl(context):
    print(context.response.get_data())
    assert strftime("%Y-%m-%d %H:%M", gmtime()) in context.response.get_data()


@then(u'end time should auto sign')
def step_impl(context):
    assert 'End at: '+ strftime("%Y-%m-%d %H:%M:%S", gmtime()) in context.response.get_data()
