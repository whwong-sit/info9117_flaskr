from contextlib import closing
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
    abort, render_template, flash

# configuration
DATABASE = 'db/flask.db'
DEBUG = True
SECRET_KEY = 'development key'
# USERNAME = 'admin'
# PASSWORD = 'default'
USERS = {'admin': 'default', 'jim': 'bean', 'spock': 'vulcan'}

app = Flask(__name__)
app.config.from_object(__name__)

app.config.from_envvar('FLASKR_SETTINGS', silent=True)


def connect_db():
    return sqlite3.connect(app.config['DATABASE'])


def init_db():
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
    cur = g.db.execute('select title, text, username, start_time, end_time,id from entries order by id desc')
    entries = [dict(title=row[0], text=row[1], username=row[2], start_time=row[3], end_time=row[4], entry_id=row[5]) for
               row in cur.fetchall()]
    return render_template('show_entries.html', entries=entries)


@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)

    g.db.execute('insert into entries (title, text, username) values (?,?,?)',
                 [request.form['title'], request.form['text'], session['username']])
    g.db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))


@app.route('/<entry_id>/show_comments')
def show_comments(entry_id):
    cur = g.db.execute(
        'SELECT DISTINCT comment_input, comments.username FROM comments, entries WHERE comments.entry_id = ' + entry_id + ' ORDER BY comment_id desc')
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
    #if end_time_null_check is True:
    g.db.execute('UPDATE entries SET end_time=CURRENT_TIMESTAMP WHERE entries.id=' + entry_id + '')
    g.db.commit()
    flash('TASK ENDED')
    return redirect(url_for('show_comments', entry_id=entry_id))
   # else:
        #flash('TASK ALREADY ENDED')
        #return redirect(url_for('show_comments', entry_id=entry_id))



@app.route('/<entry_id>/end_time_null_check')
def end_time_null_check(entry_id):  #need to debug
    cur = g.db.execute('select end_time from entries where id=' + entry_id)
    end_time_fill = [dict(end_time=row[0]) for row in cur.fetchall()]
    if end_time_fill is None:
        return end_time_null_check is True


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        if username not in app.config['USERS'].keys():
            error = 'Invalid username'
        elif request.form['password'] != app.config['USERS'][username]:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            session['username'] = username
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))


if __name__ == '__main__':
    app.run('0.0.0.0', 5002)
