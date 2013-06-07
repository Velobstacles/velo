import logging

from passlib.hash import bcrypt
from pymongo import errors

from .base import Document

log = logging.getLogger(__name__)


class User(Document):

    __collection__ = 'user'

    structure = {
        u'name': unicode,
        u'username': unicode,
        u'mail': unicode,
        u'password': unicode,
        }

    required = [
        'name',
        'username',
        'mail',
        'password',
        ]

    indexes = [
        {'fields': 'username', 'unique': True},
        {'fields': 'mail', 'unique': True},
        ]

    @staticmethod
    def create(db, name, username, mail, password):
        user = db.User()
        user.name = name
        user.username = username
        user.mail = mail
        user.password = unicode(bcrypt.encrypt(password))
        try:
            user.save()
        except errors.DuplicateKeyError:
            raise
        except errors.PyMongoError:
            log.exception('User.save db=%s', db)
            raise
        return user

    @staticmethod
    def verify(db, username, password):
        try:
            user = db.User.find_one({'username': username})
        except errors.PyMongoError:
            log.exception('User.verify username=%s', username)
            raise
        try:
            if user and bcrypt.verify(password, user.password):
                return user
        except:
            pass
        return False
