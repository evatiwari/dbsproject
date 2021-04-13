from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
from database_setup import  Base, TravelCompany #table1 is my file name, and i'm importing all the classes that i need to fill (for now you can just import User and Base, that'll be enough)
 
engine = create_engine('mysql+mysqlconnector://travel:dbmsproject@localhost:3306/sqlalchemy',echo=True) #put in whatever db you've declared in your class declaration table

Base.metadata.bind = engine
 
DBSession = sessionmaker(bind=engine)

session = DBSession() 

		
		
	
	
		
			
		
		
		


travel1 = TravelCompany(mode_id = 101 , travel_id = 1, travel_name = "Indigo" ,   travel_contact =41223117 ,  num_tickets = 300)
													

session.add(travel1)#line2
session.commit() #line3

travel2 = TravelCompany( mode_id = 101 , travel_id = 2, travel_name = "Spicejet" ,  travel_contact = 25091116 ,  num_tickets = 150)

session.add(travel2)
session.commit()

travel3 = TravelCompany( mode_id = 101 , travel_id = 3, travel_name = "Jet Airways" ,   travel_contact = 46973971,  num_tickets =	303)

session.add(travel3)
session.commit()

travel4 = TravelCompany( mode_id = 106, travel_id = 4, travel_name = "Air India" ,  travel_contact = 29559678 ,  num_tickets = 	103)

session.add(travel4)
session.commit()

travel5 = TravelCompany(mode_id = 106, travel_id = 5 , travel_name = "Go Air" ,   travel_contact =25790874,  num_tickets = 237)

session.add(travel5)
session.commit()
			
travel6 = TravelCompany(mode_id = 350 , travel_id = 6 , travel_name = "Shatabdi" ,  travel_contact =46985677,  num_tickets = 75 )
session.add(travel6)
session.commit()
			

travel7 = TravelCompany(mode_id = 301 , travel_id = 7 , travel_name = "Rajdhani" ,    travel_contact =27774457 ,  num_tickets = 309 )

session.add(travel7)
session.commit()
			

travel8 = TravelCompany( mode_id = 301 , travel_id = 8 , travel_name = "Charminar Express" ,    travel_contact = 22337335,  num_tickets =213)

session.add(travel8)
session.commit()


travel9 = TravelCompany(mode_id = 301 , travel_id = 9 , travel_name = "Duronto Express" ,  travel_contact = 44098711 ,  num_tickets = 220 )

session.add(travel9)
session.commit()

travel10 = TravelCompany( mode_id = 350 , travel_id = 10 , travel_name = "Garib Rath Express" ,  travel_contact =86741244 ,  num_tickets = 324)

session.add(travel10)
session.commit()		
 			

print ("added copmanies!")