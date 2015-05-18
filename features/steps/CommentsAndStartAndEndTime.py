from behave import *
from time import gmtime, strftime
# import meterage

# GIVENS

@given(u'the user has logged in already')
def step_impl(context):
    context.app.post('/login', data=dict(
            username='admin',
            password='default'
        ), follow_redirects=True)

# WHENS

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
