
from flask import Flask, render_template, request, redirect, url_for, g, session
app = Flask(__name__, template_folder='templates', static_folder='static')

import os
import mysql.connector
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text 
from database_setup import Base, User, Trip, TransportBooking, TravelCompany, Mode, Hotel, HotelA, HotelBooking, Room
import datetime
from functools import wraps
from pdfserver.sendmail import sendmail,hotelreservation

engine = create_engine('mysql+mysqlconnector://travel:dbmsproject@localhost:3306/sqlalchemy',echo=True)
Base.metadata.create_all(engine)

mydb = mysql.connector.connect(host="localhost", user="travel", password="dbmsproject", database="sqlalchemy")
app.secret_key = "maynardjameskeenan"
cursor = mydb.cursor()
curuser=None

DBSession = sessionmaker(bind=engine)
session1 = DBSession()

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('user') is None:
            return redirect('/login',code=302)
        return f(*args, **kwargs)
    return decorated_function

@app.route('/' )
def index():
	return render_template("index.html")

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        session.pop('user',None)
        uname=request.form['username']
        try:
            sql="SELECT user_pass FROM user WHERE user_name='{}'".format(uname)
            cursor.execute(sql)
            password=cursor.fetchone()[0]
            if request.form['password']==password:
                session['user']=request.form['username']
                sql="SELECT user_id FROM user WHERE user_name='{}'".format(uname)
                cursor.execute(sql)
                global curuser
                curuser=int(cursor.fetchone()[0])
                return redirect(url_for('user',id=curuser))
        except Exception as E:
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

@app.route('/user/',methods = ['GET', 'POST'])
@login_required
def user():
    newUser = session1.query(User).filter_by(user_id=curuser).one()
    if request.method=='POST':
        if request.form['action'] == 'Book a Trip':
            return redirect(url_for('trips'))
        if request.form['action'] == 'Your Trip History':
            return redirect(url_for('bookings'))
    else:
        return render_template('user.html',newUser=newUser)
            

@app.before_request
def before_request():
    g.user=None
    if 'user' in session:
        g.user = session['user']


@app.route('/trips', methods= ['POST' , 'GET'])
@login_required
def trips():
    if request.method =='POST':
        newTrip = Trip()
        session1.add(newTrip)
        session1.commit()
        newTrip_id = newTrip.trip_id
        newTrip.user_id = curuser
        if request.form['action'] == 'Transport Booking':
            newTransport = TransportBooking()
            session1.add(newTransport)
            session1.commit()
            newTransport_id = newTransport.booking_id
            newTrip.travel_bookingnum = newTransport_id 
            session1.add(newTrip)
            session1.commit()
            return redirect(url_for('travel' , newTransport_id = newTransport.booking_id))
        if request.form['action'] == 'Hotel Booking':
            newHotel = HotelBooking()
            session1.add(newHotel)
            session1.commit()
            newHotel_id = newHotel.booking_id
            newTrip.hotel_bookingnum = newHotel_id
            session1.add(newTrip)
            session1.commit()
            return redirect(url_for('check_in_check_out', newHotel_id = newHotel.booking_id))
            #return redirect(url_for('hotel' ))
        if request.form['action'] == 'History':
            session1.delete(newTrip)
            session1.commit()
            return redirect(url_for('bookings' ))
        if request.form['action'] == 'Profile':
            session1.delete(newTrip)
            session1.commit()
            return redirect(url_for('user' ))
    else:
        return render_template("trips.html")


@app.route('/hotel/<int:id>', methods= ['GET' ,'POST'])
@login_required
def hotel(id):
    sql="SELECT hotel_name,hotel_id,hotel_city,hotel_contact FROM hotel"
    cursor.execute(sql)
    myresult = cursor.fetchall()
    final=[]
    for i in myresult:
        s=str(i)
        s = s[1:-1]
        l=s.split(",")

        s =l[0][1:-1]+","+l[1]+",../static/img/"+l[1].strip()+".jpg"+","+l[2][2:-1]+","+l[3][2:-2]
        final.append(tuple(s.split(",")))
    if request.method=='POST':
        if request.form['action'] =='Back':
            return redirect(url_for('check_in_check_out' , newHotel_id = id))
    else:
        return render_template("hotel_display.html",items=final , id= id )


@app.route('/hotel_filter/<int:id>', methods=['GET' ,'POST'])
@login_required
def hotel_filter(id):
    sql="SELECT hotel_name,hotel_id,hotel_city,hotel_contact FROM hotel ORDER BY hotel_city"
    cursor.execute(sql)
    myresult = cursor.fetchall()
    final=[]
    for i in myresult:
        s=str(i)
        s = s[1:-1]
        l=s.split(",")
        s =l[0][1:-1]+","+l[1]+",../static/img/"+l[1].strip()+".jpg"+","+l[2][2:-1]+","+l[3][2:-2]
        final.append(tuple(s.split(",")))
    if request.method=='POST':
        if request.form['action'] =='Back':
            return redirect(url_for('check_in_check_out' , newHotel_id = id))
    return render_template("hotel_display.html",items=final , id=id)


@app.route('/hotelinfo/<int:id>/<int:hotelid>' , methods =['GET' , 'POST'])
@login_required
def hotel_info(hotelid, id):
    sql="SELECT hotel_name,hotel_id,hotel_addr,hotel_contact,hotel_num_room FROM hotel "+"WHERE hotel_id=%d"%hotelid
    cursor.execute(sql)
    myresult = cursor.fetchall()
    if request.method =='POST':
        print("inside post")
        if request.form['action'] =='Back':
            return redirect(url_for('hotel' , id = id ))
        elif request.form['action'] =='Choose this Hotel':
            newBooking = session1.query(HotelBooking).filter_by(booking_id = id).one()
            #thisHotel = session1.query(Hotel).filter_by(hotel_id= hotelid).one()
            newBooking.hotel_id = hotelid 
            session1.add(newBooking)
            session1.commit()
            return redirect(url_for('room_det' ,id = id))
    else:
        return render_template("hotel_info.html",items=myresult ,hotelid = hotelid , id = id)


@app.route('/cico/<int:newHotel_id>', methods = ['GET', 'POST'])
@login_required
def check_in_check_out(newHotel_id):
    # return render_template("check_in_check_out.html")
    newHotel = session1.query(HotelBooking).filter_by(booking_id=newHotel_id).one()
    print("cico called")
    if request.method=='POST':
        if request.form['name'] =='Continue':
            ci_date=request.form['check_in']
            co_date=request.form['check_out']
            print(ci_date, co_date)
            # sql="UPDATE hotel_booking SET check_in='2000-12-23', check_out='2000-12-27' WHERE booking_id=201"
            sql="UPDATE hotel_booking SET check_in= '"+str(ci_date)+"', check_out='"+str(co_date)+"' WHERE booking_id= %d" %newHotel.booking_id  
            cursor.execute(sql )
            cursor.execute("commit")
            return redirect(url_for('hotel', id = newHotel_id))
        elif request.form['name'] =='Back to Trip':
            newTrip = session1.query(Trip).filter_by(hotel_bookingnum = newHotel.booking_id).one()
            newTrip.hotel_bookingnum = None 
            session1.add(newTrip)
            session1.delete(newHotel)
            session1.commit()
            return redirect(url_for('trips' ))
    return render_template("check_in_check_out.html" , newHotel_id = newHotel_id)    


@app.route('/bookings/' ,methods=['GET' ,'POST'])
@login_required
def bookings():
    if request.method == 'POST':
        if request.form['action'] =='Hotel':
            return redirect(url_for('hotel_history'))
        elif request.form['action'] =='Transport':
            return redirect(url_for('travel_history'))
        elif request.form['action'] =='Back':
            return redirect(url_for('trips'))
    else:
        return render_template("bookings.html")


@app.route('/travel/<int:newTransport_id>', methods =['GET','POST'])
@login_required
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


@app.route('/travelcomp/<int:newTransport_id>' , methods = ['GET', 'POST'])
@login_required
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
@login_required
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
            newTrip = session1.query(Trip).filter_by(travel_bookingnum = newTransport_id).one()
            email=session1.query(User).filter_by(user_id=curuser).one().user_email
            sendmail(newTransport,travelcomp,modes,email) ##
            return redirect(url_for('continued' , newTrip_id = newTrip.trip_id ))
        elif request.form['action'] == 'Back':
            travelcomp.num_tickets = travelcomp.num_tickets + newTransport.num_tickets
            session1.add(travelcomp)
            session1.commit()
            return redirect(url_for('travelcomp' , newTransport_id= newTransport.booking_id))
    else:
        return render_template("confirmtravel.html" , newTransport = newTransport , travel = travelcomp , mode = modes)


@app.route('/logout', methods =['GET' , 'POST'])
@login_required
def logout():
    session.pop('username', None)
    global curuser
    curuser=None
    return redirect(url_for('login'))



@app.route('/room_details/<int:id>', methods=['GET', 'POST'])
@login_required
def room_det(id):
#def room_det():
    if request.method == 'POST':
        newHBook = session1.query(HotelBooking).filter_by(booking_id = id).one(); 
        Hotelfetch = session1.query(Hotel).filter_by(hotel_id = newHBook.hotel_id).one()
        if request.form['action'] =='Submit':
            var_num=request.form['num']
            var_rooms=request.form['rooms']
            x = "SELECT type_id from room where room_type='"+str(var_rooms)+"'"
            cursor.execute(x)
            result = cursor.fetchone()[0]
            newHBook.num_rooms = int(var_num)
            newHBook.room_type = int(result)
            
            price = session1.query(Room).filter_by(room_type = var_rooms).one()

            newHBook.totprice = newHBook.num_rooms * int(price.price)
            session1.add(newHBook)
            session1.commit()
            Hotelfetch.hotel_num_room = Hotelfetch.hotel_num_room - int(var_num)
            session1.add(Hotelfetch)
            session1.commit()
            #sql = "UPDATE hotel_booking SET room_type = "+str(result[0])+"  WHERE booking_id=201 "
            #sql = "UPDATE hotel_booking SET room_type =%d "%(result[0])"  WHERE booking_id=%d "%id
            #cursor.execute(sql)
            #session1.commit()
            return redirect(url_for('room_confirmation' , id = id ))
        if request.form['action'] =='Back':
            return redirect(url_for('hotel' , id = id ))
        #return room_confirmation()
    return render_template("RoomDetails.html" , id = id )


@app.route('/room_confirmation/<int:id>' , methods = ['GET', 'POST'])
@login_required
def room_confirmation(id):
    newHotel = session1.query(HotelBooking).filter_by(booking_id = id).one()
    hotelDet = session1.query(Hotel).filter_by(hotel_id = newHotel.hotel_id).one()
    roomType = session1.query(Room).filter_by(type_id = newHotel.room_type).one()
    if request.method == 'POST':
        if request.form['action'] == 'Delete':
            hotelDet.hotel_num_room = hotelDet.hotel_num_room + newHotel.num_rooms
            session1.add(hotelDet)
            itemToDelete = session1.query(HotelBooking).filter_by(booking_id = id).one()
            newTrip = session1.query(Trip).filter_by(hotel_bookingnum = id).one()
            newTrip.hotel_bookingnum = None 
            session1.add(newTrip)
            session1.delete(itemToDelete)
            session1.commit()
            return redirect(url_for('trips'))
        elif request.form['action'] == 'Confirm':
            newTrip = session1.query(Trip).filter_by(hotel_bookingnum = id).one()
            email=session1.query(User).filter_by(user_id=curuser).one().user_email
            hotelreservation(hotelDet,newHotel,roomType,email)    
            return redirect(url_for('continued' , newTrip_id = newTrip.trip_id ))
        elif request.form['action'] == 'Back':
            hotelDet.hotel_num_room = hotelDet.hotel_num_room + newHotel.num_rooms
            session1.add(hotelDet)
            session1.commit()
            return redirect(url_for('room_det', id = id))
    else:
        return render_template("Confirmationhotel.html", newHotel = newHotel, hotelDet = hotelDet, roomType = roomType)


@app.route('/hotel_history', methods = ['GET', 'POST'])
@login_required
def hotel_history():
    sql=" select h.hotel_name,h.hotel_city,h.hotel_addr,h.hotel_contact,hb.check_in,hb.check_out,r.price,r.room_type,hb.num_rooms from trip t,hotel_booking hb,hotel h,room r   where t.hotel_bookingnum=hb.booking_id and h.hotel_id=hb.hotel_id  and hb.room_type=r.type_id and t.user_id= %d;"%curuser
    cursor.execute(sql)
    myresult = cursor.fetchall()
    if request.method == 'POST':
        if request.form['action'] == 'Back':
            return redirect(url_for('trips'))
        if request.form['action'] == 'Next':
            return redirect(url_for('travel_history'))
    else:
        return render_template("hotel_history.html",items=myresult)


@app.route('/travel_history/', methods = ['GET', 'POST'])
@login_required
def travel_history():
    sql="select tc.travel_name,tc.travel_contact,tb.num_tickets,tb.arrival_date,tb.depart_date,tb.to_dest,tb.from_dest,m.mode_of_transport,m.price from mode m,trip t,travel_company tc,transport_booking tb where t.travel_bookingnum=tb.booking_id and tb.travel_mode=m.mode_id and tb.travel_id=tc.travel_id and t.user_id=%d"%curuser
    cursor.execute(sql)
    myresult = cursor.fetchall()
    if request.method == 'POST':
        if request.form['action'] == 'Back':
            return redirect(url_for('trips'))
        if request.form['action'] == 'Next':
            return redirect(url_for('hotel_history'))
    else:
        return render_template("travel_history.html",items=myresult)


@app.route('/continue/<int:newTrip_id>' , methods=['GET' ,'POST'])
@login_required
def continued(newTrip_id):
    newTrip = session1.query(Trip).filter_by(trip_id = newTrip_id).one()
    if request.method =='POST':
        if request.form['action']=='Return':
            return redirect(url_for('trips'))
        if request.form['action'] == 'No':
            return redirect(url_for('trips'))
        if request.form['action'] == 'Yes':
            if newTrip.travel_bookingnum == None:
                newTransport = TransportBooking()
                session1.add(newTransport)
                session1.commit()
                newTransport_id = newTransport.booking_id
                newTrip.travel_bookingnum = newTransport_id  #error from this line onwards, trip not storing travel_id
                session1.add(newTrip)
                session1.commit()
                return redirect(url_for('travel' , newTransport_id = newTransport.booking_id))
            if newTrip.hotel_bookingnum == None:
                newHotel = HotelBooking()
                session1.add(newHotel)
                session1.commit()
                newHotel_id = newHotel.booking_id
                newTrip.hotel_bookingnum = newHotel_id
                session1.add(newTrip)
                session1.commit()
                return redirect(url_for('check_in_check_out', newHotel_id = newHotel.booking_id))
            
    else:
        return render_template("continued.html" , trip = newTrip )






if __name__ == '__main__':
	
	app.debug=True
	app.run(host='0.0.0.0', port=5000)

