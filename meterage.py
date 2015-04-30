from contextlib import closing
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
    abort, render_template, flash
from jinja2 import Markup
# from os.path import isfile

import config

# create application
app = Flask(__name__, instance_relative_config=True)
app.config.from_object(config)
app.config.from_pyfile('config.py')
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

def connect_db():
    """
    Make a connection to the database specified in the config.
    """
    return sqlite3.connect(app.config['DATABASE'])


def init_db():
    """
    For initialising the database using schemal.sql.  This is usually called manually.
    """
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


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
    cur = g.db.execute('select title, text, username, sdate, stime, edate, etime from entries order by id desc')
    entries = [dict(title=row[0], text=row[1], username=row[2], sdate=row[3], stime=row[4], edate=row[5], etime=row[6])
               for row in cur.fetchall()]
    return render_template('show_entries.html', entries=entries)


@app.route('/add', methods=['POST'])
def add_entry():
    """
    Make a new entry, including title, text, username, start time and date (stime, sdate) and
    end time and date (etime, edate)
    """
    if not session.get('logged_in'):
        # If someone tries to access the page without being logged in
        abort(401)
    g.db.execute('insert into entries (title, text, username, sdate, stime, edate, etime) values (?,?,?,?,?,?,?)',
                 [request.form['title'], request.form['text'], session['username'], request.form['sdate'],
                  request.form['stime'], request.form['edate'], request.form['etime']])
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
        # get the username-password combination from the database
        cur = g.db.execute('select username, password from userPassword where username=?', [request.form['username']])
        row = cur.fetchone()

        if row is not None:
            # if the user is found
            user = {'username': row[0], 'password': row[1]}
            if request.form['password'] != user['password']:
                error = 'Invalid password'
            else:
                session['logged_in'] = True
                session['username'] = user['username']
                flash('You were logged in')
                return redirect(url_for('show_entries'))
        else:
            # TODO username needs to be made unique in the database,
            # TODO otherwise this method will malfunction
            error = 'Invalid username'
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))


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
            g.db.execute('update userPassword set password=? where username =?',
                             [request.form['password'], request.form['username']])
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
    # create the database if it's not already there.
    # if not isfile(str(app.config['DATABASE'])):
    #     app.logger.debug('creating database')
    #     init_db()
    app.run()
