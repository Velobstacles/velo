import royal
from onctuous import Schema, Required, Coerce

from .. import model
from . import report


class Collection(royal.Collection):

    create_schema = Schema({
        Required('description'): Coerce(unicode),
        Required('longitude'): Coerce(float),
        Required('latitude'): Coerce(float),
        Required('tags'): list,
        })

    @property
    def user(self):
        return self.__parent__

    def index(self, offset, limit):
        query = dict(offset=offset, limit=limit)
        cursor = model.Report.get_by_author(self.db, self.user.model.username,
                                            offset, limit)
        return royal.PaginatedResult(self.root['reports'], cursor,
                                     report.Resource, query, cursor.count())

    def create(self, description, longitude, latitude, tags):
        author = self.user.model.username
        r = model.Report.create(self.db, author, description, longitude,
                                latitude, tags)
        return report.Resource(str(r._id), self.root['reports'], model=r)
