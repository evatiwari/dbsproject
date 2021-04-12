from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__, template_folder='templates', static_folder='static')

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text 
from database_setup import Base, User, Trip, TransportBooking, TravelCompany, Mode, Hotel, HotelA, HotelBooking, Room

engine = create_engine('mysql+mysqlconnector://travel:dbmsproject@localhost:3306/sqlalchemy',echo=True)

Base.metadata.create_all(engine)
import mysql.connector
mydb = mysql.connector.connect(host="localhost", user="travel", password="dbmsproject", database="sqlalchemy")
app.secret_key = "maynardjameskeenan"

cursor = mydb.cursor()


DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/' )
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


if __name__ == '__main__':
	
	app.debug=True
	app.run(host='0.0.0.0', port=5000)