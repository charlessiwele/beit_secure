import os
import smtplib
from email.message import EmailMessage
from email.mime.application import MIMEApplication

from settings import EMAIL_SMTP_SERVER, SENDER_EMAIL, SENDER_EMAIL_PASSWORD, BCC_EMAIL_RECIPIENTS, \
    EMAIL_RETRIES_COUNT


class EmailManager:
    email_retries_count = 0

    def send_email_with_pdf_attachments(self,
            email_recipients,
            sender_email=SENDER_EMAIL,
            sender_password=SENDER_EMAIL_PASSWORD,
            bcc_email_recipients=(BCC_EMAIL_RECIPIENTS,),
            email_subject=None,
            attachment_file_path=None,
            email_body=None):

        email_user = sender_email
        password = sender_password

        email_send = email_recipients
        bcc_email_send = bcc_email_recipients
        subject = email_subject

        msg = EmailMessage()
        msg['From'] = email_user
        msg['To'] = email_send
        msg['Cc'] = bcc_email_send
        msg['Subject'] = subject

        body = email_body
        msg.set_content(body)
        try:
            if os.path.isdir(attachment_file_path):
                for file_name in os.listdir(attachment_file_path):  # add files to the message
                    file_path = os.path.join(file_name, attachment_file_path)
                    #  Open file, read file, attach file to email object
                    file_name = os.path.basename(file_path)
                    subtype = file_name.split()[-1]
                    content_file = MIMEApplication(open(file_path, "rb").read(), _subtype=subtype)
                    content_file.add_header('Content-Disposition', 'attachment', filename=file_name)
                    msg.add_attachment(content_file, subtype=subtype, filename=file_name)
            elif os.path.isfile(attachment_file_path):
                file_name = os.path.basename(attachment_file_path)
                subtype = file_name.split()[-1]
                content_file = MIMEApplication(open(attachment_file_path, "rb").read(), _subtype=subtype)
                content_file.add_header('Content-Disposition', 'attachment', filename=file_name)
                msg.add_attachment(content_file, subtype=subtype, filename=file_name)

            text = msg.as_string()
            # use gmail with port
            server = smtplib.SMTP(EMAIL_SMTP_SERVER)
            # enable security
            server.starttls()
            # login with mail_id and password
            server.login(email_user, password)
            # send email
            server.sendmail(email_user, email_send, text)
            # close smtp server  instance
            server.close()
        except Exception as e:
            print(e)
            if self.email_retries_count < EMAIL_RETRIES_COUNT:
                self.email_retries_count += 1
                self.send_email_with_pdf_attachments(
                    email_recipients,
                    sender_email=sender_email,
                    sender_password=sender_password,
                    bcc_email_recipients=bcc_email_recipients,
                    email_subject=email_subject,
                    attachment_file_path=attachment_file_path,
                    email_body=email_body)
            return str(e)
