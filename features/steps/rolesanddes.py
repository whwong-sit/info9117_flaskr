

__author__ = 'LEILEILEILEIL'


from behave import *
from datetime import *



@when(u'the user adds a new entry with task description')
def step_impl(context):
 context.rv = context.app.post('/add', data=dict(
        title='<Hello>',
        text='<strong>HTML</strong> allowed here',
        start_time='',
        task_des='fathima'
    ), follow_redirects=True)

@then(u'Task Description will displayed')
def step_impl(context):
    assert 'fathima' in context.rv.get_data()

@when(u'add the entry, the user would be able to assign user role to the entry')
def step_impl(context):

    context.app.post('/add', data=dict(
        title='<Hello>',
        text='<strong>HTML</strong> allowed here',
        start_time='',
        task_des='fathima'
    ), follow_redirects=True)

    context.rv=context.app.post('/1/add_roles', data=dict(
            user_role='<fathima>',
            ), follow_redirects=True)

@then(u'the user role should be displayed on the comments page')
def step_impl(context):

    assert '&lt;fathima&gt;' in context.rv.data