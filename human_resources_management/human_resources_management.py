from flask import Flask, render_template

app = Flask(__name__)


# user  position  department
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/users/')
def show_users():
    return render_template('users.html', title="Users")


@app.route('/positions/')
def show_positions():
    return render_template('positions.html', title="Positions")


@app.route('/departments/')
def show_departments():
    return render_template('departments.html', title="Departments")


if __name__ == '__main__':
    app.run()
