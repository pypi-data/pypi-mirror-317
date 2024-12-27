# Email Sender for Verification
# Python Email Sender Verification 
# Author: Christian Garcia

# Import required libraries
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import requests

class EmailSender:
  
    def __init__(self, api_key=None):
        # Server and port
        self.smtp_server = 'smtp.gmail.com'
        self.smtp_port = 587

        # Email configuration
        self.default_app_email = 'emailsender880@gmail.com'
        self.default_app_pswd = 'jzio inzq lhqg azeg'

        # Configure user API key
        self.api_key = api_key

        # Verify API key
        if not self.api_key:
            raise ValueError("An API key is required to send emails.")
        
        if not self.validate_apikey():
            raise PermissionError("Invalid API key. Please generate a valid API key from https://emailsender000.pythonanywhere.com/")

    def validate_apikey(self):
        # Validate the API key with the external service
        response = requests.post(
            'https://emailsender000.pythonanywhere.com/api/validate',
            json={'api_key': self.api_key}
        )
        return response.status_code == 200

    def send_email(self, email_reciever, msg_subject="Sample Message", msg_body="This is a sample message from EmailSender.", sender_name="EmailSender"):
        # Create email message
        message = MIMEMultipart()
        message['From'] = f'{sender_name} <{self.default_app_email}>'
        message['To'] = email_reciever
        message['Subject'] = msg_subject
        message.attach(MIMEText(msg_body, 'plain'))

        # Send email by establishing connection
        try:
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.default_app_email, self.default_app_pswd)
            server.sendmail(self.default_app_email, email_reciever, message.as_string())
            print('Email sent successfully!')
        except Exception as e:
            print(f'Failed to send email: {e}')
        finally:
            server.quit()
