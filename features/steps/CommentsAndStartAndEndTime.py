from behave import *
import datetime
# import meterage

# WHENS



@when(u'the user adds a new entry to log with an unspecified start time')
def step_impl(context):
    context.rv = context.app.post('/add', data=dict(
        title='<Hello>',
        text='<strong>HTML</strong> allowed here',
        start_time='',
        task_des=''
    ), follow_redirects=True)


@when(u'click the entry, the user would be able to add a comment each time')
def step_impl(context):
    context.rv = context.app.post('/1/add_comments', data=dict(
        comment_input='<FinalVERSION>'
    ), follow_redirects=True)


@when(u'the user presses end_task')
def step_impl(context):
    context.rv = context.app.post('/1/add_end_time', follow_redirects=True)

# THENS

@then(u'the comment should appear right after added')
def step_impl(context):
    assert '&lt;FinalVERSION&gt;' in context.rv.get_data()

@then(u'the username should displayed right next to the comment')
def step_impl(context):
    assert 'by hari' in context.rv.get_data()

@then(u'time will auto sign')
def step_impl(context):
    curr_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    assert curr_time in context.rv.get_data()
