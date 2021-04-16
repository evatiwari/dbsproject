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
DBSession = sessionmaker(bind=engine)
session1 = DBSession()

newTrip = Trip()			
session1.add(newTrip)
session1.commit()
newTrip_id = newTrip.trip_id
if 'HotelBooking' == 'Hotel Booking':
	newHotel = HotelBooking()
	session1.add(newHotel)
	session1.commit()
	newHotel_id = newHotel.booking_id
	newTrip.hotel_bookingnum = newHotel_id
	session1.add(newTrip)
	session1.commit()
	
print("succes")