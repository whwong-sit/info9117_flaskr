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

    e = Entry(request.form['title'], request.form['text'], session['uid'], None, None, request.form['task_des'])

    if request.form['start_time'] not in ['', None]:
        e.start_time = request.form['start_time']

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
            if not check_password_hash(user.password, request.form['password']):
                # if the password hash in the database does not correspond to the hashed form of the given password
                error = 'Invalid password'
            elif not user.approved:
                error = 'Please contact an admin for access permission'
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

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    session.pop('admin', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))

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

@app.route('/<entry_id>/add_roles', methods=['POST'])
def add_roles(entry_id):
    if not session.get('logged_in'):
        abort(401)

    e = Entry.query.get(entry_id)
    e.user_role = request.form['user_role']
    db.session.commit()
        
    flash('New role was successfully posted')
    return redirect(url_for('show_comments', entry_id=entry_id))

@app.route('/<entry_id>/delete_roles', methods=['POST'])
def delete_roles(entry_id):
    if not session.get('logged_in'):
        abort(401)

    e = Entry.query.get(entry_id)
    e.user_role = None
    db.session.commit()

    flash('Role has been reset')
    return redirect(url_for('show_comments', entry_id=entry_id))

@app.route('/<entry_id>/add_end_time', methods=['POST'])
def add_end_time(entry_id):
    if not session.get('logged_in'):
        abort(401)
    
    e = Entry.query.filter_by(id=entry_id).first()
    if e.end_time is None:
        e.end_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        db.session.commit()
        flash('TASK ENDED')
    else:
        flash('TASK ALREADY ENDED')
    return redirect(url_for('show_comments', entry_id=entry_id))

@app.route('/user/<username>', methods=['GET', 'POST'])
def manage_details(username):
    """
    Allow for a user to change their username and Gravatar email.  When more details are added, this
    will be updated
    :param username: the current user's username
    :return: manage_details
    """

    error = None

    if not session.get('logged_in'):
        abort(401)

    if 'save' in request.form.keys():
        # this also necessarily means that we are dealing with a POST request
        if request.form['username'] in ['', None]:
            flash('Username must not be empty')
        else:
            user = User.query.get(session['uid'])
            try:
                user.username, user.gravataremail = request.form['username'], request.form['gravataremail']
                db.session.commit()
                session['username'], session['gravataremail'] = request.form['username'], request.form['gravataremail']
                flash('Successfully changed user details')
            except:
                error = 'That username is taken already'

    return render_template('manage_details.html', error=error)

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

@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    Allows new user to register for log in. If the username input already exists,
    new user has to register again with a different username. If that user is not present,
    it checks that the password corresponds to the confirmation password given.
    If all of this holds, then the new user is created.
    """
    error = None
    if request.method == 'POST':
        try :
            if request.form['password'] == request.form['confirm_password']:
                db.session.add(User(request.form['username'], request.form['password'], request.form['email'], False, False))
                db.session.commit()
                flash('Successfully registered')
            else:
                error = 'Please enter the same password twice'
        except : # SQL exception for not having a unique username
            error = 'Username has already been used'
            
    return render_template('register.html', error=error)

@app.route('/admin', methods=['GET'])
def admin():
    """
    Redirect admin to admin portal page
    """
    if not session.get('logged_in'):
        # If someone tries to access the page without being logged in.
        abort(401)
    return render_template('admin.html')

@app.route('/add_new_user', methods=['GET', 'POST'])
def add_new_user():
    """
    Allows the admin to add a new user.  It searches the database for the user specified.
    If that user is not present, the new user is created.
    """
    # TODO consolidate this into the register method
    error = None
    if not session.get('logged_in'):
        # If someone tries to access the page without being logged in.
        abort(401)

    if request.method == 'POST':
        try :
            if request.form['password'] == request.form['confirm_password']:
                db.session.add(User(request.form['username'], request.form['password'], request.form['email'], False, True))
                db.session.commit()
                flash('Successfully added new user')
            else:
                error = 'Please enter the same password twice'
        except : # SQL exception for not having a unique username
            error = 'Username has already been used'
            
    return render_template('add_new_user.html', error=error)            

@app.route('/approve_new_user', methods=['GET', 'POST'])
def approve_new_user():
    """
    Allows the admin to grant access to a new user.  It searches the database for the user specified.
    If that user is present, the new user is granted with access.
    """
    error = None
    if not session.get('logged_in'):
        # If someone tries to access the page without being logged in.
        abort(401)

    if request.method == 'POST':
        e = User.query.filter_by(username=request.form['username'].first())
        if e is not None:
            e.approved = True
            db.session.commit()
            flash('Successfull granted access to ' + request.form['username'])
        else:
            error = 'No such user as ' + request.form['username']
            
    return render_template('approve_new_user.html', error=error)

@app.route('/add_new_admin', methods=['GET', 'POST'])
def add_new_admin():
    """
    Allows the admin to grant admin privilege to another non-admin user. It searches the database for the user specified.
    If that user is present and non-admin, the user is granted with admin privilege.
    """
    error = None
    if not session.get('logged_in'):
        # If someone tries to access the page without being logged in.
        abort(401)
    if not session.get('admin'):
        # If non-admin tries to access the page
        abort(401)
    if request.method == 'POST':
        try:
            u = User.query.filter_by(username=request.form['username']).first()
            if u.admin :
                error = 'User is already an admin'
            else:
               u.admin = True
               db.session.commit()
               flash('Successfully granted admin privilege to user')
        except :
            error = 'User does not exist'
             
    return render_template('add_new_admin.html', error=error)

@app.route('/revoke_admin', methods=['GET', 'POST'])
def revoke_admin():
    """
    Allows the admin to revoke admin privilege from another user. It searches the database for the user specified.
    If that user is present, the user's admin privilege is revoke. However, users with admin privilege cannot revoke their own privilege.
    """
    error = None
    if not session.get('logged_in'):
        # If someone tries to access the page without being logged in.
        abort(401)
    if not session.get('admin'):
        # If non-admin tries to access the page
        abort(401)
    if request.method == 'POST':
        try:
            u = User.query.filter_by(username=request.form['username']).first()
            if u.username == session['username']:
                error = "You can't revoke your own admin rights!"
            elif not u.admin :
                error = 'User is not an admin'
            else:
               u.admin = False
               db.session.commit()
               flash('Successfully removed admin privileges')
        except :
            error = 'User does not exist'
    
    return render_template('revoke_admin.html', error=error)
    

#####################################
#### Filters and other functions ####
#####################################

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
