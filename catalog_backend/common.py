#!/usr/bin/env python3

"""common.py"""

from threading import Thread
from time import sleep

from email.message import Message
from smtplib import SMTP, SMTPException
from string import Template
from jwt import encode as __jwt_encode__, decode as __jwt_decode__, \
                            DecodeError, InvalidAlgorithmError
from werkzeug.exceptions import BadRequest

from catalog_backend.environment import EMAIL_SENDER_FROM, EMAIL_SENDER_FROM_PASSWORD, \
                                        EMAIL_SMTP_HOST, EMAIL_SMTP_PORT, \
                                        JWT_SECRET, JWT_ALGORITHM
from catalog_backend.log import logging


FORGOT_HTML_FILE_PATH = "catalog_backend/static/common/send_email/forgot-password.html"


# JWT

def jwt_encode(json_dict):
    """jwt_encode function"""
    return __jwt_encode__(json_dict, JWT_SECRET, algorithm=JWT_ALGORITHM).decode("utf-8")


def jwt_decode(token):
    """jwt_decode function"""
    try:
        return __jwt_decode__(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except DecodeError as error:
        raise BadRequest('Error when decoding token. (error: ' + str(error) + ')')
    except InvalidAlgorithmError as error:
        raise BadRequest('Invalid algorithm. (error: ' + str(error) + ')')


# e-mail sender

def send_email(email_subject='[not-reply]', email_from=EMAIL_SENDER_FROM,
               email_from_password=EMAIL_SENDER_FROM_PASSWORD, email_to='test@test.com',
               email_content='Hello World!',
               email_smtp_host=EMAIL_SMTP_HOST, email_smtp_port=EMAIL_SMTP_PORT):
    """Sends an e-mail"""

    def __thread_send_email(email_subject, email_from, email_from_password,
                            email_to, email_content, email_smtp_host, email_smtp_port):
        msg = Message()

        msg['Subject'] = email_subject
        msg['From'] = email_from
        msg['To'] = email_to

        msg.add_header('Content-Type', 'text/html')
        msg.set_payload(email_content)

        logging.info('send_email() - sending an e-mail to `%s`...', email_to)

        try:
            s = SMTP(host=email_smtp_host, port=email_smtp_port)
            s.starttls()
            s.login(msg['From'], email_from_password)
            s.sendmail(msg['From'], [msg['To']], msg.as_string())
            s.quit()

            logging.info('send_email() - e-mail to `%s` has been sent successfully!', email_to)
        except SMTPException as error:
            logging.error('send_email() - unable to send an e-mail to `%s`.', email_to)
            logging.error('send_email() - error: `%s`.', error)
            raise error

    # wait X second(s) before sending an e-mail in order to avoid blocking the SMTP server
    sleep(1)

    thread = Thread(
        target=__thread_send_email,
        args=(email_subject, email_from, email_from_password, email_to, email_content,
              email_smtp_host, email_smtp_port,)
    )
    thread.start()


def send_email_forgot_password(email, link):
    """
    Sends an e-mail with a link to set a new password to the e-mail.

    email (str): user e-mail
    link (str): link to recover the password
    """

    logging.info('send_email_forgot_password() - sending an e-mail to `%s`.', email)

    # read the template file
    email_content_forgot_password = Template(open(FORGOT_HTML_FILE_PATH, "r").read())
    # substitute the variables inside the template, by changing the `$link` by `link`
    email_content_forgot_password = email_content_forgot_password.substitute(link=link)

    send_email(
        email_subject='[not-reply][forgot-password] Link to set a new passoword.',
        email_to=email,
        email_content=email_content_forgot_password
    )
