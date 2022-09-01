import smtplib
from email.message import EmailMessage
import imghdr

class Message():
    def __init__(self):
        self.sender="" #INPUT OUTLOOK EMAIL
        self.password='' #INPUT OUTLOOK EMAIL PASSWORD
        self.reciver='' #INPUT WHERE YOU WANT THE EMAIL TO GO
        subject = "Person Detected!"
        body = 'There was motion detected on your security camera. We attached an image of the motion below.'
        self.message = f'Subject: {subject}\n\n{body}'
        self.newMessage = EmailMessage()
        self.newMessage['Subject'] = subject #Defining email subject
        self.newMessage['From'] = self.sender  #Defining sender email
        self.newMessage['To'] = self.reciver  #Defining reciever email
        self.newMessage.set_content(body) #Defining email body

class Email():
    def __init__(self):
        pass
    def sendEmail(self,image_name):
        message = Message()
        with open(f'/images/{image_name}.png', 'rb') as f:
            image_data = f.read()
            image_type = imghdr.what(f.name)
            image_name = 'MotionDectectionImage.png'
        with smtplib.SMTP(host='smtp-mail.outlook.com', port=587) as self.smtp:
            self.smtp.ehlo()     #Identify ourselves with the mail server we are using.
            self.smtp.starttls() #Encrypt our connection
            self.smtp.ehlo()
            self.smtp.login(message.sender, message.password)
            message.newMessage.add_attachment(image_data, maintype='image', subtype=image_type, filename=image_name)
            self.smtp.send_message(message.newMessage)
        print('email sent')
