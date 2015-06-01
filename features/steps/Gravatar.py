from behave import *
from contextlib import closing
import meterage
from datetime import *

#### GIVENS


#### WHENS

@when(u'the User removes their Gravatar assignment')
def step_impl(context):
    """
    User changes their Gravatar email to an empty string
    :param context: behave context object
    """

    # TODO implement the Gravatar removal such that rhe user does not have to enter an empty string
    # TODO but can instead elect whether or not to show the Gravatar.  This is more of a "setting"

    with context.app.session_transaction() as sess:
        # see http://flask.pocoo.org/docs/0.10/testing/#accessing-and-modifying-sessions for
        # an explanation of accessing sessions during testing.
        context.app.post('/user/<username', data=dict(gravataremail="", username=sess['username'], save="save"),
                         follow_redirects=True)
        with closing(meterage.connect_db()) as db:
            cur = db.execute('select gravataremail from userPassword where username=?', [sess['username']])
            rows = [dict(gravataremail=row[0]) for row in cur.fetchall()]
            assert rows, "userPassword table has not been populated"
            assert len(rows) == 1, "There is more than one user with the logged in username."
            assert rows[0]["gravataremail"] == "", "Gravatar email has not been removed"

#### THENS

@then(u'the Gravatar is displayed alongside the post')
def step_impl(context):
    gravatar = '"http://www.gravatar.com/avatar/cf2ee704bb2c7ebc4884b06c45f703fb?s=50&amp;d=monsterid"'
    assert gravatar in context.rv.get_data(), "image is not being displayed"

@then(u'their Gravatar is no longer displayed beside posts')
def step_impl(context):
    gravatar = "<li><h2><i><img src=\"http://www.gravatar.com/avatar/cf2ee704bb2c7ebc4884b06c45f703fb?" \
                           "s=50&amp;d=monsterid\"></i><br>&lt;Hello&gt; <span class=user> by hari </span>"
    assert gravatar not in context.rv.get_data(), "image is still being displayed"
