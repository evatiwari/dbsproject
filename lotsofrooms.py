from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
from database_setup import Room, Base, Hotel, HotelBooking #table1 is my file name, and i'm importing all the classes that i need to fill (for now you can just import User and Base, that'll be enough)
 
engine = create_engine('mysql+mysqlconnector://travel:dbmsproject@localhost:3306/sqlalchemy',echo=True)
Base.metadata.create_all(engine)
 
DBSession = sessionmaker(bind=engine)

session = DBSession() #till here it's the same

#from this line onwards, you'll have to write 3 lines, and repeat till how many ever values you need (for now, 10 are enough ig, feel free to use my name a tuple in user name XD)

room1 = Room( type_id= 1 , room_type = "Single" , price = 5000) #line 1, room1 is just a variable, you can use user1 if you like
													#Room is the class you've declared, which is User in your case.
													#except for user id, fill in all the other details (name,email,pass,phone,adress) avoid lines in between

session.add(room1)#line2
session.commit() #line3


#now you can just copy paste the 3 lines, change variable number and the values inside the " "
#i'll sleep at 12 and be up at 7, other than always free
#happy coding 
room2 = Room( type_id= 2 , room_type = "Double" , price = 10000)

session.add(room2)
session.commit()

room3 = Room( type_id= 3, room_type = "Triple" , price = 15000)

session.add(room3)
session.commit()

room4 = Room( type_id= 4, room_type = "Quad" , price = 20000)

session.add(room4)
session.commit()

room5 = Room( type_id=5, room_type = "Queen" , price = 25000)

session.add(room5)
session.commit()

room6 = Room( type_id= 6, room_type = "King" , price = 27000)

session.add(room6)
session.commit()

room7 = Room( type_id= 7, room_type = "Twin" , price = 30000)

session.add(room7)
session.commit()

room8 = Room(type_id=8 ,  room_type = "Adjacent" , price = 35000)

session.add(room8)
session.commit()

room9 = Room( type_id=9 , room_type = "Adjoin" , price = 40000)

session.add(room9)
session.commit()

room10 = Room( type_id= 10, room_type = "Connecting" , price = 50000)

session.add(room10)
session.commit()


print ("added rooms items!")