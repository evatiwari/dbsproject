
from flask import Flask, render_template, request, redirect, url_for, g, session
app = Flask(__name__, template_folder='templates', static_folder='static')

import os
import mysql.connector
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text 
from database_setup import Base, User, Trip, TransportBooking, TravelCompany, Mode, Hotel, HotelA, HotelBooking, Room
from sendmail import sendmail

engine = create_engine('mysql+mysqlconnector://travel:dbmsproject@localhost:3306/sqlalchemy',echo=True)
Base.metadata.create_all(engine)

mydb = mysql.connector.connect(host="localhost", user="travel", password="dbmsproject", database="sqlalchemy")
app.secret_key = "maynardjameskeenan"
cursor = mydb.cursor()

@app.route('/' )
def index():
	return render_template("index.html")

@app.route('/login', methods = ['GET','POST'])
def login():
    if request.method == 'POST':
        session.pop('user', None)
        #SQL query to retrieve password
        uname=request.form['username']
        try:
            sql="SELECT user_pass FROM user WHERE user_name='{}'".format(uname)
            cursor.execute(sql)
            password=cursor.fetchone()[0]
            if request.form['password'] == password:
                session['user'] = request.form['username']
                return render_template('user.html')
        except Exception as E:
            print(E)
            return redirect(url_for('login'))
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


@app.route('/travel', methods =['GET','POST'])
def travel():
	if request.method == 'POST':
		newTransport = TransportBooking()
		newTransport_id = newTransport.booking_id
		session.add(newTransport)
		session.commit()
		if request.form['numtickets']:
			newTransport.num_tickets = request.form['numtickets']
		if request.form['check_in']:
			newTransport.depart_date=request.form['check_in']
		if request.form['to']:
			newTransport.to_dest= request.form['to']
		if request.form['from']:
			newTransport.from_dest= request.form['from']
		session.execute(text('update transport_booking set num_tickets= :num, to_dest= :to , from_dest = :fro where booking_id = :idt') , {'num' :newTransport.num_tickets ,'to' : newTransport.to_dest, 'fro' :newTransport.from_dest, 'idt': newTransport.booking_id })
		cursor.execute("commit")		
		return redirect(url_for('travelcomp' , newTransport_id= newTransport.booking_id))
	else:
		print("GET method on travelpage1")
		return render_template('travelpage1.html'  )

@app.route('/check')
def check():
	return render_template("check_in_check_out.html")

@app.route('/travelcomp/<int:newTransport_id>' , methods = ['GET', 'POST'])
def travelcomp(newTransport_id):
	newTransport = session.query(TransportBooking).filter_by(booking_id=newTransport_id).one()
	travelcomp = session.execute('select * from travel_company')
	mode = session.query(Mode)
	return render_template("displaytravel.html" , travelcomp= travelcomp , newTransport = newTransport , mode = Mode )

@app.route('/confirmtravel')
def confirmtravel():
	return render_template("confirmtravel.html")

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
	
	app.debug=True
	app.run(host='0.0.0.0', port=5000)