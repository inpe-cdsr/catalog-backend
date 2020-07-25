# disable pylint(line-too-long) (All codes: http://pylint-messages.wikidot.com/all-codes)
# pylint: disable=C0301

"""Controllers"""

'''
from flask_restplus import Resource as APIResource
from werkzeug.exceptions import Unauthorized

from catalog_backend.nonce import ns
from catalog_backend.nonce.business import NonceBusiness
from catalog_backend.log import logging
from catalog_backend.common import create_nonce


api = ns


@api.route('/<email:email>')
class Nonce(APIResource):
    """
    Nonce
    Full route: /api/nonce/<email>
    """

    nonce_business = NonceBusiness()

    def get(self, email):
        """
        Returns
        -------
        image/tif
        """

        logging.info('Nonce.get()\n')

        logging.info('Nonce.get() - email: %s', email)

        if not email:
            raise Unauthorized('E-mail is required!')

        # create a new nonce

        nonce = NonceBusiness.create_nonce()

        # insert the new nonce in the database related to the email

        # return the nonce

        return nonce
'''
