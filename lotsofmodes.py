from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
from database_setup import  Base, Mode#table1 is my file name, and i'm importing all the classes that i need to fill (for now you can just import User and Base, that'll be enough)
 
engine = create_engine('mysql+mysqlconnector://travel:dbmsproject@localhost:3306/sqlalchemy',echo=True) #put in whatever db you've declared in your class declaration table

Base.metadata.bind = engine
 
DBSession = sessionmaker(bind=engine)

session = DBSession() 

mode1 = Mode(mode_id = 101 , mode_of_transport = "Flight Economy" ,   price = 5500)												
session.add(mode1)#line2
session.commit() #line3

mode1 = Mode(mode_id = 106 , mode_of_transport = "Flight First Class" ,   price = 10000)												
session.add(mode1)#line2
session.commit() #line3

mode1 = Mode(mode_id = 301 , mode_of_transport = "Train 3rd AC" ,   price = 2750)												
session.add(mode1)#line2
session.commit() #line3

mode1 = Mode(mode_id = 350 , mode_of_transport = "Train Chair Car" ,   price = 1000)												
session.add(mode1)#line2
session.commit() #line3


print ("added modes!")