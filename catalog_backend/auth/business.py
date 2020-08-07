"""business.py"""

from secrets import token_urlsafe
from werkzeug.exceptions import NotFound

from catalog_backend.common import jwt_encode, send_email_forgot_password
from catalog_backend.environment import URL_CATALOG_RESET_PASSWORD
from catalog_backend.log import logging
from catalog_backend.model import DatabaseConnection


class AuthBusiness():

    def __init__(self):
        self.db_connection = DatabaseConnection()


class AuthLoginBusiness(AuthBusiness):

    def login(self, email, password):
        logging.info('AuthLoginBusiness.login()\n')

        result = self.db_connection.select_user(email=email, password=password)

        # if an empty list (i.e. result == []), then raise an exception
        if not result:
            raise NotFound('E-mail or Password was not found.')

        # get the only one available result
        result = result[0]

        logging.info('AuthLoginBusiness.login() - result[\'email\']: %s', result['email'])

        encoded_token = jwt_encode(result)

        return encoded_token, result


class AuthForgotPasswordBusiness(AuthBusiness):

    def send_an_email_to(self, email):
        logging.info('AuthForgotPasswordBusiness.send_an_email_to()')

        user = self.db_connection.select_user(email=email)

        # if an empty list (i.e. user == []), then raise an exception
        if not user:
            logging.error('AuthForgotPasswordBusiness.send_an_email_to() - e-mail was not found.')
            raise NotFound('E-mail was not found.')

        token = token_urlsafe(32)

        # save the token in the database
        self.db_connection.insert_security(user[0]['userId'], token)

        link = URL_CATALOG_RESET_PASSWORD + '?token={}'.format(token)

        logging.info('AuthForgotPasswordBusiness.send_an_email_to() - link: %s', link)

        send_email_forgot_password(email, link)

        return token


class AuthResetPasswordBusiness(AuthBusiness):

    def reset_password(self, email, password, token, **kwargs):
        logging.info('AuthResetPasswordBusiness.reset_password()')

        logging.info('AuthResetPasswordBusiness.reset_password() - email: %s', email)
        # logging.debug('AuthResetPasswordBusiness.reset_password() - password: %s', password)
        logging.info('AuthResetPasswordBusiness.reset_password() - token: %s', token)

        user = self.db_connection.select_user(email=email)

        # if an empty list (i.e. user == []), then raise an exception
        if not user:
            logging.error('AuthResetPasswordBusiness.reset_password() - e-mail was not found.')
            raise NotFound('E-mail was not found.')

        user_id = user[0]['userId']

        security = self.db_connection.select_security(user_id=user_id, token=token)

        logging.info('AuthResetPasswordBusiness.reset_password() - security: %s', security)

        # if an empty list (i.e. user == []), then raise an exception
        if not security:
            logging.error('AuthResetPasswordBusiness.reset_password() - token was not found.')
            raise NotFound('Token was not found.')

        # update the user password
        self.db_connection.update_user(user_id=user_id, password=password)

        logging.info(
            'AuthResetPasswordBusiness.reset_password() - user password has been reset successfully!'
        )

        # delete the token from the database
        self.db_connection.delete_security(user_id=user_id, token=token)

        logging.info(
            'AuthResetPasswordBusiness.reset_password() - user token has been removed successfully!'
        )
