from flask import render_template, request, redirect, url_for

from hrm_app import app, DB

@app.route('/')
def index():
    return render_template('index.html')


# ------------- USER ------------- #
@app.route('/users/')
def show_users():
    return render_template('user/users.html', title="Users", users=DB.get_users())


@app.route('/new_user/', methods=['GET', 'POST'])
def new_user():
    if request.method == 'GET':
        return render_template('user/new_user.html',
                               title="New User",
                               departments=DB.get_departments(),
                               positions=DB.get_positions())

    elif request.method == 'POST':
        DB.create_user([request.form['first_name'],
                        request.form['last_name'],
                        request.form['department_id'],
                        request.form['position_id'],
                        request.form['email'],
                        request.form['phone'],
                        request.form['date_of_birth']])
        return redirect(url_for('show_users'))


@app.route('/user/<int:user_id>/', methods=['GET', 'POST'])
def update_user(user_id):
    if request.method == 'GET':
        user = DB.get_user(user_id)
        if user:
            return render_template('user/user.html',
                                   title=user['last_name'],
                                   user=user,
                                   departments=DB.get_departments(),
                                   positions=DB.get_positions())
        return render_template('user/user.html', title='not found')

    elif request.method == 'POST':
        DB.update_user([request.form['first_name'],
                        request.form['last_name'],
                        request.form['department_id'],
                        request.form['position_id'],
                        request.form['email'],
                        request.form['phone'],
                        request.form['phone'],
                        user_id])
        return redirect(url_for('show_users'))


@app.route('/user/delete/<int:user_id>/', methods=['GET', 'POST'])
def delete_user(user_id):
    if request.method == 'GET':
        return render_template('error.html', title='error')
    elif request.method == 'POST':
        department = DB.get_department_with_leader(user_id)
        DB.delete_user(user_id)
        if department:
            return redirect(url_for('update_department', department_id=department[0]))
        return redirect(url_for('show_users'))


# ------------- POSITION ------------- #
@app.route('/positions/')
def show_positions():
    return render_template('position/positions.html', title="Positions", positions=DB.get_positions())


@app.route('/new_position/', methods=['GET', 'POST'])
def new_position():
    if request.method == 'GET':
        return render_template('position/new_position.html', title="New Position")

    elif request.method == 'POST':
        DB.create_position([request.form['name'],
                            request.form['description']])
        return redirect(url_for('show_positions'))


@app.route('/position/<int:position_id>/', methods=['GET', 'POST'])
def update_position(position_id):
    if request.method == 'GET':
        position = DB.get_position(position_id)
        if position:
            return render_template('position/position.html',
                                   title=position['name'],
                                   position=position)
        return render_template('position/position.html', title='not found')
    elif request.method == 'POST':
        DB.update_position([request.form['name'], request.form['description']])
        return redirect(url_for('show_positions'))


@app.route('/position/delete/<int:position_id>/', methods=['GET', 'POST'])
def delete_position(position_id):
    if request.method == 'GET':
        return render_template('error.html', title='error')
    elif request.method == 'POST':
        users = DB.get_users_with_specify_position(position_id)
        if not users:
            DB.delete_position(position_id)
            return redirect(url_for('show_positions'))
        else:
            return render_template('user/users.html',
                                   title="Users",
                                   users=users,
                                   msg='You should change position for this users first.')


# ------------- DEPARTMENT ------------- #
@app.route('/departments/')
def show_departments():
    return render_template('department/departments.html', title="Departments", departments=DB.get_departments())


@app.route('/new_department/', methods=['GET', 'POST'])
def new_department():
    if request.method == 'GET':
        return render_template('department/new_department.html',
                               title="New Department",
                               users=DB.get_not_leader_users(),
                               departments=DB.get_departments())

    elif request.method == 'POST':
        DB.create_department([request.form['name'],
                              request.form['parental_department_id'],
                              request.form['leader_id'],
                              request.form['description']])
        return redirect(url_for('show_departments'))


@app.route('/department/<int:department_id>/', methods=['GET', 'POST'])
def update_department(department_id):
    if request.method == 'GET':
        department = DB.get_department(department_id)
        if department:
            users = DB.get_not_leader_users(department_id)
            return render_template('department/department.html',
                                   title=department['name'],
                                   department=department,
                                   departments=DB.get_departments(department_id),
                                   users=users)
        return render_template('department/department.html', title='not found')
    elif request.method == 'POST':
        DB.update_department([request.form['name'],
                              request.form['parental_department_id'],
                              request.form['leader_id'],
                              request.form['description'],
                              department_id])
        return redirect(url_for('show_departments'))


@app.route('/department/delete/<int:department_id>/', methods=['GET', 'POST'])
def delete_department(department_id):
    if request.method == 'GET':
        return render_template('error.html', title='error')
    elif request.method == 'POST':
        department = DB.get_department(department_id)
        DB.update_users_department(department_id, department['parental_department_id'])
        DB.delete_department(department_id)
        return redirect(url_for('show_departments'))