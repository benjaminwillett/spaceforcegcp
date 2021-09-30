import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


class grouponmessage(object):

    def __init__(self, sender_email="", receiver_email=""):

        try:
            self.sender_email = sender_email
            self.receiver_email = receiver_email
            message = MIMEMultipart()
            message['From'] = sender_email
            message['To'] = receiver_email
            message['Subject'] = 'A test mail sent by Python. It has an attachment.'
            mail_content = '''Hello,
        This is a test mail.
        In this mail we are sending some attachments.
        The mail is sent using Python SMTP library.
        Thank You
        '''

            message.attach(MIMEText(mail_content, 'plain'))
            attach_file_name = 'static/js/Chart.min.js'
            attach_file = open(attach_file_name, 'rb')
            payload = MIMEBase('application', 'octate-stream')
            payload.set_payload((attach_file).read())
            encoders.encode_base64(payload)
            payload.add_header('Content-Decomposition', 'attachment', filename=attach_file_name)
            message.attach(payload)
            text = message.as_string()

            port = 587
            key = "Distort3192!"
            server = smtplib.SMTP(host="smtp-mail.outlook.com", port=port)
            server.starttls()
            server.login("ben.willett@distortenterprises.com", key)

            server.sendmail(sender_email, receiver_email, text)
            server.quit()
        except:
            print("could't setup mail connection")
            pass