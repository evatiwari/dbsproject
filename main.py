from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__, template_folder='templates', static_folder='static')

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text 
from database_setup import Base, User, Trip, TransportBooking, TravelCompany, Mode, Hotel, HotelA, HotelBooking, Room
import datetime
engine = create_engine('mysql+mysqlconnector://travel:dbmsproject@localhost:3306/sqlalchemy',echo=True)

Base.metadata.create_all(engine)
import mysql.connector
mydb = mysql.connector.connect(host="localhost", user="travel", password="dbmsproject", database="sqlalchemy")
app.secret_key = "maynardjameskeenan"

cursor = mydb.cursor()


DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/' ,methods =['GET' , 'POST'] )
def index():
	
	if request.method =='POST':
		if request.form['action'] == 'Transport Booking':
			newTransport = TransportBooking()
			newTransport_id = newTransport.booking_id
			session.add(newTransport)
			session.commit()
			return redirect(url_for('travel' , newTransport_id = newTransport.booking_id))

	else:
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

@app.route('/travel/<int:newTransport_id>', methods =['GET','POST'])
def travel(newTransport_id):
	newTransport = session.query(TransportBooking).filter_by(booking_id=newTransport_id).one()
	if request.method == 'POST':
		#newTransport = TransportBooking()
		#newTransport_id = newTransport.booking_id
		#session.add(newTransport)
		#session.commit()
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
		return render_template('travelpage1.html' , newTransport_id= newTransport_id )

@app.route('/check')
def check():
	return render_template("check_in_check_out.html")

@app.route('/travelcomp/<int:newTransport_id>' , methods = ['GET', 'POST'])
def travelcomp(newTransport_id):
	newTransport = session.query(TransportBooking).filter_by(booking_id=newTransport_id).one()
	travelcomp = session.query(TravelCompany)
	#modes = session.execute('select * from mode')
	modes = session.query(Mode)
	if request.method == 'POST':
		#if request.form['name']:
		if request.form['action'] == "Submit" :
			print('The form has data, we can proceed')
			newTransport.travel_id = request.form['options']
			chosenTravel = session.query(TravelCompany).filter_by(travel_id= newTransport.travel_id).one()
			newTransport.travel_mode = chosenTravel.mode_id
			if chosenTravel.mode_id >300 :
				newTransport.arrival_date = newTransport.depart_date + datetime.timedelta( days = 2 ,hours=5, minutes=13)
			else:
				newTransport.arrival_date = newTransport.depart_date + datetime.timedelta( days = 1 ,hours=2, minutes=10)
			#price = session.execute(text('select price from mode where mode.mode_id = :ii'),{'ii': request.form['options'] })
			price = session.query(Mode).filter_by(mode_id = chosenTravel.mode_id).one()
			newTransport.totprice = newTransport.num_tickets *price.price
			chosenTravel.num_tickets = chosenTravel.num_tickets - newTransport.num_tickets
			session.add(newTransport)
			session.execute(text("update travel_company set num_tickets= :num where travel_company.travel_id = :idf"),{'num' :chosenTravel.num_tickets,'idf' : newTransport.travel_id})
			session.commit()
			cursor.execute("commit")
			return redirect(url_for('confirmtravel', newTransport_id = newTransport_id))
		elif request.form['action'] == 'All':
			return render_template("displaytravel.html" , travelcomp= travelcomp , newTransport = newTransport , mode = modes )
		elif request.form['action'] == 'Flights':
			travelcomp = session.query(TravelCompany).filter( TravelCompany.mode_id  < 300)
			return render_template("displaytravel.html" , travelcomp= travelcomp , newTransport = newTransport , mode = modes )
		elif request.form['action'] == 'Trains':
			travelcomp = session.query(TravelCompany).filter(TravelCompany.mode_id  >= 300)
			return render_template("displaytravel.html" , travelcomp= travelcomp , newTransport = newTransport , mode = modes )	
			
	else:
		return render_template("displaytravel.html" , travelcomp= travelcomp , newTransport = newTransport , mode = modes )

@app.route('/confirmtravel/<int:newTransport_id>' , methods = ['GET', 'POST'])
def confirmtravel(newTransport_id):
	newTransport = session.query(TransportBooking).filter_by(booking_id=newTransport_id).one()
	travelcomp = session.query(TravelCompany).filter_by(travel_id= newTransport.travel_id).one()
	modes = session.query(Mode).filter_by(mode_id = newTransport.travel_mode).one()
	if request.method=='POST':
		if request.form['action'] == 'Delete':
			travelcomp.num_tickets = travelcomp.num_tickets + newTransport.num_tickets
			session.add(travelcomp)
			itemToDelete = session.query(TransportBooking).filter_by(booking_id = newTransport_id).one() 
			session.delete(itemToDelete)
			session.commit()
			return redirect(url_for('index'))
		elif request.form['action'] == 'Confirm':
			return redirect(url_for('index'))
		elif request.form['action'] == 'Back':
			travelcomp.num_tickets = travelcomp.num_tickets + newTransport.num_tickets
			session.add(travelcomp)
			session.commit()
			return redirect(url_for('travelcomp' , newTransport_id= newTransport.booking_id))
	else:
		return render_template("confirmtravel.html" , newTransport = newTransport , travel = travelcomp , mode = modes)


if __name__ == '__main__':
	
	app.debug=True
	app.run(host='0.0.0.0', port=5000)




	