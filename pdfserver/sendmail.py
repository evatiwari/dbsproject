import yagmail
from fpdf import FPDF

yagmail.register('kdeepthi8569@gmail.com', 'iamdeepti')

def sendmail(travelbooking,company,mode, receiver):
    #generatetravel(travelbooking,company)
    pdf=FPDF()
    pdf.add_page()
    pdf.set_xy(10,10)

    pdf.set_font('arial','B',18.0)
    content="Your Ticket to Destination"
    pdf.cell(ln=1, h=5.0, align='L', w=0, txt=content, border=0)
    pdf.cell(ln=1, h=5.0, align='L', w=0, txt="\n", border=0)


    pdf.set_font('arial','B',16.0)
    content="Travel Company: "+company.travel_name
    pdf.cell(ln=1, h=5.0, align='L', w=0, txt=content, border=0)
    pdf.cell(ln=1, h=5.0, align='L', w=0, txt="\n", border=0)

    content="Mode: "+mode.mode_of_transport
    pdf.cell(ln=1, h=5.0, align='L', w=0, txt=content, border=0)
    pdf.cell(ln=1, h=5.0, align='L', w=0, txt="\n", border=0)
    
    content="Location: "+travelbooking.from_dest
    pdf.cell(ln=1, h=5.0, align='L', w=0, txt=content, border=0)
    pdf.cell(ln=1, h=5.0, align='L', w=0, txt="\n", border=0)
    
    content="Destination: "+travelbooking.to_dest
    pdf.cell(ln=1, h=5.0, align='L', w=0, txt=content, border=0)
    pdf.cell(ln=1, h=5.0, align='L', w=0, txt="\n", border=0)
    
    content="Date of Departure: "+str(travelbooking.depart_date)
    pdf.cell(ln=1, h=5.0, align='L', w=0, txt=content, border=0)
    pdf.cell(ln=1, h=5.0, align='L', w=0, txt="\n", border=0)

    content="Date of Arrival: "+str(travelbooking.arrival_date)
    pdf.cell(ln=1, h=5.0, align='L', w=0, txt=content, border=0)
    pdf.cell(ln=1, h=5.0, align='L', w=0, txt="\n", border=0)
    
    content="Number of tickets: "+str(travelbooking.num_tickets)
    pdf.cell(ln=1, h=5.0, align='L', w=0, txt=content, border=0)
    pdf.cell(ln=1, h=5.0, align='L', w=0, txt="\n", border=0)
    
    content="Total price: "+str(travelbooking.totprice)
    pdf.cell(ln=1, h=5.0, align='L', w=0, txt=content, border=0)
    pdf.cell(ln=1, h=5.0, align='L', w=0, txt="\n", border=0)
    
    filename=str(travelbooking.booking_id)+".pdf"
    pdf.output(filename,'F')
    body="Please find attached your tickets. Bon Voyage!"
    yag = yagmail.SMTP("mohan666420@gmail.com")
    yag.send(
        to=receiver,
        subject="Your reservation has been confirmed",
        contents=body,
        attachments=filename,
    )

def hotelreservation(hoteldetails,hotelbooking,roomtype,receiver):
    #generatetravel(travelbooking,company)
    pdf=FPDF()
    pdf.add_page()
    pdf.set_xy(10,10)

    pdf.set_font('arial','B',18.0)
    content="Your Hotel Reservation"
    pdf.cell(ln=1, h=5.0, align='L', w=0, txt=content, border=0)
    pdf.cell(ln=1, h=5.0, align='L', w=0, txt="\n", border=0)


    pdf.set_font('arial','B',16.0)
    content="Hotel Name: "+hoteldetails.hotel_name
    pdf.cell(ln=1, h=5.0, align='L', w=0, txt=content, border=0)
    pdf.cell(ln=1, h=5.0, align='L', w=0, txt="\n", border=0)

    content="City: "+hoteldetails.hotel_city
    pdf.cell(ln=1, h=5.0, align='L', w=0, txt=content, border=0)
    pdf.cell(ln=1, h=5.0, align='L', w=0, txt="\n", border=0)
    
    content="Address: "+hoteldetails.hotel_addr
    pdf.cell(ln=1, h=5.0, align='L', w=0, txt=content, border=0)
    pdf.cell(ln=1, h=5.0, align='L', w=0, txt="\n", border=0)
    
    content="Contact number: "+hoteldetails.hotel_contact
    pdf.cell(ln=1, h=5.0, align='L', w=0, txt=content, border=0)
    pdf.cell(ln=1, h=5.0, align='L', w=0, txt="\n", border=0)
    
    content="Date of check-in "+str(hotelbooking.check_in)
    pdf.cell(ln=1, h=5.0, align='L', w=0, txt=content, border=0)
    pdf.cell(ln=1, h=5.0, align='L', w=0, txt="\n", border=0)

    content="Date of check-out: "+str(hotelbooking.check_out)
    pdf.cell(ln=1, h=5.0, align='L', w=0, txt=content, border=0)
    pdf.cell(ln=1, h=5.0, align='L', w=0, txt="\n", border=0)
    
    content="Room type: "+roomtype.room_type
    pdf.cell(ln=1, h=5.0, align='L', w=0, txt=content, border=0)
    pdf.cell(ln=1, h=5.0, align='L', w=0, txt="\n", border=0)
    
    content="Number of rooms: "+str(hotelbooking.num_rooms)
    pdf.cell(ln=1, h=5.0, align='L', w=0, txt=content, border=0)
    pdf.cell(ln=1, h=5.0, align='L', w=0, txt="\n", border=0)

    content="Total price: "+str(hotelbooking.totprice)
    pdf.cell(ln=1, h=5.0, align='L', w=0, txt=content, border=0)
    pdf.cell(ln=1, h=5.0, align='L', w=0, txt="\n", border=0)
    
    filename=str(hotelbooking.booking_id)+".pdf"
    pdf.output(filename,'F')
    body="Please find attached your hotel reservation details. Enjoy your stay!"
    yag = yagmail.SMTP("mohan666420@gmail.com")
    yag.send(
        to=receiver,
        subject="Your reservation has been confirmed",
        contents=body,
        attachments=filename,
    )