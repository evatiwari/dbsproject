from flask import Flask, session, render_template, request, redirect, g, url_for

app = Flask(__name__, template_folder='templates', static_folder='static')

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask_sqlalchemy import SQLAlchemy
from database_setup import Base, User, Trip, TransportBooking, TravelCompany,\
Mode, Hotel, HotelA, HotelBooking, Room

engine = create_engine('mysql+mysqlconnector://travel:dbmsproject@localhost:3306/sqlalchemy',echo=True)
Base.metadata.create_all(engine)

app.secret_key = "ilikeskysowner"

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        session.pop('user', None)
        #SQL query to retrieve password
        if request.form['password'] == 'pass':
            session['user'] = request.form['username']
            return redirect(url_for('user'))
    return render_template("login.html")

@app.route('/signup')
def signup():
    return render_template("signup.html")


@app.route('/user')
def user():
    if g.user:
        return render_template("user.html", user=session['user'])
    return redirect(url_for("login"))

@app.before_request
def before_request():
    g.user=None
    if 'user' in session:
        g.user = session['user']

@app.route('/hotel')
def hotel():
    return render_template("hotel.html")

@app.route('/bookings')
def bookings():
    return render_template("bookings.html")

if __name__ == '__main__':
    app.run(debug=True)