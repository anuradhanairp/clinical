# To change this template, choose Tools | Templates
# and open the template in the editor.


import smtplib
import os
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import formatdate
from email import Encoders


class ConnectionError(smtplib.SMTPException): pass
class LoginError(smtplib.SMTPException): pass
class DisconnectionError(smtplib.SMTPException): pass
class EmailSendError(smtplib.SMTPException): pass

COMASPACE=', ' # Used to convert list of recipient into string email addresses seperated with "," and "space".

class Smtp:

        '''
        SMTP class, specify all informations require to send a mail.This script use systems default mailing application
        to send mails.The relying of mail via other servers are now disabled.

        This class have following set of methods to complete to mail construction and sending process.
        1.connect()
        2.send()
        3.close()
        4.subject()
        5.from_addr()
        6.rcpt_to()
        7.load_attachments()
        '''

        def __init__(self,host='localhost', user='', password='', port=25):
                self._host        = host
                self._port        = port
                self._user        = user
                self._password    = password

                self._message     = ''
                self._subject     = ''
                self._from_addr   = ''
                self._rcpt_to     = ''
                self._server      = ''
                self._attachments = []

                #atexit.register(close) #our close() method will be automatically executed upon normal interpreter termination

                self.connect()


        def connect(self):
            
                 if self._host != '':

                        try:
                                self._server = smtplib.SMTP(self._host, self._port)

                        except smtplib.SMTPException, e:
                                raise ConnectionError("Connection failed!")
                        '''
                        try:
                                self._server.login(self._user, self._password)

                        except smtplib.SMTPException, e:
                                raise LoginError("Login Failed!")
                        '''


        def close(self):

                if self._server:
                        try:
                                self._server.quit()

                        except smtplib.SMTPException, e:
                                raise DisconnectionError("Disconnection failed!")


        def message(self, message):
                self._message = message


        def subject(self, subject):
                self._subject = subject


        def from_addr(self, email):
                self._from_addr = email


        def rcpt_to(self, email):
                self._rcpt_to = email
                


        def attach(self, file):
                if os.path.exists(file):
                        self._attachments.append(file)


        def load_attachments(self, m_message):
                for file in self._attachments:
                        part = MIMEBase('application', "octet-stream")
                        part.set_payload(open(file,"rb").read())
                        Encoders.encode_base64(part)
                        part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(file))
                        m_message.attach(part)

                return m_message


        def send(self, content_type='plain'):   #Remove the charset UFT-8 to avoid the encoding of the mail.Only encode the mail only when neccessary.

                if self._message and self._subject and self._from_addr and self._rcpt_to:

                        m_message             = MIMEMultipart()

                        m_message['From']     = self._from_addr
                        m_message['To']       = " ,".join(self._rcpt_to)
                        m_message['Date']     = formatdate(localtime=True)
                        m_message['Subject']  = self._subject
                        m_message['X-Mailer'] = "Python X-Mailer"

                        m_message.attach(MIMEText(self._message, content_type))
                        m_message = self.load_attachments(m_message)

                        try:
                                self._server.sendmail(self._from_addr, self._rcpt_to, m_message.as_string())

                        except smtplib.SMTPException, e:
                                raise EmailSendError("Email has not been sent")

if __name__ == "__main__":
    print "Hello World";
    p=Smtp('localhost','','');  #If user is not given then it will take user who running this script.
    print 'Sending mails'
    p.subject('From python smtp class');
    p.from_addr('haridas@sparksupport.com');
    p.rcpt_to('haridas.nss@gmail.com')
    p.message('Test mail')
    #p.send()
    p.close()