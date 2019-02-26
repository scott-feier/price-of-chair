import uuid
from src.common.database import Database
from src.common.utils import Utils
import src.models.users.errors as user_errors
import src.models.users.constants as user_constants
from src.models.alerts.alert import Alert


class User(object):
    def __init__(self, email, password, _id=None):
        self.email = email
        self.password = password
        self._id = uuid.uuid4().hex if _id is None else _id

    def json(self):
        return {
            "_id": self._id,
            "email": self.email,
            "password": self.password
        }

    def __repr__(self):
        return '<Alert for user {}>'.format(self.email)

    @staticmethod
    def is_login_valid(email, password):
        """  Verify email and password combo

        this method verifies that an email password combo is valid
        email exists, and password is correct
        :param email:   user's email (string)
        :param password:   a SHA512 hashed password
        :return: true if valid false otherwise
        """
        user_data = User.get_from_db_by_email(email)
        if user_data is None:  # raise an error if user does not exist
            raise user_errors.UserNotExistError('Your user does not exist')
        else:
            if not Utils.check_hashed_password(password, user_data['password']):
                raise user_errors.IncorrectPasswordError('Password mismatch')
            else:
                return True  # user is there AND password matches

    @staticmethod
    def register_user(email, password):
        """  Register the user

        :param email:  the email - make sure it's unique
        :param password:  hashed digest of the password
        :return:  true if successfully stored
        """
        user_data = User.get_from_db_by_email(email)
        if user_data is not None:  # raise an error if user does not exist
            raise user_errors.UserAlreadyExistsError('Your user already exists')
        if not Utils.email_is_valid(email):
            raise user_errors.InvalidEmailError('invalid email format')

        password = Utils.hash_password(password)
        User(email, password).save_to_db()

        return True

    def save_to_db(self):
        Database.insert(user_constants.COLLECTION, self.json())

    @staticmethod
    def get_from_db_by_email(email):
        user_data = Database.find_one(user_constants.COLLECTION, {'email': email})
        return user_data  # returns database record, fine if checking for presence / absence

    @staticmethod
    def get_from_db_by_id(_id):
        user_data = Database.find_one(user_constants.COLLECTION, {'_id': _id})
        return user_data  # returns database record, fine if checking for presence / absence

    @classmethod
    def db_to_rec(cls, db_rec):
        return cls(**db_rec)

    def get_alerts(self):
        return Alert.find_by_user_email(self.email)
