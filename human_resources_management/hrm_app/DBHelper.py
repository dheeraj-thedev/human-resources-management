import sqlite3


class DBHelper:
    def __init__(self, path_to_db):
        self.path_to_db = path_to_db
        # with sqlite3.connect(path_to_db) as db:
        #     with open('hrm_app/schema.sql') as f:
        #         db.cursor().executescript(f.read())
        #     db.commit()

    def get_db(self):
        return sqlite3.connect(self.path_to_db)

    def query_db(self, query, args=(), one=False):
        db = self.get_db()
        cur = db.execute(query, args)
        rv = cur.fetchall()
        db.close()
        return (rv[0] if rv else None) if one else rv

    def exec_db(self, query, args):
        db = self.get_db()
        db.execute(query, args)
        db.commit()
        db.close()

    def get_user(self, user_id):
        user = self.query_db('SELECT * FROM users WHERE id = ?', [user_id], one=True)
        if user:
            user = dict(zip(
                ['id', 'first_name', 'last_name', 'department_id', 'position_id', 'email', 'phone', 'date_of_birth'],
                user))
            return user

    def get_not_leader_users(self, department_id=0):
        users = self.query_db(
            'SELECT id, first_name, last_name FROM users WHERE id NOT IN (SELECT leader_id FROM departments WHERE id !=?)',
            [department_id])
        users = [{
                     'id': user[0],
                     'name': (user[1] + " " + user[2])
                 } for user in users]
        return users

    def get_users_with_specify_position(self, position):
        users = self.query_db('SELECT id, first_name, last_name FROM users WHERE position_id=?', [position])
        users = [{
                     'id': user[0],
                     'name': (user[1] + " " + user[2])
                 } for user in users]
        return users

    def create_user(self, data):
        self.exec_db(
            'INSERT INTO users (first_name, last_name, department_id, position_id, email, phone, date_of_birth) '
            'VALUES (?, ?, ?, ?, ?, ?, ?)',
            [data['first_name'],
             data['last_name'],
             data['department_id'],
             data['position_id'],
             data['email'],
             data['phone'],
             data['date_of_birth']])

    def update_user(self, data, user_id):
        self.exec_db('UPDATE users SET '
                     'first_name=?, '
                     'last_name=?, '
                     'department_id=?, '
                     'position_id=?, '
                     'email=?, '
                     'phone=?, '
                     'date_of_birth=? '
                     'WHERE id=?',
                     [data['first_name'],
                      data['last_name'],
                      data['department_id'],
                      data['position_id'],
                      data['email'],
                      data['phone'],
                      data['date_of_birth'],
                      user_id])

    def update_user_position(self, user_id, position_id):
        self.exec_db('UPDATE users SET position_id=? WHERE id=?', [position_id, user_id])

    def delete_user(self, user_id):
        self.exec_db('DELETE FROM users WHERE id=?', [user_id])

    def get_users(self):
        users = self.query_db('SELECT id, first_name, last_name FROM users')
        users = [{
                     'id': user[0],
                     'name': (user[1] + " " + user[2])
                 } for user in users]
        return users

    def update_users_department(self, old_id, new_id):
        self.exec_db('UPDATE users SET department_id=? WHERE department_id=?', [new_id, old_id])

    def get_position(self, position_id):
        position = self.query_db('SELECT * FROM positions WHERE id = ?', [position_id], one=True)
        if position:
            position = dict(zip(['id', 'name', 'description'], position))
            return position

    def create_position(self, values):
        self.exec_db('INSERT INTO positions (name, description) VALUES (?, ?)', values)

    def update_position(self, values):
        self.exec_db('UPDATE positions SET name=?, description=? WHERE id=?', values)

    def delete_position(self, position_id):
        self.exec_db('DELETE FROM positions WHERE id=?', [position_id])

    def get_positions_without_specify_id(self, position_id):
        positions = self.query_db('SELECT id, name FROM positions WHERE id != ?', [position_id])
        positions = [{
                         'id': position[0],
                         'name': position[1]
                     } for position in positions]
        return positions

    def get_positions(self):
        positions = self.query_db('SELECT id, name FROM positions')
        positions = [{
                         'id': position[0],
                         'name': position[1]
                     } for position in positions]
        return positions

    def get_department(self, department_id):
        department = self.query_db('SELECT * FROM departments WHERE id = ?', [department_id], one=True)
        if department:
            department = dict(zip(['id', 'name', 'parental_department_id', 'leader_id', 'description'], department))
            return department

    def get_department_leader(self, department_id):
        return self.query_db('SELECT leader_id FROM departments WHERE id = ?', [department_id], one=True)[0]

    def get_department_with_leader(self, leader_id):
        department = self.query_db('SELECT id, name, leader_id FROM departments WHERE leader_id = ?', [leader_id],
                                   one=True)
        if department:
            department = dict(zip(['id', 'name', 'leader_id'], department))
            return department

    def create_department(self, values):
        self.exec_db(
            'INSERT INTO departments (name, parental_department_id, leader_id, description) VALUES (?, ?, ?, ?)',
            values)

    def update_leader_department(self, department_id, leader_id):
        self.exec_db('UPDATE departments SET leader_id=? WHERE id=?', [leader_id, department_id])

    def update_department(self, values):
        self.exec_db('UPDATE departments SET name=?, parental_department_id=?, leader_id=?, description=? WHERE id=?',
                     values)

    def delete_department(self, department_id):
        self.exec_db('DELETE FROM departments WHERE id=?', [department_id])

    def get_departments(self, except_id=0):
        departments = self.query_db('SELECT id, name FROM departments WHERE id !=?', [except_id])
        departments = [{
                           'id': department[0],
                           'name': department[1]
                       } for department in departments]
        return departments
