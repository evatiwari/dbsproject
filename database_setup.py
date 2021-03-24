import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

#start inserting your tables below
class TransportBooking(Base):
    __tablename__='transport_booking'
    booking_id=Column(Integer, primary_key=True)
    travel_mode=Column(Integer, ForeignKey('mode.mode_id'))
    num_tickets=Column(Integer)
    arrival_date=Column(DateTime)
    depart_date=Column(DateTime)
    to_dest=Column(String(80))
    from_dest=Column(String(80))
    travel_id=Column(Integer, ForeignKey(''))

class Mode(Base):
    __tablename__='mode'
    mode_id=Column(Integer, primary_key=True)
    mode_of_transport=Column(String(20))
    price=Column(Integer)

engine =create_engine('mysql+mysqlconnector://travel:dbmsproject@localhost:3306/sqlalchemy',echo=True)
Base.metadata.create_all(engine)

#print("Successful")