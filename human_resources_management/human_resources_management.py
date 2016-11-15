from flask import Flask, render_template

app = Flask(__name__)


# user  position  department
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/users/')
def show_users():
    return render_template('users.html')


@app.route('/positions/')
def show_positions():
    return render_template('positions.html')


@app.route('/departments/')
def show_departments():
    return render_template('departments.html')


if __name__ == '__main__':
    app.run(debug=True)
