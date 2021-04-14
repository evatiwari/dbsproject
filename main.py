
from flask import Flask, render_template, request, redirect, url_for, g, session
app = Flask(__name__, template_folder='templates', static_folder='static')

import os
import mysql.connector
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text 
from database_setup import Base, User, Trip, TransportBooking, TravelCompany, Mode, Hotel, HotelA, HotelBooking, Room
import datetime
from sendmail import sendmail

engine = create_engine('mysql+mysqlconnector://travel:dbmsproject@localhost:3306/sqlalchemy',echo=True)
Base.metadata.create_all(engine)

mydb = mysql.connector.connect(host="localhost", user="travel", password="dbmsproject", database="sqlalchemy")
app.secret_key = "maynardjameskeenan"
cursor = mydb.cursor()



DBSession = sessionmaker(bind=engine)
session1 = DBSession()

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
@app.route('/trips', methods= ['POST' , 'GET'])
def trips():
		if request.method =='POST':
			newTrip = Trip()			
			session1.add(newTrip)
			session1.commit()
			newTrip_id = newTrip.trip_id
			if request.form['action'] == 'Transport Booking':
				newTransport = TransportBooking()				
				session1.add(newTransport)
				session1.commit()
				newTransport_id = newTransport.booking_id
				newTrip.travel_bookingnum = newTransport_id  #error from this line onwards, trip not storing travel_id
				session1.add(newTrip)
				session1.commit()
				return redirect(url_for('travel' , newTransport_id = newTransport.booking_id))
			if request.form['action'] == 'Hotel Booking':
				return redirect(url_for('hotel' ))
			if request.form['action'] == 'History':
				session1.delete(newTrip)
				session1.commit()
				return redirect(url_for('bookings' ))
		else:
			return render_template("trips.html")

@app.route('/hotel')
def hotel():
    mydb = mysql.connector.connect( host="localhost",user="travel",password="dbmsproject",database="sqlalchemy")
    mycursor = mydb.cursor()
    sql="SELECT hotel_name,hotel_id,hotel_city,hotel_contact FROM hotel"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    final=[]
    for i in myresult:
        s=str(i)
        s = s[1:-1]
        l=s.split(",")

        s =l[0][1:-1]+","+l[1]+",images/"+l[1].strip()+".jpg"+","+l[2][2:-1]+","+l[3][2:-2]
        final.append(tuple(s.split(",")))
    return render_template("hotel_display.html",items=final)

@app.route('/hotel_filter/')
def hotel_filter():
    mydb = mysql.connector.connect( host="localhost",user="travel",password="dbmsproject",database="sqlalchemy")
    mycursor = mydb.cursor()
    sql="SELECT hotel_name,hotel_id,hotel_city,hotel_contact FROM hotel ORDER BY hotel_city"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    final=[]
    for i in myresult:
        s=str(i)
        s = s[1:-1]
        l=s.split(",")
        s =l[0][1:-1]+","+l[1]+",images/"+l[1].strip()+".jpg"+","+l[2][2:-1]+","+l[3][2:-2]
        final.append(tuple(s.split(",")))
    return render_template("hotel_display.html",items=final)

@app.route('/hotel/<id>/')
def hotel_info(id):
    mydb = mysql.connector.connect( host="localhost",user="swd",password="swd123",database="sqlalchemy")
    mycursor = mydb.cursor()
    sql="SELECT hotel_name,hotel_id,hotel_addr,hotel_contact,hotel_num_room FROM hotel "+"WHERE hotel_id="+str(id)
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    return render_template("hotel_info.html",items=myresult)

@app.route('/cico/', methods = ['GET', 'POST'])  
def check_in_check_out():
    # return render_template("check_in_check_out.html")
    if request.method=='POST':
        ci_date=request.form['check_in']
        co_date=request.form['check_out']
        mydb = mysql.connector.connect( host="localhost",user="swd",password="swd123",database="sqlalchemy")
        mycursor = mydb.cursor()
        # sql="UPDATE hotel_booking SET check_in='2000-12-23', check_out='2000-12-27' WHERE booking_id=201"
        sql="UPDATE hotel_booking SET check_in= '"+str(ci_date)+"', check_out='"+str(co_date)+"' WHERE booking_id=201"
        mycursor.execute(sql)
        mydb.commit()
        return hotel()
    return render_template("check_in_check_out.html")    

@app.route('/bookings')
def bookings():
    return render_template("bookings.html")


@app.route('/travel/<int:newTransport_id>', methods =['GET','POST'])
def travel(newTransport_id):
	newTransport = session1.query(TransportBooking).filter_by(booking_id=newTransport_id).one()
	if request.method == 'POST':
		if request.form['name'] == 'Submit':
			if request.form['numtickets']:
				newTransport.num_tickets = request.form['numtickets']
			if request.form['check_in']:
				newTransport.depart_date=request.form['check_in']
			if request.form['to']:
				newTransport.to_dest= request.form['to']
			if request.form['from']:
				newTransport.from_dest= request.form['from']
			session1.execute(text('update transport_booking set num_tickets= :num, to_dest= :to , from_dest = :fro where booking_id = :idt') , {'num' :newTransport.num_tickets ,'to' : newTransport.to_dest, 'fro' :newTransport.from_dest, 'idt': newTransport.booking_id })
			cursor.execute("commit")		
			return redirect(url_for('travelcomp' , newTransport_id= newTransport.booking_id))
		elif request.form['name'] =='Back to Trip':
			newTrip = session1.query(Trip).filter_by(travel_bookingnum = newTransport_id).one()
			newTrip.travel_bookingnum = None 
			session1.add(newTrip)
			session1.delete(newTransport)
			cursor.execute("commit")
			return redirect(url_for('trips' ))
	else:
		print("GET method on travelpage1")
		return render_template('travelpage1.html' , newTransport_id= newTransport_id )

@app.route('/check')
def check():
	return render_template("check_in_check_out.html")

@app.route('/travelcomp/<int:newTransport_id>' , methods = ['GET', 'POST'])
def travelcomp(newTransport_id):
	newTransport = session1.query(TransportBooking).filter_by(booking_id=newTransport_id).one()
	travelcomp = session1.query(TravelCompany)
	#modes = session1.execute('select * from mode')
	modes = session1.query(Mode)
	if request.method == 'POST':
		#if request.form['name']:
		if request.form['action'] == "Submit" :
			print('The form has data, we can proceed')
			newTransport.travel_id = request.form['options']
			#chosenTravel = session1.query(TravelCompany).filter_by(travel_id= newTransport.travel_id).one()
			chosenTravel = session1.query(TravelCompany).filter_by(travel_id= newTransport.travel_id).one()
			newTransport.travel_mode = chosenTravel.mode_id
			if chosenTravel.mode_id >300 :
				newTransport.arrival_date = newTransport.depart_date + datetime.timedelta( days = 2 ,hours=5, minutes=13)
			else:
				newTransport.arrival_date = newTransport.depart_date + datetime.timedelta( days = 1 ,hours=2, minutes=10)
			#price = session1.execute(text('select price from mode where mode.mode_id = :ii'),{'ii': request.form['options'] })
			price = session1.query(Mode).filter_by(mode_id = chosenTravel.mode_id).one()
			newTransport.totprice = newTransport.num_tickets *price.price
			chosenTravel.num_tickets = chosenTravel.num_tickets - newTransport.num_tickets
			session1.add(newTransport)
			session1.execute(text("update travel_company set num_tickets= :num where travel_company.travel_id = :idf"),{'num' :chosenTravel.num_tickets,'idf' : newTransport.travel_id})
			session1.commit()
			cursor.execute("commit")
			return redirect(url_for('confirmtravel', newTransport_id = newTransport_id))
		elif request.form['action'] == 'All':
			return render_template("displaytravel.html" , travelcomp= travelcomp , newTransport = newTransport , mode = modes )
		elif request.form['action'] == 'Flights':
			travelcomp = session1.query(TravelCompany).filter( TravelCompany.mode_id  < 300)
			return render_template("displaytravel.html" , travelcomp= travelcomp , newTransport = newTransport , mode = modes )
		elif request.form['action'] == 'Trains':
			travelcomp = session1.query(TravelCompany).filter(TravelCompany.mode_id  >= 300)
			return render_template("displaytravel.html" , travelcomp= travelcomp , newTransport = newTransport , mode = modes )	
			
	else:
		return render_template("displaytravel.html" , travelcomp= travelcomp , newTransport = newTransport , mode = modes )

@app.route('/confirmtravel/<int:newTransport_id>' , methods = ['GET', 'POST'])
def confirmtravel(newTransport_id):
	newTransport = session1.query(TransportBooking).filter_by(booking_id=newTransport_id).one()
	travelcomp = session1.query(TravelCompany).filter_by(travel_id= newTransport.travel_id).one()
	modes = session1.query(Mode).filter_by(mode_id = newTransport.travel_mode).one()
	if request.method=='POST':
		if request.form['action'] == 'Delete':
			travelcomp.num_tickets = travelcomp.num_tickets + newTransport.num_tickets
			session1.add(travelcomp)
			itemToDelete = session1.query(TransportBooking).filter_by(booking_id = newTransport_id).one() 
			newTrip = session1.query(Trip).filter_by(travel_bookingnum = newTransport_id).one()
			newTrip.travel_bookingnum = None 
			session1.add(newTrip)
			session1.delete(itemToDelete)
			session1.commit()
			return redirect(url_for('trips'))
		elif request.form['action'] == 'Confirm':
			return redirect(url_for('trips'))
		elif request.form['action'] == 'Back':
			travelcomp.num_tickets = travelcomp.num_tickets + newTransport.num_tickets
			session1.add(travelcomp)
			session1.commit()
			return redirect(url_for('travelcomp' , newTransport_id= newTransport.booking_id))
	else:
		return render_template("confirmtravel.html" , newTransport = newTransport , travel = travelcomp , mode = modes)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
	
	app.debug=True
	app.run(host='0.0.0.0', port=5000)




	