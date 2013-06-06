import logging

import bcrypt

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
        user.password = bcrypt.hashpw(password, bcrypt.gensalt())
        try:
            user.save()
        except errors.PyMongoError:
            log.exception('user.save db=%s', db)
            raise
        return user
