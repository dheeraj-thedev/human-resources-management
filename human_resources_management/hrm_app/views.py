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


# ------------- USER ------------- #
@app.route('/users/')
def show_users():
    return render_template('users.html', title="Users", users=get_users())


@app.route('/new_user/', methods=['GET', 'POST'])
def new_user():
    if request.method == 'GET':
        departments = get_departments()
        positions = get_positions()
        return render_template('new_user.html', title="New User", departments=departments, positions=positions)

    elif request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        department_id = request.form['department_id']
        position_id = request.form['position_id']
        email = request.form['email']
        phone = request.form['phone']
        date_of_birth = request.form['date_of_birth']
        exec_db('INSERT INTO users (first_name, last_name, department_id, position_id, email, phone, date_of_birth) '
                'VALUES (?, ?, ?, ?, ?, ?, ?)',
                [first_name, last_name, department_id, position_id, email, phone, date_of_birth])
        return redirect(url_for('show_users'))


@app.route('/user/<int:user_id>/', methods=['GET', 'POST'])
def update_user(user_id):
    if request.method == 'GET':
        user = get_user(user_id)
        if user:
            departments = get_departments()
            positions = get_positions()
            return render_template('user.html', title=user['last_name'],
                                   user=user, departments=departments, positions=positions)
        return render_template('user.html', title='not found')

    elif request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        department_id = request.form['department_id']
        position_id = request.form['position_id']
        email = request.form['email']
        phone = request.form['phone']
        date_of_birth = request.form['date_of_birth']
        exec_db('UPDATE users '
                'SET first_name=?, last_name=?, department_id=?, position_id=?, email=?, phone=?, date_of_birth=? '
                'WHERE id=?',
                [first_name, last_name, department_id, position_id, email, phone, date_of_birth, user_id])
        return redirect(url_for('show_users'))


@app.route('/user/delete/<int:user_id>/', methods=['GET', 'POST'])
def delete_user(user_id):
    if request.method == 'GET':
        return render_template('error.html', title='error')
    elif request.method == 'POST':
        department = query_db('SELECT id, name FROM departments WHERE leader_id =?', [user_id], one=True)
        exec_db('DELETE FROM users WHERE id=?', [user_id])
        if department:
            return redirect(url_for('update_department', department_id=department[0]))
        return redirect(url_for('show_users'))


# ------------- POSITION ------------- #
@app.route('/positions/')
def show_positions():
    return render_template('positions.html', title="Positions", positions=get_positions())


@app.route('/new_position/', methods=['GET', 'POST'])
def new_position():
    if request.method == 'GET':
        return render_template('new_position.html', title="New Position")

    elif request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        exec_db('INSERT INTO positions (name, description) VALUES (?, ?)', [name, description])
        return redirect(url_for('show_positions'))


@app.route('/position/<int:position_id>/', methods=['GET', 'POST'])
def update_position(position_id):
    if request.method == 'GET':
        position = get_position(position_id)
        if position:
            return render_template('position.html', title=position['name'], position=position)
        return render_template('position.html', title='not found')
    elif request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        exec_db('UPDATE positions SET name=?, description=? WHERE id=?', [name, description, position_id])
        return redirect(url_for('show_positions'))


@app.route('/position/delete/<int:position_id>/', methods=['GET', 'POST'])
def delete_position(position_id):
    if request.method == 'GET':
        return render_template('error.html', title='error')
    elif request.method == 'POST':
        users = get_users_with_specify_position(position_id)
        if not users:
            exec_db('DELETE FROM positions WHERE id=?', [position_id])
            return redirect(url_for('show_positions'))
        else:
            return render_template('users.html', title="Users", users=users,
                                   msg='You should change position for this users first.')


# ------------- DEPARTMENT ------------- #
@app.route('/departments/')
def show_departments():
    return render_template('departments.html', title="Departments", departments=get_departments())


@app.route('/new_department/', methods=['GET', 'POST'])
def new_department():
    if request.method == 'GET':
        users = get_not_leader_users()
        return render_template('new_department.html', title="New Department",
                               users=users, departments=get_departments())

    elif request.method == 'POST':
        name = request.form['name']
        parental_department_id = request.form['parental_department_id']
        leader_id = request.form['leader_id']
        description = request.form['description']
        exec_db('INSERT INTO departments (name, parental_department_id, leader_id, description) VALUES (?, ?, ?, ?)',
                [name, parental_department_id, leader_id, description])
        return redirect(url_for('show_departments'))


@app.route('/department/<int:department_id>/', methods=['GET', 'POST'])
def update_department(department_id):
    if request.method == 'GET':
        department = get_department(department_id)
        if department:
            users = get_not_leader_users(department_id)
            return render_template('department.html', title=department['name'],
                                   department=department, departments=get_departments(department_id), users=users)
        return render_template('department.html', title='not found')
    elif request.method == 'POST':
        name = request.form['name']
        parental_department_id = request.form['parental_department_id']
        leader_id = request.form['leader_id']
        description = request.form['description']
        exec_db('UPDATE departments SET name=?, parental_department_id=?, leader_id=?, description=? WHERE id=?',
                [name, parental_department_id, leader_id, description, department_id])
        return redirect(url_for('show_departments'))


@app.route('/department/delete/<int:department_id>/', methods=['GET', 'POST'])
def delete_department(department_id):
    if request.method == 'GET':
        return render_template('error.html', title='error')
    elif request.method == 'POST':
        department = get_department(department_id)
        exec_db('UPDATE users SET department_id=? WHERE department_id=?',
                [department['parental_department_id'], department_id])
        exec_db('DELETE FROM departments WHERE id=?', [department_id])
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


def exec_db(query, args):
    db = get_db()
    db.execute(query, args)
    db.commit()


def get_user(user_id):
    user = query_db('SELECT * FROM users WHERE id = ?', [user_id], one=True)
    if user:
        user = dict(zip(
            ['id', 'first_name', 'last_name', 'department_id', 'position_id', 'email', 'phone', 'date_of_birth'],
            user))
        return user


def get_not_leader_users(department_id=0):
    users = query_db('SELECT * FROM users WHERE id NOT IN (SELECT leader_id FROM departments WHERE id !=?)',
                     [department_id])
    users = [{
                 'id': user[0],
                 'name': (user[1] + " " + user[2])
             } for user in users]
    return users


def get_users_with_specify_position(position):
    users = query_db('SELECT * FROM users WHERE position_id=?', [position])
    users = [{
                 'id': user[0],
                 'name': (user[1] + " " + user[2])
             } for user in users]
    return users


def get_users():
    users = query_db('SELECT id, first_name, last_name FROM users')
    users = [{
                 'id': user[0],
                 'name': (user[1] + " " + user[2])
             } for user in users]
    return users


def get_position(position_id):
    position = query_db('SELECT * FROM positions WHERE id = ?', [position_id], one=True)
    if position:
        position = dict(zip(['id', 'name', 'description'], position))
        return position


def get_positions():
    positions = query_db('SELECT id, name FROM positions')
    positions = [{
                     'id': position[0],
                     'name': position[1]
                 } for position in positions]
    return positions


def get_department(department_id):
    department = query_db('SELECT * FROM departments WHERE id = ?', [department_id], one=True)
    if department:
        department = dict(zip(['id', 'name', 'parental_department_id', 'leader_id', 'description'], department))
        return department


def get_departments(except_id=0):
    departments = query_db('SELECT id, name FROM departments WHERE id !=?', [except_id])
    departments = [{
                       'id': department[0],
                       'name': department[1]
                   } for department in departments]
    return departments


if __name__ == '__main__':
    # init_db()
    app.run()
