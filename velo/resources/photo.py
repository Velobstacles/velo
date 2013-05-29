import logging

import royal

from bson.objectid import InvalidId
from pymongo import errors
from pyramid.decorator import reify
from royal import exceptions as exc

from . import photo_file
from ..model.photo import Photo

log = logging.getLogger(__name__)


class Collection(royal.Collection):

    index_schema = {}

    def __getitem__(self, key):
        return Resource(key, self)

    def index(self, page, page_size):
        skip = page_size * page
        if self.model is None:
            self.model = self.db.Photo.find(limit=page_size, skip=skip)
        return royal.PaginatedResult(self, self.model, Resource,
                                     self.model.count())


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
                self.model = Photo.get_by_id(self.db, self.__name__)
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
