from flask import request, redirect, url_for, abort, render_template, flash
from jinja2 import Markup
from flask_bcrypt import check_password_hash
from flask_gravatar import Gravatar

import datetime

from . import *


@app.route('/')
def show_entries():
    """
    Get all the information required in show_entries.html from the database and pipe it
    into show_entries.html
    """
    return render_template('show_entries.html', entries=Entry.query.order_by(-Entry.id).all())


@app.route('/add', methods=['POST'])
def add_entry():

    if not session.get('logged_in'):
        abort(401)

    if request.form['start_time'] == '':
        # use the default time (current time)
        db.session.add(Entry(request.form['title'], request.form['text'], session['uid'], None,
                             request.form['end_time']))
    else:
        db.session.add(Entry(request.form['title'], request.form['text'], session['uid'], request.form['start_time'],
                             request.form['end_time']))
    db.session.commit()

    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Check to see if the entered username is in the database.  If no, present an error.
    If the username is present in the database, check that the given password corresponds
    to the given username.  If so, log in, otherwise present an error.
    """
    error = None
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()

        if user is not None:
            # if the user is found
            if not check_password_hash(user.password, request.form['password']):
                # if the password hash in the database does not correspond to the hashed form of the given password
                error = 'Invalid password'
            else:
                session['logged_in'] = True
                session['username'] = user.username
                session['gravataremail'] = user.gravataremail
                session['uid'] = user.id
                session['admin'] = user.admin
                flash('You were logged in')
                return redirect(url_for('show_entries'))
        else:
            error = 'Invalid username'
    return render_template('login.html', error=error)


@app.route('/<entry_id>/show_comments')
def show_comments(entry_id):
    comments = Comment.query.filter_by(entry_id=entry_id).order_by(-Comment.id).all()
    entry = Entry.query.get(entry_id)
    return render_template('show_comments.html', entry=entry, comments=comments, entry_id=entry_id)

@app.route('/<entry_id>/add_comments', methods=['POST'])
def add_comments(entry_id):
    if not session.get('logged_in'):
        abort(401)

    db.session.add(Comment(session['uid'], request.form['comment_input'], entry_id))
    db.session.commit()
    flash('New comment was successfully posted')
    return redirect(url_for('show_comments', entry_id=entry_id))


@app.route('/<entry_id>/add_end_time', methods=['POST'])
def add_end_time(entry_id):
    if not session.get('logged_in'):
        abort(401)
    # if end_time_null_check is True:
    entry = Entry.query.filter_by(id=entry_id).first()
    entry.end_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    db.session.commit()
    flash('TASK ENDED')
    return redirect(url_for('show_comments', entry_id=entry_id))


@app.route('/<entry_id>/end_time_null_check')
def end_time_null_check(entry_id):  # need to debug
    entry = Entry.query.filter_by(id=entry_id).get()
    if entry.endtime is None:
        return True
    else:
        return False


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))


@app.route('/user/<username>', methods=['GET', 'POST'])
def manage_details(username):
    """
    Allow for a user to change their username and Gravatar email.  When more details are added, this
    will be updated
    :param username: the current user's username
    :return: manage_details
    """

    if not session.get('logged_in'):
        abort(401)

    if 'save' in request.form.keys():
        # this also necessarily means that we are dealing with a POST request
        if request.form['username'] in ['', None]:
            # TODO Check that username is unique
            flash('Username must not be empty')
        else:
            user = User.query.get(session['uid'])
            user.username, user.gravataremail = request.form['username'], request.form['gravataremail']
            db.session.commit()
            session['username'], session['gravataremail'] = request.form['username'], request.form['gravataremail']
            flash('Successfully changed user details')
    return render_template('manage_details.html')


@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    """
    Allows the admin to change the password of a user.  It searches the database for the user specified.
    If that user is present, it checks that the new password is not empty and that the new password
    corresponds to the confirmation password given.  If all of this holds, then the user's password
    is updated.
    """
    error = None
    if not session.get('logged_in'):
        # If someone tries to access the page without being logged in.
        abort(401)
    if request.method == 'POST':
        
        user = User.query.filter_by(username=request.form['username']).first()

        if user is None:
            error = 'User does not exist'
        elif request.form['password'] is None or request.form['password'] == '':
            error = 'Empty password'
        elif request.form['password'] != request.form['confirm_password']:
            error = 'Please enter same password twice'
        else:
            user.password = request.form['password']
            db.session.commit()
            flash('Successfully changed user password')
            return render_template('change_password.html', success='Successfully changed password')

    return render_template('change_password.html', error=error)


@app.template_filter('newlines')
def newline_filter(s):
    s = s.replace("\r\n", '<br />')
    s = s.replace("\n", '<br />')
    # Markup() is used to prevent '<' and '>' symbols from being interpreted as less-than or greater-than symbols
    return Markup(s)

@app.template_filter('timestamp')
def timestamp_filter(s):
    if isinstance(s, datetime.datetime):
        # return time.strftime("%Y-%m-%d %H:%M:%S", s.time())
        return s.strftime("%Y-%m-%d %H:%M:%S")

# This is a Gravatar object, used by Flask-Gravatar extension as a filter in templates
gravatar = Gravatar(app,
                    size=50,
                    rating='g',
                    default='retro',
                    force_default=False,
                    force_lower=False,
                    use_ssl=False,
                    base_url=None)
