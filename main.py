from flask import Flask, session, render_template, request, redirect, g, url_for
import mysql.connector #here

app = Flask(__name__, template_folder='templates', static_folder='static')

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask_sqlalchemy import SQLAlchemy
from database_setup import Base, User, Trip, TransportBooking, TravelCompany,\
Mode, Hotel, HotelA, HotelBooking, Room

#engine = create_engine('mysql+mysqlconnector://travel:dbmsproject@localhost:3306/sqlalchemy',echo=True)
engine = create_engine('mysql+mysqlconnector://swd:swd123@localhost:3306/sqlalchemy',echo=True)

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

# @app.route('/hotel/',methods = ['GET', 'POST'])                    #from here
@app.route('/hotel/')  
# @app.route('/hotel/<id>/')
# def hotel(id):
def hotel():
    #return render_template("hotel.html")
    mydb = mysql.connector.connect( host="localhost",user="swd",password="swd123",database="sqlalchemy")
    mycursor = mydb.cursor()
    # sql="SELECT hotel_name,hotel_id FROM hotel"+" WHERE hotel_id="+str(id) 
    sql="SELECT hotel_name,hotel_id,hotel_city,hotel_contact FROM hotel"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    # sql="SELECT hotel_city FROM hotel"
    # mycursor.execute(sql)
    # hotel_ids = mycursor.fetchall()
    # output=''
    # hotel_imgs=list(myresult)
    final=[]
    for i in myresult:
        s=str(i)
        s = s[1:-1]
        l=s.split(",")

        s =l[0][1:-1]+","+l[1]+",images/"+l[1].strip()+".jpg"+","+l[2][2:-1]+","+l[3][2:-2]
        final.append(tuple(s.split(",")))
    # if request.method=='POST':
    #     return hotel_info(request.form['h_id'])
    # x="css/401.jpg"
    return render_template("hotel_display.html",items=final)

@app.route('/hotel_filter/')     #here
def hotel_filter():
    #return render_template("hotel.html")
    mydb = mysql.connector.connect( host="localhost",user="swd",password="swd123",database="sqlalchemy")
    mycursor = mydb.cursor()
    # sql="SELECT hotel_name,hotel_id FROM hotel"+" WHERE hotel_id="+str(id) 
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
    # if request.method=='POST':
    #     return hotel_info(request.form['h_id'])
    # x="css/401.jpg"
    return render_template("hotel_display.html",items=final)


@app.route('/hotel/<id>/')     #from here 
def hotel_info(id):
    mydb = mysql.connector.connect( host="localhost",user="swd",password="swd123",database="sqlalchemy")
    mycursor = mydb.cursor()
    #need to make sure hotel name is unique!!!!!
    sql="SELECT hotel_name,hotel_id,hotel_addr,hotel_contact,hotel_num_room FROM hotel "+"WHERE hotel_id="+str(id)
    #sql="SELECT hotel_name,hotel_id,hotel_addr,hotel_contact,hotel_num_room FROM hotel "+"WHERE hotel_name='"+str(id)+"'"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    return render_template("hotel_info.html",items=myresult)

# @app.route('/cico/<id>', methods = ['GET', 'POST'])  
# def check_in_check_out(id):
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

if __name__ == '__main__':
    app.run(debug=True)