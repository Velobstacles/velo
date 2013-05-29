import logging

import onctuous
import royal

from bson.objectid import InvalidId
from royal import exceptions as exc

from . import photo
from .. import model

log = logging.getLogger(__name__)


class Collection(royal.Collection):

    index_schema = {
        onctuous.Required('location'): onctuous.Match(r'\d(\.\d)?,\d(\.\d)?'),
        onctuous.Required('radius', 50): onctuous.InRange(min=1),
        }

    def __getitem__(self, key):
        return Resource(key, self)

    def index(self, page, page_size, location, radius):
        skip = page_size * page
        location = [float(s) for s in location.split(',')]
        geoquery = {
            'location': {
                '$near': {
                    '$geometry': {
                        "type": "Point",
                        "coordinates": location,
                        },
                    '$maxDistance': radius
                    }
                }
            }
        cursor = self.db.Report.find(geoquery, limit=page_size, skip=skip)
        return royal.PaginatedResult(self, cursor, Resource, cursor.count())


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
        return self.load_model()
