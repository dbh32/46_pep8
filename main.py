import email
import smtplib
import imaplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

GMAIL_SMTP = "smtp.gmail.com"
GMAIL_SMTP_PORT = 587
GMAIL_IMAP = "imap.gmail.com"


class Mail:
    def __init__(self, login,
                 password,
                 recipients,
                 subject='Subject',
                 message='Message',
                 header=None):
        self.login = login
        self.password = password
        self.subject = subject
        self.recipients = recipients
        self.message = message
        self.header = header

    def send_message(self, smtp_address=GMAIL_SMTP, smtp_port=GMAIL_SMTP_PORT):
        # send message
        msg = MIMEMultipart()
        msg['From'] = self.login
        msg['To'] = ', '.join(self.recipients)
        msg['Subject'] = self.subject
        msg.attach(MIMEText(self.message))

        smtp_client = smtplib.SMTP(smtp_address, smtp_port)
        # identify ourselves to smtp gmail client
        smtp_client.ehlo()
        # secure our email with tls encryption
        smtp_client.starttls()
        # re-identify ourselves as an encrypted connection
        smtp_client.ehlo()
        smtp_client.login(self.login, self.password)
        smtp_client.sendmail(self.login,
                             smtp_client, msg.as_string())
        smtp_client.quit()
        # send end

    def receive(self, imap_address=GMAIL_IMAP):
        # receive
        mail = imaplib.IMAP4_SSL(imap_address)
        mail.login(self.login, self.password)
        mail.list()
        mail.select("inbox")
        criterion = '(HEADER Subject "%s")' % self.header if self.header else 'ALL'
        result, data = mail.uid('search', None, criterion)
        assert data[0], 'There are no letters with current header'
        latest_email_uid = data[0].split()[-1]
        result, data = mail.uid('fetch', latest_email_uid, '(RFC822)')
        raw_email = data[0][1]
        email.message_from_string(raw_email)
        mail.logout()
        # end receive


if __name__ == '__main__':
    letter = Mail('login@gmail.com', 'qwerty', ('vasya@email.com', 'petya@email.com'))
