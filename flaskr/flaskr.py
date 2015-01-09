# all the imports
import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from contextlib import closing

# creating our application
app = Flask(__name__)

# configuration
DATABASE = os.path.join(app.root_path, 'flaskr.db')
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

app.config.from_object(__name__)

# to be able to connect to our database so we can open connections on request
def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

# initializing our database
def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()
    print('Successfully initialized the database.')

@app.before_request
def before_request():
    g.db = connect_db()
    cur = g.db.execute('select firstname, lastname, charity, about, email from entries order by id desc')
    if cur.fetchall():
        g.db.execute('update entries set hitcount = hitcount + 1 where (firstname = "Hitcount") and (lastname = "Initializer")')
        g.db.commit()
    else:
        g.db.execute('insert into entries (firstname, lastname, hitcount) values (?, ?, ?)', ["Hitcount", "Initializer", 1])
        g.db.commit()


@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

# showing entries
@app.route('/')
def show_entries():
    cur = g.db.execute('select firstname, lastname, charity, about, email from entries order by id desc')
    entries = [dict(firstname=row[0], lastname=row[1], charity=row[2], about=row[3], email=row[4]) for row in cur.fetchall()]
    return render_template('show_entries.html', entries=entries)

# adding new entry
@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    g.db.execute('insert into entries (firstname, lastname, charity, about, email) values (?, ?, ?, ?, ?)',
                 [request.form['firstname'], request.form['lastname'], request.form['charity'], request.form['about'], request.form['email']])
    g.db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))

# loggin in
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)

# logging out
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))

# collaborator pages
@app.route('/collaborator')
def collaborator(entry_info):
    collaborator_info = None
    cur = g.db.execute('select firstname, lastname, charity, about from entries order by id desc where (firstname <> "Hitcount") and (lastname <> "Initializer")')
    entries = [dict(firstname=row[0], lastname=row[1], charity=row[2], about=row[3]) for row in cur.fetchall()]
    for e in entries:
        if e['firstname'] == entry_info['firstname'] and e['lastname'] == entry_info['lastname']:
            collaborator_info = e
            break
    return render_template('collaborator.html', collaborator_info=collaborator_info)

# running the server if this program is being run by itself
if __name__ == '__main__':
    app.run()

