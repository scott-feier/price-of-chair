from passlib.hash import pbkdf2_sha512
import hashlib
import re


class Utils(object):

    @staticmethod
    def check_hashed_password(entered_password, db_password):
        """ Checks if hash of password user entered matches the stored password hash

        :param entered_password: user entered password
        :param db_password: hash of password retrieved from database
        :return: true if match, false if not
        """
        return pbkdf2_sha512.verify(entered_password, db_password)

    @staticmethod
    def hash_password(password):
        """ Hash the password, create salt and encrypt

        :param password:  plaintext password
        :return: hashed password using sha512
        """

        return pbkdf2_sha512.hash(password)

    @staticmethod
    def hash_digest(password):
        """ Hash the password to sha512 digest

        :param password:  plaintext password
        :return: hashed password using sha512
        """
        m = hashlib.sha512()
        m.update(password.encode())
        return m.hexdigest().upper()

    @staticmethod
    def email_is_valid(email):
        email_address_matcher = re.compile('^[\w\-.]+@([\w\-]+\.)+[\w]+$')
        return True if email_address_matcher.match(email) else False
