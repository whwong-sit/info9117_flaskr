from behave import *
import meterage
from re import sub

#### GIVENS

#### WHENS

@when(u'the User navigates to the web interface')
def step_impl(context):
    """
    navigate to a page named /user/<username>
    """
    context.rv = context.app.get('/user/<username>')

    # assert that this page actually exists
    assert context.rv.status_code != 404, "'/user/<username>/' page does not exist; you're getting a 404 error"


#### THENS

@then(u'account details are displayed')
def step_impl(context):
    """
    Assert that information associated with the logged in user, including username and Gravatar email,
    is on the web interface page.
    """
    with context.app.session_transaction() as sess:
        # see http://flask.pocoo.org/docs/0.10/testing/#accessing-and-modifying-sessions for
        # an explanation of accessing sessions during testing.
        for detail in ["Username", sess['username'], "Gravatar Email", sess['gravataremail']]:
            # assert all these strings are present in rv.get_data() when stripped of HTML junk
            assert detail in sub('<[^>]*>', '', unicode(context.rv.get_data(), 'utf-8')), "{0} not displayed".format(
                detail)
            context.username = sess['username']


@then(u'the User is able to edit and commit {detail}')
def step_impl(context, detail):
    """
    POST a new value for {detail} to the change_{detail} page, then check if flaskr.USERS dicitonary
    has been updated appropriately.  Of all the methods written so far this is the least robust,
    as it only deals with usernames and passwords (not any other details associated with a user's account)
    and it is relying on usernames and passwords being in the flat little dictionary they are currently in.
    This is bound to be one of the first things to change.
    """
    # create the data to be sent in the POST to the user/<username>/ page's POST method

    if detail == "Gravatar email":
        data = dict(gravataremail="xXx_New_Detail_xXx", username="whatever", save="save")
    elif detail == "username":
        data = dict(gravataremail="doesntmatter@somethingelse.com", username="xXx_New_Detail_xXx", save="save")

    # This should take the new value of <detail> and put it through the
    # POST method of /users/<username>/
    rv = context.app.post('/user/<username>', data=data, follow_redirects=True)

    # this ensures that the session's username is still functioning
    context.execute_steps(u'''
        when the User navigates to the web interface
        then account details are displayed
    ''')

    with context.app.session_transaction() as sess:
        # see http://flask.pocoo.org/docs/0.10/testing/#accessing-and-modifying-sessions for
        # an explanation of accessing sessions during testing.
        allusers = meterage.User.query.all()
        assert allusers, "database tables have not been populated"
        for user in allusers:
            if user.username == sess['username']:
                if detail == 'Gravatar email':
                    assert data['gravataremail'] == user.gravataremail, 'new Gravatar email is not in the database'
                elif detail == 'username':
                    assert data[detail] == user.username, 'new username is not in the database'
