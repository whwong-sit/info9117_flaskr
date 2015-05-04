from behave import *



@given('the user is logged in')
def step_impl(context):
    rv = context.login('admin', 'default')
    assert 'You were logged in' in rv.data

@when('create a entry')
def step_impl(context):
    context.app.post('/add', data=dict(
            title='Hi',
            text='<strong>HTML</strong> allowed here'
        ), follow_redirects=True)

@when('click add_comment')
def step_impl(context):
    rv = context.app.post('/1/add_comments', data= dict(
            comment_input = '<FinalVERSION>'
        ), follow_redirects=True)
    return rv

@when('press end_task')
def step_impl(context):
    rv = context.app.post('/1/add_end_time', follow_redirects=True)
    return rv



@then('the comment should appear')
def step_impl(rv):
    assert '&lt;FinalVERSION&gt;' in rv.data

@then('start time will auto_sign')
def step_impl(rv):
    from time import gmtime, strftime
    curr_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    assert curr_time in rv.data

@then('end time should auto_sign')
def step_impl(rv):
    from time import gmtime, strftime
    curr_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    assert 'End at: '+ curr_time in rv.data