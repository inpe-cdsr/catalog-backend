"""
DGI Catalog
"""

from datetime import date, datetime

# from mysql.connector import connect, errorcode, Error
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import text

from werkzeug.exceptions import InternalServerError

from dgi_catalog.environment import MYSQL_DB_USER, MYSQL_DB_PASSWORD, \
                                    MYSQL_DB_HOST, MYSQL_DB_PORT, \
                                    MYSQL_DB_DATABASE
from dgi_catalog.exception import DatabaseConnectionException
from dgi_catalog.log import logging


def fix_rows(rows):
    for row in rows:
        for key in row:
            # datetime/date is not serializable by default, then it gets a serializable string representation
            if isinstance(row[key], (datetime, date)):
                row[key] = row[key].isoformat()

    return rows


def mysql_old_password(password):
    nr = 1345345333
    add = 7
    nr2 = 0x12345671

    for c in (ord(x) for x in password if x not in (' ', '\t')):
        nr^= (((nr & 63)+add)*c)+ (nr << 8) & 0xFFFFFFFF
        nr2= (nr2 + ((nr2 << 8) ^ nr)) & 0xFFFFFFFF
        add= (add + c) & 0xFFFFFFFF

    return "%08x%08x" % (nr & 0x7FFFFFFF,nr2 & 0x7FFFFFFF)


class DatabaseConnection():
    # Source: https://dev.mysql.com/doc/connector-python/en/connector-python-example-connecting.html

    def __init__(self):
        self.engine = None

    def connect(self):
        try:
            self.engine = create_engine('mysql://{}:{}@{}:{}/{}'.format(
                MYSQL_DB_USER, MYSQL_DB_PASSWORD, MYSQL_DB_HOST,
                MYSQL_DB_PORT, MYSQL_DB_DATABASE
            ))

        except SQLAlchemyError as error:
            error_message = 'An error occurred during database connection'

            logging.error('DatabaseConnection.connect() - error.code: %s', error.code)
            logging.error('DatabaseConnection.connect() - error.args: %s', error.args)
            logging.error('DatabaseConnection.connect() - %s: %s\n', error_message, error)

            error_message += ': ' + str(error.args)

            self.close()
            raise InternalServerError(error_message)

    def close(self):
        if self.engine is not None:
            self.engine.dispose()

        self.engine = None

    # def commit(self):
    #     self.engine.commit()

    # def rollback(self):
    #     self.engine.rollback()

    def try_to_connect(self):
        attempt = 0

        # while engine is None, try to connect
        while self.engine is None and attempt < 3:
            attempt += 1
            self.connect()

        if attempt >= 3:
            self.close()
            raise DatabaseConnectionException('Connection was not opened to the database.')

    def execute(self, query, params=None, is_transaction=False):
        logging.info('DatabaseConnection.execute()')

        # sometimes there are a lot of blank spaces, then I remove it
        query = query.replace('            ', '')

        # logging.info('DatabaseConnection.execute() - query: %s', query)
        # logging.debug('DatabaseConnection.execute() - params: %s', params)
        logging.info('DatabaseConnection.execute() - is_transaction: %s', is_transaction)

        try:
            # if query is a transaction statement, then commit the changes
            if is_transaction:
                query_text = text(query).execution_options(autocommit=True)
            else:
                query_text = text(query)

            logging.info('DatabaseConnection.execute() - query_text: %s', query_text)

            self.try_to_connect()

            # cursor.execute(query, params=params)
            result = self.engine.execute(query_text, params)

            logging.info('DatabaseConnection.execute() - result.returns_rows: %s', result.returns_rows)
            logging.info('DatabaseConnection.execute() - result.rowcount: %s', result.rowcount)
            logging.info('DatabaseConnection.execute() - result.lastrowid: %s', result.lastrowid)

            if result.returns_rows:
                # SELECT clause
                rows = result.fetchall()
                rows = [dict(row) for row in rows]

                # logging.info('DatabaseConnection.execute() - rows: \n%s\n', rows)

                return rows
            else:
                # INSERT, UPDATE and DELETE operations need to be committed
                # if 'query' was a 'INSERT' statement, then it returns the inserted record 'id',
                # else it returns '0'
                return str(result.lastrowid)

        except SQLAlchemyError as error:
            # self.rollback()
            error_message = 'An error occurred during query execution'

            logging.error('DatabaseConnection.execute() - error.code: %s', error.code)
            logging.error('DatabaseConnection.execute() - error.args: %s', error.args)
            logging.error('DatabaseConnection.execute() - %s: %s\n', error_message, error)

            error_message += ': ' + str(error.args)

            raise InternalServerError(error_message)

        # finally is always executed (both at try and except)
        finally:
            self.close()
            # print('Database connection was closed.')

    def select_user(self, email=None, password=None):
        # Sources:
        # https://dev.mysql.com/doc/connector-python/en/connector-python-example-cursor-select.html
        # https://dev.mysql.com/doc/connector-python/en/connector-python-api-mysqlcursor-execute.html

        query = '''
            SELECT * FROM User
            WHERE email=:email AND password=:password
        '''

        params = {'email': email, 'password': mysql_old_password(password)}

        # execute the query and fix the resulted rows
        return fix_rows(self.execute(query, params))

    def select_user_by_email(self, email=None):
        # Sources:
        # https://dev.mysql.com/doc/connector-python/en/connector-python-example-cursor-select.html
        # https://dev.mysql.com/doc/connector-python/en/connector-python-api-mysqlcursor-execute.html

        query = '''
            SELECT * FROM User
            WHERE email=:email
        '''

        params = { 'email': email }

        # execute the query and fix the resulted rows
        return fix_rows(self.execute(query, params))

    def insert_user(self, email=None, password=None, fullname='', cnpjCpf='',
                    areaCode='', phone='', company='', companyType='',
                    activity='', userType='', addressId=None, userStatus=''):
        # Source: https://dev.mysql.com/doc/connector-python/en/connector-python-example-cursor-transaction.html

        query = '''
            INSERT INTO User (
                userId, email, password, fullname, CNPJ_CPF,
                areaCode, phone, company, companyType,
                activity, userType, registerDate, addressId,
                userStatus
            ) VALUES (
                :userId, :email, :password, :fullname, :cnpjCpf,
                :areaCode, :phone, :company, :companyType,
                :activity,  :userType, CURRENT_DATE(), :addressId,
                :userStatus
            )
        '''

        params = {
            'userId': email,
            'email': email,
            'password': mysql_old_password(password),
            'fullname': fullname,
            'cnpjCpf': cnpjCpf,
            'areaCode': areaCode,
            'phone': phone,
            'company': company,
            'companyType': companyType,
            'activity': activity,
            'userType': userType,
            'addressId': addressId,
            'userStatus': userStatus
        }

        self.execute(query, params, is_transaction=True)

        # return user id (i.e. e-mail)
        return email

    def insert_statistics(self, user_id=None, scene_id=None, path=None, ip=None,
                          country=None, region=None, latitude=None, longitude=None):
        # Source: https://dev.mysql.com/doc/connector-python/en/connector-python-example-cursor-transaction.html

        logging.info('DatabaseConnection.insert_statistics()')

        query = '''
            INSERT INTO Download (
                userId, sceneId, path, ip, region,
                country, latitude, longitude,
                date
            ) VALUES (
                :user_id, :scene_id, :path, :ip, :region,
                :country, :latitude, :longitude,
                NOW()
            )
        '''

        params = {
            'user_id': user_id,
            'scene_id': scene_id,
            'path': path,
            'ip': ip,
            'region': region,
            'country': country,
            'latitude': latitude,
            'longitude': longitude
        }

        self.execute(query, params, is_transaction=True)

    def insert_address(self, userId, cep, street, number, city, state, country):
        # Source: https://dev.mysql.com/doc/connector-python/en/connector-python-example-cursor-transaction.html

        # print('\n\n DatabaseConnection.insert_address()')

        query = '''
            INSERT INTO Address (
                userId, cep, street, number, city,
                state, country, addressType, CNPJ_CPF
            ) VALUES (
                :userId, :cep, :street, :number, :city,
                :state, :country, "", ""
            )
        '''

        params = {
            'userId': userId,
            'cep': cep,
            'street': street,
            'number': number,
            'city': city,
            'state': state,
            'country': country
        }

        address_id = self.execute(query, params, is_transaction=True)

        return address_id

    def delete_user(self, user_id):
        query = '''
            DELETE FROM User
            WHERE userId=:user_id;
        '''

        params = {
            'user_id': user_id
        }

        self.execute(query, params, is_transaction=True)
