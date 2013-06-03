import cgi
import logging
import mimetypes

from onctuous import Schema, Optional, Match, InRange, Required, Coerce

import royal

from bson.objectid import InvalidId, ObjectId
from pymongo import errors
from pyramid.decorator import reify
from royal import exceptions as exc

from . import photo_file
from .validators import validate_isinstance
from ..import model

log = logging.getLogger(__name__)


class Collection(royal.Collection):

    default_radius = 50

    index_schema = Schema({
        Optional('location'): Match('-?\d+(\.\d+)?,-?\d+(\.\d+)?'),
        Optional('radius'): InRange(min=1),
        })

    create_schema = Schema({
        Required('report_id'): Coerce(ObjectId),
        Required('author'): Coerce(unicode),
        Required('longitude'): Coerce(float),
        Required('latitude'): Coerce(float),
        Required('content'): validate_isinstance(cgi.FieldStorage),
        })

    def __getitem__(self, key):
        return Resource(key, self)

    def index(self, page, page_size, location=None, radius=None):
        query = {}
        if location is not None:
            coordinates = [float(s) for s in location.split(',')]
            radius = radius if radius else Collection.default_radius
            cursor = model.Photo.get_by_location(self.db, page, page_size,
                                                 coordinates, radius)
            query['location'] = location
            query['radius'] = radius
        else:
            cursor = model.Photo.get_newests(self.db, page, page_size)
        query.update(page=page, page_size=page_size)
        if self.model is None:
            self.model = cursor
        return royal.PaginatedResult(self, self.model, Resource, query,
                                     self.model.count())

    def create(self, report_id, author, longitude, latitude, content):
        mime_type = mimetypes.guess_type(content.filename)
        photo = model.Photo.create(
            self.db,
            report_id,
            author,
            longitude,
            latitude,
            content.file,
            mime_type[0],
            )
        return Resource(str(photo._id), self, model=photo)


class Resource(royal.Resource):

    children = {
        'content': photo_file.Collection,
        }

    def __getitem__(self, key):
        return self.children[key](key, self)

    @reify
    def links(self):
        self_link = self.root['photos'][self.__name__]
        return {
            'self': self_link,
            'content': self_link['content'],
            'report': self.root['reports'][self.model.report_id]
            }

    def load_model(self):
        if self.model is None:
            try:
                self.model = model.Photo.get_by_id(self.db, self.__name__)
            except InvalidId:
                raise exc.NotFound(self)

        if self.model is None:
            raise exc.NotFound(self)

        return self.model

    def show(self):
        return self.load_model()

    def delete(self):
        self.load_model()
        try:
            self.model.delete()
        except errors.PyMongoError:
            log.exception('delete on %s', self.model)
