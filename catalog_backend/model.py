#!/usr/bin/env python3

"""DGI Catalog"""

from datetime import date, datetime
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import text
from werkzeug.exceptions import InternalServerError

from catalog_backend.environment import MYSQL_DB_USER, MYSQL_DB_PASSWORD, \
                                    MYSQL_DB_HOST, MYSQL_DB_PORT, \
                                    MYSQL_DB_DATABASE
from catalog_backend.exception import DatabaseConnectionException
from catalog_backend.log import logging


def fix_rows(rows):
    for row in rows:
        for key in row:
            # datetime/date is not serializable by default, then it gets a
            # serializable string representation
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

            logging.info(f'DatabaseConnection.execute() - query_text: {query_text}')
            logging.info(f'DatabaseConnection.execute() - params: {params}')

            self.try_to_connect()

            # cursor.execute(query, params=params)
            result = self.engine.execute(query_text, params)

            # logging.info('DatabaseConnection.execute() - returns_rows: %s', result.returns_rows)
            logging.info('DatabaseConnection.execute() - rowcount: %s', result.rowcount)
            logging.info('DatabaseConnection.execute() - lastrowid: %s', result.lastrowid)
            # logging.debug('DatabaseConnection.execute() - result: %s', result)

            # `returns_rows` means the query is a SELECT clause
            if result.returns_rows:
                # SELECT clause
                rows = result.fetchall()
                rows = [dict(row) for row in rows]

                # logging.debug('DatabaseConnection.execute() - rows: \n%s\n', rows)

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

    ##################################################
    # USER
    ##################################################

    def select_user(self, email=None, password=None):
        # Sources:
        # https://dev.mysql.com/doc/connector-python/en/connector-python-example-cursor-select.html
        # https://dev.mysql.com/doc/connector-python/en/connector-python-api-mysqlcursor-execute.html

        logging.info('DatabaseConnection.select_user()')

        where = []
        params = {}

        logging.info(f'DatabaseConnection.select_user() - email: {email}')

        if email is not None:
            where.append('email=:email')
            params['email'] = email

        if password is not None:
            where.append('password=:password')
            params['password'] = mysql_old_password(password)

        where = ' AND '.join(where)

        if where != '':
            where = 'WHERE {}'.format(where)

        query = 'SELECT * FROM User {};'.format(where)

        logging.info(f'DatabaseConnection.select_user() - query: {query}')

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

    def update_user(self, user_id, password):
        logging.info('DatabaseConnection.update_user()')

        query = 'UPDATE User SET password=:password WHERE userId=:user_id'

        params = {
            'user_id': user_id,
            'password': mysql_old_password(password)
        }

        self.execute(query, params, is_transaction=True)

    def delete_user(self, user_id):
        query = 'DELETE FROM User WHERE userId=:user_id;'

        params = {'user_id': user_id}

        self.execute(query, params, is_transaction=True)

    ##################################################
    # ITEM
    ##################################################

    def select_item(self, item_id=None, collection=None):
        logging.info('DatabaseConnection.select_item()')
        logging.info(f'DatabaseConnection.select_item() - item_id: {item_id}')
        logging.info(f'DatabaseConnection.select_item() - collection: {collection}')

        where = []
        params = {}

        if item_id is not None:
            where.append('id=:item_id')
            params['item_id'] = item_id

        if collection is not None:
            where.append('collection=:collection')
            params['collection'] = collection

        where = ' AND '.join(where)
        if where != '':
            where = f'WHERE {where}'

        query = f'SELECT * FROM stac_item {where};'

        logging.info(f'DatabaseConnection.select_item() - query: {query}')

        # execute the query and fix the resulted rows
        return fix_rows(self.execute(query, params))

    ##################################################
    # LOCATION
    ##################################################

    def select_location(self, ip=None):
        where = ''

        if ip is not None and ip != '':
            where = 'WHERE ip=:ip'

        query = 'SELECT * FROM Location {};'.format(where)

        params = {'ip': ip}

        # execute the query and fix the resulted rows
        return fix_rows(self.execute(query, params))

    def insert_location(self, ip=None, longitude=None, latitude=None, city=None, district=None,
                        region=None, region_code=None, country=None, country_code=None,
                        continent=None, continent_code=None, zip_code=None, time_zone=None):

        logging.info('DatabaseConnection.insert_location()')

        # just insert the new location if the IP has not been already added in the database
        query = '''
            INSERT INTO Location (
                ip, longitude, latitude, city, district,
                region, region_code, country, country_code,
                continent, continent_code, zip_code, time_zone
            )
            SELECT
                :ip, :longitude, :latitude, :city, :district,
                :region, :region_code, :country, :country_code,
                :continent, :continent_code, :zip_code, :time_zone
            WHERE
                (SELECT count(ip)
                FROM Location
                WHERE ip = :ip) = 0;
        '''

        params = {
            'ip': ip,
            'longitude': longitude,
            'latitude': latitude,
            'city': city,
            'district': district,
            'region': region,
            'region_code': region_code,
            'country': country,
            'country_code': country_code,
            'continent': continent,
            'continent_code': continent_code,
            'zip_code': zip_code,
            'time_zone': time_zone
        }

        self.execute(query, params, is_transaction=True)

    ##################################################
    # SECURITY
    ##################################################

    def select_security(self, user_id, token):
        logging.info('DatabaseConnection.select_security()')

        params = {'user_id': user_id, 'token': token}

        logging.info('DatabaseConnection.select_security() - params: %s', params)

        query = 'SELECT * FROM security WHERE user_id=:user_id AND token=:token;'

        # execute the query and fix the resulted rows
        return fix_rows(self.execute(query, params))

    def insert_security(self, user_id, token):
        logging.info('DatabaseConnection.insert_security()')

        params = {'user_id': user_id, 'token': token}

        logging.info('DatabaseConnection.insert_security() - params: %s', params)

        query = 'INSERT INTO security (user_id, token) VALUES (:user_id, :token);'

        self.execute(query, params, is_transaction=True)

    def delete_security(self, user_id, token):
        query = 'DELETE FROM security WHERE user_id=:user_id AND token=:token;'

        params = {'user_id': user_id, 'token': token}

        self.execute(query, params, is_transaction=True)

    ##################################################
    # OTHER
    ##################################################

    def insert_statistics(self, user_id=None, scene_id=None, dataset=None, path=None, ip=None):
        logging.info('DatabaseConnection.insert_statistics()')

        query = '''
            INSERT INTO Download (
                userId, sceneId, dataset, path, ip, date
            ) VALUES (
                :user_id, :scene_id, :dataset, :path, :ip, NOW()
            )
        '''

        params = {
            'user_id': user_id,
            'scene_id': scene_id,
            'dataset': dataset,
            'path': path,
            'ip': ip
        }

        self.execute(query, params, is_transaction=True)

    def insert_address(self, userId, cep, street, number, city, state, country, complement, **kwards):
        # Source: https://dev.mysql.com/doc/connector-python/en/connector-python-example-cursor-transaction.html

        # print('\n\n DatabaseConnection.insert_address()')

        query = '''
            INSERT INTO Address (
                userId, cep, street, number, city, state,
                country, addressType, CNPJ_CPF, complement
            ) VALUES (
                :userId, :cep, :street, :number, :city, :state,
                :country, "", "", :complement
            )
        '''

        params = {
            'userId': userId,
            'cep': cep,
            'street': street,
            'number': number,
            'city': city,
            'state': state,
            'country': country,
            'complement': complement
        }

        address_id = self.execute(query, params, is_transaction=True)

        return address_id
