import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, TransportBooking

Base = declarative_base()

engine =create_engine('mysql+mysqlconnector://travel:dbmsproject@localhost:3306/sqlalchemy',echo=True) #eva's setup
#engine =create_engine('mysql+mysqlconnector://travel:virgo@2000@localhost:3306/sqlalchemy',echo=True) #deepti's setup
Base.metadata.create_all(engine)
dbsession = sessionmaker(bind = engine)
session = dbsession()
newTransport = TransportBooking()
newTransport_id = newTransport.booking_id
session.add(newTransport)
session.commit()
newTransport.num_tickets= 5
newTransport.depart_date="2020-12-20"
newTransport.to_dest= "Chennai"
newTransport.from_dest="Delhi"
session.add(newTransport)
session.commit()
print("added")
r = session.query(TransportBooking).all()
for i in r:
	print (i.booking_id, i.num_tickets)