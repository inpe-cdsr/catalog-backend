"""
DGI Catalog
"""

from mysql.connector import connect, errorcode, Error
from datetime import date, datetime

from werkzeug.exceptions import BadRequest, InternalServerError, NotFound

from dgi_catalog.environment import MYSQL_DB_USER, MYSQL_DB_PASSWORD, \
                                    MYSQL_DB_HOST, MYSQL_DB_DATABASE


def fix_rows(rows):
    for row in rows:
        for key in row:
            # datetime/date is not serializable by default, then get a serializable string representation
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
        self.connection = None

    def close(self):
        self.connection.close()

    def connect(self):
        try:
            self.connection = connect(user=MYSQL_DB_USER, password=MYSQL_DB_PASSWORD,
                                      host=MYSQL_DB_HOST, database=MYSQL_DB_DATABASE)

        except Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print('Access was denied to your credentials.')
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print('Database does not exist.')
            else:
                print('An error occurred during database connection: %s', err)

            self.close()

    def commit(self):
        self.connection.commit()

    def rollback(self):
        self.connection.rollback()

    def execute(self, query, params=None, is_transaction=False):
        self.connect()
        cursor = self.connection.cursor(dictionary=True)
        # print('Database connection was created.')

        result = None

        try:
            cursor.execute(query, params=params)

            # if query is a transaction statement, then commit the changes
            if is_transaction:
                self.commit()

            # print('The query was executed successfully.')

            # if there are rows, then return them (SELECT operation)
            if cursor.with_rows:
                return cursor.fetchall()
            # INSERT, UPDATE and DELETE operations need to be committed
            else:
                # if 'query' was a 'INSERT' statement, then it returns the inserted record 'id',
                # else it returns '0'
                return str(cursor.lastrowid)

        except Error as err:
            self.rollback()
            print('An error occurred during query execution: %s', err)
            raise BadRequest(str(err))

        # finally is always executed (both at try and except)
        finally:
            cursor.close()
            self.close()
            # print('Database connection was closed.')

    def select_user(self, email=None, password=None):
        # Sources:
        # https://dev.mysql.com/doc/connector-python/en/connector-python-example-cursor-select.html
        # https://dev.mysql.com/doc/connector-python/en/connector-python-api-mysqlcursor-execute.html

        query = '''
            SELECT * FROM User
            WHERE email=%(email)s AND password=%(password)s
        '''

        params = { 'email': email, 'password': password }

        # execute the query and fix the resulted rows
        rows = self.execute(query, params)
        rows = fix_rows(rows)

        return rows

    def insert_user(self, email=None, password=None, fullname='', cnpjCpf='',
                    areaCode='', phone='', company='', companyType='',
                    activity='', userType='', addressId=None,
                    userStatus='', marlin=0):
        # Source: https://dev.mysql.com/doc/connector-python/en/connector-python-example-cursor-transaction.html

        # print('\n\n DatabaseConnection.insert_user()')

        query = '''
            INSERT INTO User (
                userId, email, password, fullname, CNPJ_CPF,
                areaCode, phone, company, companyType,
                activity, userType, registerDate, addressId,
                userStatus, marlin
            ) VALUES (
                %(userId)s, %(email)s, %(password)s, %(fullname)s, %(cnpjCpf)s,
                %(areaCode)s, %(phone)s, %(company)s, %(companyType)s,
                %(activity)s,  %(userType)s, CURRENT_DATE(), %(addressId)s,
                %(userStatus)s, %(marlin)s
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
            'userStatus': userStatus,
            'marlin': marlin
        }

        self.execute(query, params, is_transaction=True)

        # return user id (i.e. e-mail)
        return email

        # return user id
        # return self.execute(query, params)

    def insert_statistics(self, userId, sceneId, path, ip,
                    country=None, region=None, lat=None, lng=None):
        # Source: https://dev.mysql.com/doc/connector-python/en/connector-python-example-cursor-transaction.html

        # print('\n\n DatabaseConnection.insert_statistics()')

        query = '''
            INSERT INTO Download (
                userId, sceneId, path, ip, region,
                country, latitude, longitude, date
            ) VALUES (
                %(userId)s, %(sceneId)s, %(path)s, %(ip)s, %(region)s,
                %(country)s, %(latitude)s, %(longitude)s, CURRENT_DATE()
            )
        '''

        params = {
            'userId': userId,
            'sceneId': sceneId,
            'path': path,
            'ip': ip,
            'region': region,
            'country': country,
            'latitude': lat,
            'longitude': lng
        }

        self.execute(query, params, is_transaction=True)

        return True
