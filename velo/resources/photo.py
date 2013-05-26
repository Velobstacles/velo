import cgi
import logging

import onctuous
from bson.objectid import InvalidId
from pymongo import errors

import velo.exceptions as exc
from . import meta
from . import photo_file
from ..model.photo import Photo

log = logging.getLogger(__name__)

schema = onctuous.Schema({
    onctuous.Required('longitude'): onctuous.Coerce(float),
    onctuous.Required('latitude'): onctuous.Coerce(float),
    onctuous.Required('content'): meta.validate_isinstance(cgi.FieldStorage),
    })


class Collection(meta.Collection):

    index_schema = onctuous.Schema({})

    def __getitem__(self, key):
        return Resource(key, self)

    def index(self, limit=20, page=0):
        skip = page * limit
        cursor = self.db.Photo.find(limit=limit, skip=skip)
        return meta.PaginatedResult(self, cursor, Resource, cursor.count())


class Resource(meta.Resource):

    children = {
        'content': photo_file.Collection,
        }

    def __getitem__(self, key):
        return self.children[key](key, self)

    @property
    def links(self):
        return {
            'self': self,
            'content': self['content'],
            'report': self.root['reports'][self.model.report_id]
            }

    def load_model(self):
        if not self.model:
            try:
                self.model = Photo.get_by_id(self.db, self.__name__)
            except InvalidId:
                raise exc.NotFound(self)
        if not self.model:
            raise exc.NotFound(self)
        return self.model

    def show(self):
        self.load_model()
        return self.model

    def delete(self):
        self.load_model()
        try:
            self.model.delete()
        except errors.PyMongoError:
            log.exception('delete on %s', self.model)
