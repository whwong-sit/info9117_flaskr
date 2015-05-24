from behave import *
import meterage
from contextlib import closing
from datetime import *
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
    abort, render_template, flash
from jinja2 import Markup
from os.path import isfile
from flask_bcrypt import check_password_hash

from models import User

# GIVENS

@given(u'all the users and passwords in plain text')
def step_impl(context):
    # getting users in database
    with closing(meterage.connect_db()) as db:
        cur = db.execute('select username, password from userPassword')
        context.hasheduser = [dict(username=row[0], password=row[1]) for row in cur.fetchall()]
        assert context.hasheduser[0]['username']=='admin', print (context.hasheduser)
	
@given(u'the admin is login')
def step_impl(context):
    """
    log in as admin
    """
    context.app.post('/login', data=dict(
        username='admin',
        #please refer to environment.py for users
        password=context.users['admin']
    ), follow_redirects=True)

    with context.app.session_transaction() as sess:
        # see http://flask.pocoo.org/docs/0.10/testing/#accessing-and-modifying-sessions for
        # an explanation of accessing sessions during testing.
        assert sess['logged_in'], "Admin is not logged in."

@given(u'the user knows the hashed value of their passwords')
def step_impl(context):
    # getting users in database
    with closing(meterage.connect_db()) as db:
        cur = db.execute('select username, password from userPassword')
        context.hasheduser = [dict(username=row[0], password=row[1]) for row in cur.fetchall()]
        assert context.hasheduser[0]['username']=='admin', print (context.hasheduser)

# WHENS

@when(u'we compare them with passwords stored in database')
def step_impl(context):
    pass

@when(u'the admin changed a user password')
def step_impl(context):
    """
    change hari's password to 1234
    """
    context.rv = context.app.post('/change_password', data=dict(
        username='hari',
        password='1234',
        confirm_password='1234'
    ), follow_redirects=True)

    assert "Successfully changed user password" in context.rv.get_data(), print (context.rv.get_data())
    context.rv = context.app.get('/logout', follow_redirects=True)
    assert 'You were logged out' in context.rv.get_data()

@when(u'the user is trying to log in with hashed string')
def step_impl(context):
    pass

# THENS

@then(u'they should not be the same')
def step_impl(context):
    assert context.users['admin']!=context.hasheduser[0]['password']
    assert context.users['hari']!=context.hasheduser[1]['password']

@then(u'the user should not be able to log in with old password')
def step_impl(context):
    """
    log in as hari with old password
    """
    context.rv = context.app.post('/login', data=dict(
        username='hari',
        #please refer to environment.py for users
        password=context.users['hari']
    ), follow_redirects=True)
    assert "Invalid password" in context.rv.get_data()

@then(u'the user should not be able to log in')
def step_impl(context):
    """
    log in as hari with hashed string
    """
    context.rv = context.app.post('/login', data=dict(
        username='hari',
        #please refer to environment.py for users
        password=context.hasheduser[1]['password']
    ), follow_redirects=True)
    assert "Invalid password" in context.rv.get_data()
