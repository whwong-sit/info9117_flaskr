from behave import *


@given('the user has logged in already')
def step_impl(context):
    context.app.post('/login', data=dict(
            username='admin',
            password='default'
        ), follow_redirects=True)


@when('the user add a new entry to log')
def step_impl(context):
    rv = context.app.post('/add', data=dict(
            title='Hi',
            text='<strong>HTML</strong> allowed here'
        ), follow_redirects=True)
    context.response = rv

@when('click the entry, the user would be able to add a comment each time')
def step_impl(context):
    cv = context.app.post('/1/add_comments', data= dict(
            comment_input = '<FinalVERSION>'
        ), follow_redirects=True)
    context.response = cv


@then('the comment should appear right after added')
def step_impl(context):
    assert '&lt;FinalVERSION&gt;' in context.response.data


@then('the username should displayed right next to the comment')
def step_impl(context):
    assert 'by admin' in context.response.data


@when('the user press end_task')
def step_impl(context):
    rv = context.app.post('/1/add_end_time', follow_redirects=True)
    context.response=rv


@then('start time will auto_sign')
def step_impl(context):
    from time import gmtime, strftime
    curr_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    assert curr_time in context.response.data


@then('end time should auto_sign')
def step_impl(context):
    from time import gmtime, strftime
    curr_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    assert 'End at: '+ curr_time in context.response.data

