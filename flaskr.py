from contextlib import closing
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
    abort, render_template, flash

#configuration
DATABASE = 'db/flask.db'
DEBUG = True
SECRET_KEY = 'development key'
#USERNAME = 'admin'
#PASSWORD = 'default'
USERS = {'admin':'default','adam':'alpha','bob':'bravo','cat':'charlie'}

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
    cur = g.db.execute('select title, text, username, sdate, stime, edate, etime from entries order by id desc')
    entries = [dict(title=row[0], text=row[1], username=row[2], sdate=row[3], stime=row[4], edate=row[5], etime=row[6]) for row in cur.fetchall()]
    return render_template('show_entries.html', entries=entries)

@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    g.db.execute('insert into entries (title, text, username, sdate, stime, edate, etime) values (?,?,?,?,?,?,?)',
                 [request.form['title'], request.form['text'], session['username'], request.form['sdate'], request.form['stime'], request.form['edate'], request.form['etime']])
    g.db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        cursor = g.db.execute('select username, password from userPassword where username=?', [request.form['username']])
        row = cursor.fetchone()
        user = {'username':row[0], 'password':row[1]}
        print user
        if user['username'] is None:
            error = 'Invalid username'
        elif request.form['password'] != user['password']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            session['username'] = user['username']
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)
	
@app.route('/logout')
def logout():
	session.pop('logged_in', None)
	flash('You were logged out')
	return redirect(url_for('show_entries'))

	
@app.route('/change_password')
def change_password():
    
	return redirect(url_for('change_password'))

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8080)
