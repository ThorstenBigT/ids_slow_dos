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

NEO4J_URI = 'bolt://localhost:7687'
NEO4J_USER = 'neo4j'
NEO4J_PASS = 'gh1KLaqw'
# CHANGE PASSWORDS BEFORE PUBLISHING!!!!!!!!!!!!!!!!!!!!!!!!!!!
EMAIL = 'thorsten.steuer@gmx.net'
EMAIL_PASS ='gh!KLaqw'
EMAIL_SUBJECT = 'INTRUSION DETECTED!!!!'

class AlarmNotification:
    """[summary]
    """
    @beartype
    def __init__(self):
        """[summary]
        """
        self.email_server = smtplib.SMTP(host='mail.gmx.net', port=587)
        self.email_server.starttls()
        self.email_server.login(EMAIL, EMAIL_PASS)

    @beartype
    def stop_smtp(self):
        """[summary]
        """
        self.email_server.quit()

    @beartype
    def send_email(self, message: str):
        """[summary]

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
    email_server.send_email("TEST")
    email_server.stop_smtp()
