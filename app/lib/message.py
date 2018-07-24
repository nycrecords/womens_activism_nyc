from flask_mail import Message

@app.route("/")
def message():

    msg = Message("WomensActivism - New Subscribe",
                  recipients=["womensactivism@records.nyc.gov"])
    msg.body = "First Name: ",
               "Last Name: ",
               "Email Address: ",
               "Phone Number: ",
