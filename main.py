from flask import Flask, render_template

app = Flask(__name__, template_folder='templates', static_folder='static')

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/user')
def user():
    return render_template("user.html")

@app.route('/hotel')
def hotel():
    return render_template("hotel.html")

@app.route('/bookings')
def bookings():
    return render_template("bookings.html")

if __name__ == '__main__':
    app.run(debug=True)