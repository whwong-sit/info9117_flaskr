from behave import *
import meterage
from contextlib import closing


#### GIVENS

@Given(u'the user goes to register page')
def step_impl(context):
    context.rv = context.app.get('/register')
    assert context.rv.status_code != 404, "register page does not exist"
	
@Given(u'admin has approved a new user')
def step_impl(context):
	context.rv = context.app.get('/approve_new_user')
	assert context.rv.status_code != 404, "approve_new_user page does not exist"
	 
	context.rv = context.app.post('/approve_new_user', data=dict(
        username='jim1'
		), follow_redirects=True)
		

@Given(u'a user registration without permission')
def step_impl(context):
    """
    Check in the database to see that the new value for the user's password is as it should be.
    """
	
    with closing(meterage.connect_db()) as db:
        cur = db.execute('select flag_approval from userPassword where username=?', ['jim'])
        for ap in [row[0] for row in cur.fetchall()]:
            assert ap == False, "Successfully grant access to user"
	
	
#### WHENS
@when(u'the user is logged in')
def step_impl(context):
    context.app.post('/login', data=dict(
        username='jim',
        password='bean'
    ), follow_redirects=True)

	

	
@when(u'the user register')
def step_impl(context):
  
    context.rv = context.app.post('/register',data=dict(
           username='jim',
           password='bean',
		   confirm_password='bean',
		   email='jimbean1@whisky.biz'
        ), follow_redirects=True)
    
	


  
	

@when(u'the Admin goes to adding_new_user page')
def step_impl(context):
    context.rv = context.app.get('/add_new_user')
    assert context.rv.status_code != 404, "add_new_user page does not exist"
	

	
@when(u'the Admin add new user for login')
def step_impl(context):
    """
    POST a new password to the change_password page for the user hari
    """
    context.rv = context.app.post('/add_new_user', data=dict(
        username='test1',
        password='test',
		confirm_password='test',
		email='test1@test1.com'
    ), follow_redirects=True)



	

	
	
	
####THENS
@then(u'registration performed successfully')
def step_impl(context):
  assert 'Successfully registered' in context.rv.get_data()


@then(u'the user login successfully')
def step_impl(context):

    # logout of Admin account
   context.app.get('/logout')
  
   context.app.post('/login', data=dict(
        username='jim1',
        password='bean1'
    ), follow_redirects=True)
   with context.app.session_transaction() as sess:
      assert 'logged_in' not in sess.keys(), "The user is able to log in"
	   
	   
@then(u'the user login fails')
def step_impl(context):

    # logout of Admin account
   context.app.get('/logout')
   
   context.app.post('/login', data=dict(
        username='jim1',
        password='bean1'
    ), follow_redirects=True)
   with context.app.session_transaction() as sess:
      assert 'logged_in' not in sess.keys(), "The user is able to log in"
				
@then(u'adding new user performed successfully')
def step_impl(context):
  assert 'Successfully added new user' in context.rv.get_data()

