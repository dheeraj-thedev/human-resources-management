import sqlite3
import os
from flask import Flask, render_template, request, redirect, flash, url_for, g
from contextlib import closing

# configuration
DATABASE = os.path.join(os.path.dirname(__file__), 'database.db')
DEBUG = True
SECRET_KEY = 'development key'

app = Flask(__name__)
app.config.from_object(__name__)


@app.teardown_request
def teardown_request(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


# user  position  department
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/users/')
def show_users():
    users = query_db('select * from users')
    users = [(user[1] + " " + user[2]) for user in users]
    return render_template('users.html', title="Users", users=users)


@app.route('/new_user/', methods=['GET', 'POST'])
def new_user():
    if request.method == 'GET':
        departments = query_db('select * from departments')
        departments = [department[1] for department in departments]
        positions = query_db('select * from positions')
        positions = [position[1] for position in positions]
        return render_template('new_user.html', title="New User", departments=departments, positions=positions)

    elif request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        department_id = request.form['department_id']
        position_id = request.form['position_id']
        email = request.form['email']
        phone = request.form['phone']
        date_of_birth = request.form['date_of_birth']
        db = get_db()
        db.execute(
            'INSERT INTO users '
            '(first_name, last_name, department_id, position_id, email, phone, date_of_birth)'
            ' VALUES (?, ?, ?, ?, ?, ?, ?)',
            [first_name, last_name, department_id, position_id, email, phone, date_of_birth])
        db.commit()
        return redirect(url_for('show_users'))


@app.route('/user/<int:user_id>/', methods=['GET', 'POST'])
def update_user(user_id):
    if request.method == 'GET':
        departments = query_db('select * from departments')
        departments = [department[1] for department in departments]
        positions = query_db('select * from positions')
        positions = [position[1] for position in positions]
        user = query_db('select * from users where id = ?', [user_id], one=True)
        if user is not None:
            user = dict(zip(
                ['id', 'first_name', 'last_name', 'department_id', 'position_id', 'email', 'phone', 'date_of_birth'],
                user))
            return render_template('user.html', title=user['last_name'], user=user, departments=departments,
                                   positions=positions)
        return render_template('user.html', title='not found')
    elif request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        department_id = request.form['department_id']
        position_id = request.form['position_id']
        email = request.form['email']
        phone = request.form['phone']
        date_of_birth = request.form['date_of_birth']
        db = get_db()
        db.execute(
            'UPDATE users SET'
            ' first_name=?, last_name=?, department_id=?, position_id=?, email=?, phone=?, date_of_birth=? '
            ' WHERE id=?',
            [first_name, last_name, department_id, position_id, email, phone, date_of_birth, user_id])
        db.commit()
        return redirect(url_for('show_users'))


@app.route('/positions/')
def show_positions():
    positions = query_db('select * from positions')
    positions = [position[1] for position in positions]
    return render_template('positions.html', title="Positions", positions=positions)


@app.route('/new_position/', methods=['GET', 'POST'])
def new_position():
    if request.method == 'GET':
        return render_template('new_position.html', title="New Position")

    elif request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        db = get_db()
        db.execute(
            'INSERT INTO positions '
            '(name, description)'
            ' VALUES (?, ?)',
            [name, description])
        db.commit()
        return redirect(url_for('show_positions'))


@app.route('/position/<int:position_id>/', methods=['GET', 'POST'])
def update_position(position_id):
    if request.method == 'GET':
        position = query_db('select * from positions where id = ?', [position_id], one=True)
        if position is not None:
            position = dict(zip(['id', 'name', 'description'], position))
            return render_template('position.html', title=position['name'], position=position)
        return render_template('position.html', title='not found')
    elif request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        db = get_db()
        db.execute(
            'UPDATE positions SET'
            ' name=?, description=?'
            ' WHERE id=?',
            [name, description, position_id])
        db.commit()
        return redirect(url_for('show_positions'))


@app.route('/departments/')
def show_departments():
    departments = query_db('select * from departments')
    departments = [department[1] for department in departments]
    return render_template('departments.html', title="Departments", departments=departments)


@app.route('/new_department/', methods=['GET', 'POST'])
def new_department():
    if request.method == 'GET':
        users = query_db('select * from users')
        users = [(user[1] + " " + user[2]) for user in users]
        departments = query_db('select * from departments')
        departments = [department[1] for department in departments]
        return render_template('new_department.html', title="New Department", users=users, departments=departments)

    elif request.method == 'POST':
        name = request.form['name']
        parental_department_id = request.form['parental_department_id']
        leader_id = request.form['leader_id']
        description = request.form['description']
        db = get_db()
        db.execute(
            'INSERT INTO departments '
            '(name, parental_department_id, leader_id, description)'
            ' VALUES (?, ?, ?, ?)',
            [name, parental_department_id, leader_id, description])
        db.commit()
        return redirect(url_for('show_departments'))


@app.route('/department/<int:department_id>/', methods=['GET', 'POST'])
def update_department(department_id):
    if request.method == 'GET':
        users = query_db('select * from users')
        users = [(user[1] + " " + user[2]) for user in users]
        departments = query_db('select * from departments where id !=?', [department_id])
        departments = [department[1] for department in departments]

        department = query_db('select * from departments where id = ?', [department_id], one=True)
        if department is not None:
            department = dict(zip(['id', 'name', 'parental_department_id', 'leader_id', 'description'], department))
            return render_template('department.html', title=department['name'], department=department,
                                   departments=departments,
                                   users=users)
        return render_template('department.html', title='not found')
    elif request.method == 'POST':
        name = request.form['name']
        parental_department_id = request.form['parental_department_id']
        leader_id = request.form['leader_id']
        description = request.form['description']
        db = get_db()
        db.execute(
            'UPDATE departments SET '
            'name=?, parental_department_id=?, leader_id=?, description=?'
            ' WHERE id=?',
            [name, parental_department_id, leader_id, description, department_id])
        db.commit()
        return redirect(url_for('show_departments'))


# functions for work with database
def connect_db():
    return sqlite3.connect(app.config['DATABASE'])


def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = connect_db()
    return db


def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


if __name__ == '__main__':
    # init_db()
    app.run()
