from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
from database_setup import  Base, User#table1 is my file name, and i'm importing all the classes that i need to fill (for now you can just import User and Base, that'll be enough)
 
engine = create_engine('mysql+mysqlconnector://travel:dbmsproject@localhost:3306/sqlalchemy',echo=True) #put in whatever db you've declared in your class declaration table

Base.metadata.bind = engine
 
DBSession = sessionmaker(bind=engine)

session = DBSession() 

user1 = User( user_id = 10 ,   user_name ='Deepti' ,  user_email='f20180790@hyderabad.bits-pilani.ac.in',  user_pass='11111' , user_phone='1111111111' ,  user_address='Chennai')

session.add(user1)
session.commit()

user2 = User( user_id =11 ,   user_name ='Anirudh' ,  user_email='f20180936@hyderabad.bits-pilani.ac.in',  user_pass='22222' , user_phone='2222222222' ,  user_address='Chennai')

session.add(user2)
session.commit()

user3 = User( user_id = 12 ,   user_name ='Eva' ,  user_email='f20180816@hyderabad.bits-pilani.ac.in',  user_pass='33333' , user_phone='3333333333' ,  user_address='Mumbai')

session.add(user3)
session.commit()

user4 = User( user_id = 13,   user_name ='Shreya' ,  user_email='f20180790886@hyderabad.bits-pilani.ac.in',  user_pass='44444' , user_phone='4444444444' ,  user_address='Delhi')

session.add(user4)
session.commit()

