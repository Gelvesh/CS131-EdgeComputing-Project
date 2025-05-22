import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from pyfcm import FCMNotification

class NotificationService:
    def __init__(self, config):
        self.email_config = config['email']
        self.fcm_config = config['fcm']
        self.push_service = FCMNotification(api_key=self.fcm_config['api_key'])
    
    def send_email(self, to, subject, body, attachment=None):
        msg = MIMEMultipart()
        msg['From'] = self.email_config['sender']
        msg['To'] = to
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'html'))
        
        if attachment:
            self._attach_file(msg, attachment)
        
        try:
            with smtplib.SMTP(self.email_config['server'], self.email_config['port']) as server:
                server.starttls()
                server.login(self.email_config['user'], self.email_config['password'])
                server.send_message(msg)
            return True
        except Exception as e:
            print(f"Email error: {e}")
            return False
    
    def send_push(self, device_ids, title, message):
        return self.push_service.notify_multiple_devices(
            registration_ids=device_ids,
            message_title=title,
            message_body=message
        )