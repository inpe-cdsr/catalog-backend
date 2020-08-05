#!/usr/bin/env python3

"""common.py"""

from threading import Thread
from time import sleep

import email.message
from smtplib import SMTP, SMTPException
from jwt import encode as __jwt_encode__, decode as __jwt_decode__, \
                            DecodeError, InvalidAlgorithmError
from werkzeug.exceptions import BadRequest

from catalog_backend.environment import EMAIL_SENDER_FROM, EMAIL_SENDER_FROM_PASSWORD, \
                                        EMAIL_SMTP_HOST, EMAIL_SMTP_PORT, \
                                        JWT_SECRET, JWT_ALGORITHM
from catalog_backend.log import logging

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
        msg = email.message.Message()

        msg['Subject'] = email_subject
        msg['From'] = email_from
        msg['To'] = email_to

        msg.add_header('Content-Type', 'text/html')
        msg.set_payload(email_content)

        logging.info('send_email() - sending an e-mail to `%s`.', email_to)

        try:
            s = SMTP(host=email_smtp_host, port=email_smtp_port)
            s.starttls()
            s.login(msg['From'], email_from_password)
            s.sendmail(msg['From'], [msg['To']], msg.as_string())
            s.quit()

            logging.info('send_email() - e-mail to `%s` has been sent successfully', email_to)
        except SMTPException as error:
            logging.error('send_email() - unable to send an e-mail to `%s`.', email_to)
            logging.error('send_email() - error: `%s`.', error)
            raise error

    thread = Thread(
        target=__thread_send_email,
        args=(email_subject, email_from, email_from_password, email_to, email_content,
              email_smtp_host, email_smtp_port,)
    )
    thread.start()

    # wait X second(s) after sending an e-mail in order to avoid blocking the SMTP server
    sleep(1)


email_content_forgot_password = """
<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">

        <title>CDSR E-mail Newsletter</title>
        <style type="text/css">
            a {color: #d80a3e;}
            body, #header h1, #header h2, p {margin: 0; padding: 0;}
            #main {border: 1px solid #cfcece;}
            img {display: block;}
            #top-message p, #bottom p {color: #3f4042; font-size: 12px; font-family: Arial, Helvetica, sans-serif; }
            #header h1 {color: #ffffff !important; font-family: "Lucida Grande", sans-serif; font-size: 24px; margin-bottom: 0!important; padding-bottom: 0; }
            #header p {color: #ffffff !important; font-family: "Lucida Grande", "Lucida Sans", "Lucida Sans Unicode", sans-serif; font-size: 12px;  }
            h5 {margin: 0 0 0.8em 0;}
            h5 {font-size: 18px; color: #444444 !important; font-family: Arial, Helvetica, sans-serif; }
            p {font-size: 12px; color: #444444 !important; font-family: "Lucida Grande", "Lucida Sans", "Lucida Sans Unicode", sans-serif; line-height: 1.5;}
        </style>
    </head>

    <body>
        <table width="100%" cellpadding="0" cellspacing="0" bgcolor="e4e4e4"><tr><td>
        <table id="top-message" cellpadding="20" cellspacing="0" width="600" align="center">
            <tr>
            <td align="center">
                <p><a href="#">View in Browser</a></p>
            </td>
            </tr>
        </table>

        <table id="main" width="600" align="center" cellpadding="0" cellspacing="15" bgcolor="ffffff">
            <tr>
            <td>
                <table id="header" cellpadding="10" cellspacing="0" align="center" bgcolor="8fb3e9">
                <tr>
                    <td width="570" align="center"  bgcolor="#d80a3e"><h1>Evanto Limited</h1></td>
                </tr>
                <tr>
                    <td width="570" align="right" bgcolor="#d80a3e"><p>November 2017</p></td>
                </tr>
                </table>
            </td>
            </tr>

            <tr>
            <td>
                <table id="content-3" cellpadding="0" cellspacing="0" align="center">
                <tr>
                    <td width="250" valign="top" bgcolor="d0d0d0" style="padding:5px;">
                    <img src="https://thumbsplus.tutsplus.com/uploads/users/30/posts/29520/preview_image/pre.png" width="250" height="150"  />
                    </td>
                    <td width="15"></td>
                    <td width="250" valign="top" bgcolor="d0d0d0" style="padding:5px;">
                        <img src="https://cms-assets.tutsplus.com/uploads/users/30/posts/29642/preview_image/vue-2.png" width ="250" height="150" />
                    </td>
                </tr>
                </table>
            </td>
            </tr>
            <tr>
            <td>
                <table id="content-4" cellpadding="0" cellspacing="0" align="center">
                <tr>
                    <td width="200" valign="top">
                    <h5>How to Get Up and Running With Vue</h5>
                    <p>In the introductory post for this series we spoke a little about how web designers can benefit by using Vue. In this tutorial we will learn how to get Vue up..</p>
                    </td>
                    <td width="15"></td>
                    <td width="200" valign="top">
                    <h5>Introducing Haiku: Design and Create Motion</h5>
                    <p>With motion on the rise amongst web developers so too are the tools that help to streamline its creation. Haiku is a stand-alone..</p>
                    </td>
                </tr>
                </table>
            </td>
            </tr>
        </table>

        <table id="bottom" cellpadding="20" cellspacing="0" width="600" align="center">
            <tr>
            <td align="center">
                <p>Design better experiences for web & mobile</p>
                <p><a href="#">Unsubscribe</a> | <a href="#">Tweet</a> | <a href="#">View in Browser</a></p>
            </td>
            </tr>
        </table><!-- top message -->
        </td></tr></table><!-- wrapper -->
    </body>
</html>
"""

def send_email_forgot_password(email_to):
    """Sends an e-mail with a link to set a new password to the e-mail."""

    logging.info('send_email_forgot_password() - sending an e-mail to `%s`.', email_to)

    send_email(
        email_subject='[not-reply][forgot-password] Link to set a new passoword.',
        email_to=email_to,
        email_content=email_content_forgot_password
    )
