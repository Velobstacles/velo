import cgi
import mimetypes

import royal

from onctuous import Schema, Required, Coerce

from .. import model
from . import photo
from .validators import validate_isinstance


class Collection(royal.Collection):

    create_schema = Schema({
        Required('author'): Coerce(unicode),
        Required('longitude'): Coerce(float),
        Required('latitude'): Coerce(float),
        Required('content'): validate_isinstance(cgi.FieldStorage),
        })

    @property
    def report(self):
        return self.__parent__

    def index(self, page, page_size):
        cursor = model.Photo.get_by_report(self.db, self.report.model._id)
        query = dict(page=page, page_size=page_size)
        return royal.PaginatedResult(self, cursor, photo.Resource, query,
                                     cursor.count())

    def create(self, author, longitude, latitude, content):
        mime_type = mimetypes.guess_type(content.filename)
        p = model.Photo.create(
            self.db,
            self.report.model._id,
            author,
            longitude,
            latitude,
            content.file,
            mime_type[0],
            )
        return photo.Resource(str(p._id), self.root['photos'], model=p)
