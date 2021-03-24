import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

#start inserting your tables below
class Mode(Base):
    __tablename__='mode'
    mode_id=Column(Integer, primary_key=True)
    mode_of_transport=Column(String(20))
    price=Column(Integer)

class TravelCompany(Base):
	_tablename_ = 'travel_company'
	travel_name = Column(String(80), nullable = False)
	travel_id = Column(Integer, primary_key = True)
	travel_contact = Column(BigInteger)
	num_tickets = Column(Integer)

class TransportBooking(Base):
    __tablename__='transport_booking'
    booking_id=Column(Integer, primary_key=True)
    travel_mode=Column(Integer, ForeignKey('mode.mode_id'))
    num_tickets=Column(Integer)
    arrival_date=Column(DateTime)
    depart_date=Column(DateTime)
    to_dest=Column(String(80))
    from_dest=Column(String(80))
    travel_id=Column(Integer, ForeignKey('travel_company.travel_id'))

class Room(Base):
	_tablename_ = 'room'
	type_id = Column(Integer, primary_key= True)
	room_type = Column(String(100) , nullable = False)
	price = Column(BigInteger, nullable = False)

class Hotel(Base):
	_tablename_ = 'hotel'
	hotel_name = Column(String(80), nullable = False)
	hotel_id = Column(Integer, primary_key = True)
	hotel_addr= Column(String(250))
	hotel_contact = Column(BigInteger)
	hotel_num_room = Column(Integer)
	
class HotelA(Base):
	_tablename_ = 'hotela'
	hotela_id = Column(Integer,  ForeignKey('hotel.hotel_id') , primary_key = True)
	room_no = Column(Integer, ForeignKey('room.type_id'), primary_key = True)
	room = relationship(Room)
	hotela = relationship(Hotel)


class HotelBooking(Base) :
	_tablename_ = 'hotel_booking'
	booking_id = Column(Integer, primary_key = True)
	hotel_id = Column(Integer,  ForeignKey('hotel.hotel_id'))
	check_in = Column(DateTime)
	check_out = Column(DateTime)
	hotel = relationship(Hotel)


engine =create_engine('mysql+mysqlconnector://travel:dbmsproject@localhost:3306/sqlalchemy',echo=True)
Base.metadata.create_all(engine)

#print("Successful")