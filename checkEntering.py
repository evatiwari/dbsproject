from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base,User,Hotel
engine =create_engine('mysql+mysqlconnector://swd:swd123@localhost:3306/sqlalchemy',echo=True) #put in whatever db you've declared in your class declaration table

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession() 


user1=User(user_id=101,user_name="Kiran",user_email="kiran123@gmail.com",user_pass="kiranabc",user_phone="987654321",user_address="Chennai");
session.add(user1)
session.commit()



hotel1=Hotel(hotel_name="Leela Palace",hotel_id=401,hotel_addr="Street4",hotel_contact="9679674567",hotel_num_room=25)
session.add(hotel1)
session.commit()



print ("added menu items!") 