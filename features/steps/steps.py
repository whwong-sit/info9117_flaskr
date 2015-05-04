from behave import *


@given('the user is logged in')
def step_impl(context):
    context.app.post('/login', data=dict(
            username='admin',
            password='default'
        ), follow_redirects=True)

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
    context.response = rv

@then('the comment should appear')
def step_impl(context):
    assert '&lt;FinalVERSION&gt;' in context.response.data

@then('the comment should note username')
def step_impl(context):
    assert 'by admin' in context.response.data

@when('press end_task')
def step_impl(context):
    rv = context.app.post('/1/add_end_time', follow_redirects=True)
    return rv




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

