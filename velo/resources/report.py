import logging

from onctuous import Schema, Optional, Match, InRange
import royal

from bson.objectid import InvalidId
from royal import exceptions as exc

from . import photo
from .. import model

log = logging.getLogger(__name__)


class Collection(royal.Collection):

    default_radius = 50

    index_schema = Schema({
        Optional('location'): Match('-?\d+(\.\d+)?,-?\d+(\.\d+)?'),
        Optional('radius'): InRange(min=1),
        })

    def __getitem__(self, key):
        return Resource(key, self)

    def index(self, page, page_size, location=None, radius=None):
        if location is not None:
            coordinates = [float(s) for s in location.split(',')]
            radius = radius if radius else Collection.default_radius
            cursor = model.Report.get_by_location(self.db, page, page_size,
                                                  coordinates, radius)
            query = dict(page=page, page_size=page_size, location=location,
                         radius=radius)
        else:
            cursor = model.Report.get_newests(self.db, page, page_size)
            query = dict(page=page, page_size=page_size)
        return royal.PaginatedResult(self, cursor, Resource, query,
                                     cursor.count())


class Resource(royal.Resource):

    def __getitem__(self, key):
        self.load_model()

        if key == 'photos':
            report_photos = model.Photo.get_by_report(self.db, self.model._id)
            return photo.Collection(key, self, model=report_photos)

        raise KeyError(key)

    @property
    def links(self):
        return {
            'self': self,
            'photos': self['photos'],
            }

    def load_model(self):
        if self.model is None:
            try:
                self.model = model.Report.get_by_id(self.db, self.__name__)
            except InvalidId:
                raise exc.NotFound(self)

        if self.model is None:
            raise exc.NotFound(self)

        return self.model

    def show(self):
        report = self.load_model()
        report['created'] = report._id.generation_time
        return report
