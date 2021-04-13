import yagmail

def sendmail(receiver):
    body = "This is Eva, the email sending thingy has been set up :) Just need to figure out the body :3"
    yag = yagmail.SMTP("mohan666420@gmail.com")
    yag.send(
        to=receiver,
        subject="Boo!",
        contents=body,
    )

sendmail("f20180790@hyderabad.bits-pilani.ac.in")
sendmail("f20180886@hyderabad.bits-pilani.ac.in")
sendmail("f20180936@hyderabad.bits-pilani.ac.in")