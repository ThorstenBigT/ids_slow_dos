"""This module send a email notification if an attack is detected.
    Adapted from:
        https://docs.python.org/3/library/email.examples.html
        [last accessed December 2021]

    Author: Thorsten Steuer
    Licence: Apache 2.0
"""
import smtplib
from email.message import EmailMessage

from beartype import beartype


EMAIL = 'ids_masterarbeit@gmx.at'
EMAIL_PASS ='cYqBUB5L'
EMAIL_SUBJECT = 'INTRUSION DETECTED!!!!'

class AlarmNotification:
    """ A class to send a Email Message once an intrusion was detected.
    """

    @beartype
    def stop_smtp(self):
        """Stop smtp client.
        """
        self.email_server.quit()

    @beartype
    def connect_to_smtp_server(self):
        """Connects to a smtp sever.
        """
        self.email_server = smtplib.SMTP(host='mail.gmx.net', port=587)
        self.email_server.starttls()
        self.email_server.login(EMAIL, EMAIL_PASS)

    @beartype
    def send_email(self, message: str):
        """Is Sending an Email with the provided message string.

        Args:
            message (str): [description]
        """
        msg = EmailMessage()
        msg.set_content(message)
        msg['Subject'] = EMAIL_SUBJECT
        msg['From'] = EMAIL
        msg['To'] = EMAIL

        self.email_server.send_message(msg)

if __name__ == '__main__':
    email_server = AlarmNotification()
    email_server.connect_to_smtp_server()
    email_server.send_email("TEST")
    email_server.stop_smtp()
