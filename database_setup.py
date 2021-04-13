import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

#start inserting your tables below
class User(Base):
    __tablename__ = 'user'
    user_id = Column(Integer, primary_key = True)
    user_name =Column(String(80), nullable = False)
    user_email=Column(String(80), nullable = False)
    user_pass=Column(String(15),nullable = False)
    user_phone=Column(String(10), nullable = False)
    user_address=Column(String(100),nullable=False)
    
    
class Trip(Base):
    __tablename__ = 'trip'
    trip_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.user_id'))
    hotel_bookingnum=Column(Integer, ForeignKey('hotel_booking.booking_id'))
    travel_bookingnum=Column(Integer, ForeignKey('transport_booking.booking_id'))
    user=relationship(User)

class Mode(Base):
    __tablename__='mode'
    mode_id=Column(Integer, primary_key=True)
    mode_of_transport=Column(String(20)) #flight or train
   	#mode_name = Coulmn(String(100)) #shatabdi or indigo or rajdani or spicejet or 
    price=Column(Integer)

class TravelCompany(Base):
	__tablename__ = 'travel_company'
	travel_name = Column(String(80), nullable = False) #shatabdi or indigo or spicejet
	travel_id = Column(Integer, primary_key = True)
	travel_contact = Column(BigInteger) #NULL also
	num_tickets = Column(Integer)
	mode_id = Column(Integer, ForeignKey('mode.mode_id'))
	mode = relationship(Mode)

class TransportBooking(Base):
    __tablename__='transport_booking'
    booking_id=Column(Integer, primary_key=True)
    travel_mode=Column(Integer, ForeignKey('mode.mode_id'))
    num_tickets=Column(Integer)
    arrival_date=Column(DateTime)
    depart_date=Column(DateTime)
    to_dest=Column(String(80))
    from_dest=Column(String(80))
    totprice = Column(Integer)
    travel_id=Column(Integer, ForeignKey('travel_company.travel_id'))
    travel_comp = relationship(TravelCompany)
    mode = relationship(Mode)

class Room(Base):
	__tablename__ = 'room'
	type_id = Column(Integer, primary_key= True)
	room_type = Column(String(100) , nullable = False)
	price = Column(BigInteger, nullable = False)

class Hotel(Base):
	__tablename__ = 'hotel'
	hotel_name = Column(String(80), nullable = False)
	hotel_id = Column(Integer, primary_key = True)
	hotel_lane= Column(String(250))
	hotel_city= Column(String(250))
	hotel_contact = Column(BigInteger)
	hotel_num_room = Column(Integer)
	
class HotelA(Base):
	__tablename__ = 'hotela'
	hotela_id = Column(Integer,  ForeignKey('hotel.hotel_id') , primary_key = True)
	room_no = Column(Integer, ForeignKey('room.type_id'), primary_key = True)
	room = relationship(Room)
	hotela = relationship(Hotel)


class HotelBooking(Base) :
	__tablename__ = 'hotel_booking'
	booking_id = Column(Integer, primary_key = True)
	hotel_id = Column(Integer,  ForeignKey('hotel.hotel_id'))
	check_in = Column(DateTime)
	check_out = Column(DateTime)
	num_rooms = Column(Integer) #number of rooms for the user
	room_type = Column(Integer, ForeignKey('room.type_id'))
	hotel = relationship(Hotel)
	room = relationship(Room)


engine =create_engine('mysql+mysqlconnector://travel:dbmsproject@localhost:3306/sqlalchemy',echo=True) #eva's setup
#engine =create_engine('mysql+mysqlconnector://travel:virgo@2000@localhost:3306/sqlalchemy',echo=True) #deepti's setup
Base.metadata.create_all(engine)

print("Successful")