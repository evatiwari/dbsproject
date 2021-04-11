from flask import Flask, session, render_template, request, redirect, g, url_for

app = Flask(__name__, template_folder='templates', static_folder='static')

import mysql.connector
mydb = mysql.connector.connect(host="localhost", user="travel", password="dbmsproject", database="sqlalchemy")

cursor = mydb.cursor()

cursor.execute("SHOW TABLES")

for x in cursor:
    print(x)

#from sqlalchemy import create_engine
#from sqlalchemy.orm import sessionmaker
#from flask_sqlalchemy import SQLAlchemy
#from database_setup import Base, User, Trip, TransportBooking, TravelCompany,\
#Mode, Hotel, HotelA, HotelBooking, Room

#engine = create_engine('mysql+mysqlconnector://travel:dbmsproject@localhost:3306/sqlalchemy',echo=True)
#Base.metadata.create_all(engine)

app.secret_key = "maynardjameskeenan"

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        session.pop('user', None)
        #SQL query to retrieve password
        uname=request.form['username']
        password=cursor.execute("SELECT user_pass FROM user WHERE user_name='%s'",uname)
        for x in cursor.fetchall():
            print(x)
        #if request.form['password'] == password:
            #session['user'] = request.form['username']
            #return redirect(url_for('user'))
    print("hello?")
    return render_template("login.html")

@app.route('/signup', methods = ['GET', 'POST'])
def signup():
    if request.method == 'POST':
        user_name=request.form['username']
        email=request.form['email']
        password=request.form['password']
        address=request.form['address']
        phone_number=request.form['phone']
        cursor.execute("SELECT MAX(user_id) FROM user")
        result=cursor.fetchone()
        uid=0
        query="INSERT INTO user VALUES (%s,%s,%s,%s,%s,%s)"
        cursor.execute(query,(uid,user_name,email,password,phone_number,address))
        cursor.execute("COMMIT")
        return redirect(url_for('login'))
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

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)