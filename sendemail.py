# login.txt should contain address on first line and app specific password on the second
# 
# username@gmail.com
# password123

def sendEmail(subject, message_):
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    with open("login.txt") as f:
        login = f.read().splitlines()

    gmailUser = login[0]
    gmailPassword = login[1]
    recipient = login[0]
    message = message_

    msg = MIMEMultipart()
    msg['From'] = gmailUser
    msg['To'] = recipient
    msg['Subject'] = subject
    msg.attach(MIMEText(message))

    mailServer = smtplib.SMTP('smtp.gmail.com', 587)
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.ehlo()
    mailServer.login(gmailUser, gmailPassword)
    mailServer.sendmail(gmailUser, recipient, msg.as_string())
    mailServer.close()