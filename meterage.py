import urllib
import hashlib
from contextlib import closing
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
    abort, render_template, flash
from jinja2 import Markup
from os.path import isfile
from flask_bcrypt import check_password_hash
from models import User

import config

# create application
app = Flask(__name__, instance_relative_config=True)
app.config.from_object(config)
app.config.from_pyfile('config.py')
app.config.from_envvar('FLASKR_SETTINGS', silent=True)


def connect_db():
    """
    Make a connection to the database

    database specified in the config.
    """
    return sqlite3.connect(app.config['DATABASE'])


def init_db():
    """
    For initialising the database using schemal.sql.

    This is usually called manually.
    """
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


def avatar(email, size=50):
    """
    generate gravatar url from email

    :param email: email address for gravatar
    :param size: size of the image, deafaults to 50
    :return: url of gravatar
    """
    gravatar_url = "http://www.gravatar.com/avatar/" + hashlib.md5(email.lower()).hexdigest()+"?"
    gravatar_url += urllib.urlencode({'d':"monsterid",'s':str(size)})
    return gravatar_url

@app.before_request
def before_request():
    g.db = connect_db()


@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


@app.route('/')
def show_entries():
    """
    Get all the information required in show_entries.html from the database and pipe it
    into show_entries.html
    """
    cur = g.db.execute('select entries.title, entries.text, userPassword.username, '
                       'entries.start_time, entries.end_time, userPassword.gravataremail, entries.id'
                       ' from entries inner join userPassword on entries.username=userPassword.username'
                       ' order by entries.id desc')
    entries = [dict(title=row[0], text=row[1], username=row[2], start_time=row[3],
                    end_time=row[4], gravataremail=row[5], avimg=avatar(row[5]), id=row[6]) for row in cur.fetchall()]
    return render_template('show_entries.html', entries=entries)


@app.route('/add', methods=['POST'])
def add_entry():
    """
    Make a new entry, including title, text, username, start time and date (stime, sdate) and
    end time and date (etime, edate)
    """
    if not session.get('logged_in'):
        abort(401)

    if request.form['start_time'] == '':
        # use the default time (current time)
        g.db.execute('insert into entries (title, text, username, end_time) values (?,?,?,?)',
                     [request.form['title'], request.form['text'], session['username'], request.form['end_time']])
    else:
        g.db.execute('insert into entries (title, text, username, start_time, end_time)'
                     ' values (?,?,?,?,?)',
                     [request.form['title'], request.form['text'], session['username'], request.form['start_time'],
                      request.form['end_time']])
    g.db.commit()
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
        cur = g.db.execute('select username, password, gravataremail from userPassword where username=?',
                           [request.form['username']])
        row = cur.fetchone()

        if row is not None:
            # if the user is found
            user = {'username': row[0], 'password': row[1], 'gravataremail': row[2]}

            if not check_password_hash(user['password'], request.form['password']):
                # if the password hash in the database does not correspond to the hashed form of the given password
                error = 'Invalid password'
            else:
                session['logged_in'] = True
                session['username'] = user['username']
                session['gravataremail'] = user['gravataremail']
                flash('You were logged in')
                return redirect(url_for('show_entries'))
        else:
            # TODO username needs to be made unique in the database,
            # TODO otherwise this method will malfunction
            error = 'Invalid username'
    return render_template('login.html', error=error)


@app.route('/<entry_id>/show_comments')
def show_comments(entry_id):
    cur = g.db.execute(
        'SELECT DISTINCT comment_input, comments.username FROM comments, entries WHERE comments.entry_id = '
        + entry_id + ' ORDER BY comment_id desc')
    comments = [dict(comment_input=row[0], username=row[1]) for row in cur.fetchall()]

    cur = g.db.execute(
        'select title, text, username, start_time, end_time from entries where id = ' + entry_id + ' order by id desc')
    entries1 = [dict(title=row[0], text=row[1], username=row[2], start_time=row[3], end_time=row[4]) for row in
                cur.fetchall()]
    return render_template('show_comments.html', entries1=entries1, comments=comments, entry_id=entry_id)


@app.route('/<entry_id>/add_comments', methods=['POST'])
def add_comments(entry_id):
    if not session.get('logged_in'):
        abort(401)

    g.db.execute('insert into comments (comment_input, entry_id, username) values (?,?,?)',
                 [request.form['comment_input'], entry_id, session['username']])

    g.db.commit()
    flash('New comment was successfully posted')
    return redirect(url_for('show_comments', entry_id=entry_id))


@app.route('/<entry_id>/add_end_time', methods=['POST'])
def add_end_time(entry_id):
    if not session.get('logged_in'):
        abort(401)
    # if end_time_null_check is True:
    g.db.execute('UPDATE entries SET end_time=CURRENT_TIMESTAMP WHERE entries.id=' + entry_id + '')
    g.db.commit()
    flash('TASK ENDED')
    return redirect(url_for('show_comments', entry_id=entry_id))
    # else:
        # flash('TASK ALREADY ENDED')
        # return redirect(url_for('show_comments', entry_id=entry_id))


@app.route('/<entry_id>/end_time_null_check')
def end_time_null_check(entry_id):  # need to debug
    cur = g.db.execute('select end_time from entries where id=' + entry_id)
    end_time_fill = [dict(end_time=row[0]) for row in cur.fetchall()]
    if end_time_fill is None:
        return end_time_null_check is True


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
            g.db.execute('update userPassword set gravataremail=?, username=? where username =?',
                         [request.form['gravataremail'], request.form['username'], session['username']])
            g.db.execute('update entries set username=? where username=?',
                         [request.form['username'], session['username']])
            g.db.commit()
            session['username'] = request.form['username']
            session['gravataremail'] = request.form['gravataremail']
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
        cursor = g.db.execute('select username from userPassword where username=?', [request.form['username']])
        row = cursor.fetchone()

        if row is None:
            error = 'User does not exist'
        elif request.form['password'] is None or request.form['password'] == '':
            error = 'Empty password'
        elif request.form['password'] != request.form['confirm_password']:
            error = 'Please enter same password twice'
        else:
            # create the User object and add to the database
            user = User(request.form['username'], request.form['password'], session['gravataremail'])
            g.db.execute('update userPassword set password=? where username =?',
                         [user.password, user.username])
            g.db.commit()
            flash('Successfully changed user password')
            return render_template('change_password.html', success='Successfully changed password')

    return render_template('change_password.html', error=error)


@app.template_filter('newlines')
def newline_filter(s):
    s = s.replace("\r\n", '<br />')
    s = s.replace("\n", '<br />')
    # Markup() is used to prevent '<' and '>' symbols from being interpreted as less-than or greater-than symbols
    return Markup(s)


if __name__ == '__main__':
    # create and populate the database if it's not already there.
    if not isfile(str(app.config['DATABASE'])):
        app.logger.debug('creating database')
        init_db()

        usernames = ["admin", "hari", "jim", "spock"]
        passwords = ["default", "seldon", "bean", "vulcan"]
        gravataremails = ['daisy22229999@gmail.com', 'daisy200029@gmail.com', "jimbean@whisky.biz", "livelong@prosper.edu.au"]

        with closing(connect_db()) as db:
            for username, password, gravataremail in zip(usernames, passwords, gravataremails):
                user = User(username, password, gravataremail)
                app.logger.debug("Adding user {0} to the database.".format(user.username))
                db.execute('insert into userPassword (username, password, gravataremail) values (?, ?, ?)',
                           [user.username, user.password, user.gravataremail])
            db.commit()

    app.run()

