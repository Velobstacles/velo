from onctuous import Schema, Required, Coerce, Match

from bson.objectid import InvalidId
from pymongo import errors
from royal import exceptions as exc

import royal

from ..model import User
from . import user_report


class Collection(royal.Collection):

    create_schema = Schema({
        Required('name'): Coerce(unicode),
        Required('username'): Match('[a-zA-Z0-9_]'),
        Required('mail'): Coerce(unicode),
        Required('password'): Coerce(unicode),
        })

    def __getitem__(self, key):
        return Resource(key, self)

    def index(self, offset, limit):
        cursor = User.get_newests(self.db, offset, limit)
        query = dict(offset=offset, limit=limit)
        return royal.PaginatedResult(self, cursor, Resource, query,
                                     cursor.count())

    def create(self, name, username, mail, password):
        try:
            user = User.create(self.db, name, username, mail, password)
        except errors.DuplicateKeyError:
            raise exc.Conflict(self)
        else:
            return Resource(str(user._id), self, model=user)


class Resource(royal.Resource):

    children = {
        'reports': user_report.Collection,
        }

    def __getitem__(self, key):
        self.load_model()
        return self.children[key](key, self)

    def load_model(self):
        if self.model is None:
            try:
                self.model = User.get_by_id(self.db, self.__name__)
            except InvalidId:
                raise exc.NotFound(self)

        if self.model is None:
            raise exc.NotFound(self)

        return self.model

    def show(self):
        user = self.load_model()
        user['created'] = user._id.generation_time
        del user['password']
        return user
