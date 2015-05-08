from behave import *
import meterage
from contextlib import closing


#### GIVENS
@given(u'admin has changed a user password')
def step_impl(context):
    context.rv = context.app.post('/change_password', data=dict(
        username='harri',
        password='potter',
        confirm_password='potter'
    ), follow_redirects=True)


    for s in ['harri','potter', 'potter']:
        assert s in context.rv.get_data()
    with context.app.session_transaction() as sess:
        assert sess['username'] in context.rv.get_data()

    with closing(meterage.connect_db()) as db:
        cur = db.execute('select username, password from userPassword')
        return [dict(username=row[0], password=row[1]) for row in cur.fetchall()]



@given(u'the Admin is logged in')
def step_impl(context):
    context.app.post('/login', data=dict(
        username='admin',
        password='default'
    ), follow_redirects=True)




@when(u'the user login with old password')
def step_impl(context):
    context.app.post('/login', data=dict(
        username='hari',
        password='seldon'
    ), follow_redirects=True)


@then(u'user login should fail')
def step_impl(context):
    with context.app.session_transaction() as sess:
        assert sess['logged_in'], "The user is not logged in."


# assert rv. data password sucessfully change  (refer adminpassword unit test)
@when(u'the Admin goes to change password')
def step_impl(context):
    context.rv = context.app.get('/change_password')
    assert context.rv.status_code != 404




@when(u'admin change  a user password')
def step_impl(context):
    context.rv = context.app.post('/change_password', data=dict(
        username='harri',
        password='potter',
        confirm_password='potter'
    ), follow_redirects=True)


    for s in ['harri','potter', 'potter']:
        assert s in context.rv.get_data()

    with context.app.session_transaction() as sess:
        assert sess['username'] in context.rv.get_data()
        assert 'Successfully changed user password' in context.rv.data.get_data()



@then(u'the password successfully changed')
def step_impl(context):
    with closing(meterage.connect_db()) as db:
        cur = db.execute('select username, password from userPassword')
        return [dict(username=row[0], password=row[1]) for row in cur.fetchall()]
        assert 'Successfully changed user password' in context.rv.data.get_data()

@when(u'admin change  a user password with invalid username')
def step_impl(context):

    context.rv = context.app.post('/change_password', data=dict(
        username='h',
        password='potter',
        confirm_password='potter'
    ), follow_redirects=True)


    for s in ['h','potter', 'potter']:
        assert s in context.rv.get_data()
    with context.app.session_transaction() as sess:
        assert sess['username'] in context.rv.get_data()
    with closing(meterage.connect_db()) as db:
        cur = db.execute('select username, password from userPassword')
        return [dict(username=row[0], password=row[1]) for row in cur.fetchall()]
        assert 'Invalid username' in context.rv.data.get_data()




@then(u'the change should fail')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then the change should fail')
