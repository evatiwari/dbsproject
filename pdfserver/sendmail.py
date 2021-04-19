import yagmail
from fpdf import FPDF

def sendmail(travelbooking,company,receiver):
    #generatetravel(travelbooking,company)
    pdf=FPDF()
    pdf.add_page()
    pdf.set_xy(0,0)
    pdf.set_font('arial','B',16.0)
    content="Travel Company: "+company.travel_name
    pdf.cell(ln=0, h=5.0, align='L', w=0, txt=content, border=0)
    #content="Mode: "+travelbooking.mode_of_transport
    #pdf.cell(ln=0, h=5.0, align='L', w=0, txt=content, border=0)
    content="Location: "+travelbooking.from_dest
    pdf.cell(ln=0, h=5.0, align='L', w=0, txt=content, border=0)
    content="Destination: "+travelbooking.to_dest
    pdf.cell(ln=0, h=5.0, align='L', w=0, txt=content, border=0)
    content="Date of travel: "+str(travelbooking.arrival_date)
    pdf.cell(ln=0, h=5.0, align='L', w=0, txt=content, border=0)
    content="Number of tickets: "+str(travelbooking.num_tickets)
    pdf.cell(ln=0, h=5.0, align='L', w=0, txt=content, border=0)
    content="Total price: "+str(travelbooking.totprice)
    pdf.cell(ln=0, h=5.0, align='L', w=0, txt=content, border=0)
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