from onctuous import Schema, Required

import royal

from ..model import User


class Collection(royal.Collection):

    create_schema = None

    def index(self, page, page_size):
        cursor = User.get_newests(self.db, page, page_size)
        query = dict(page=page, page_size=page_size)
        return royal.PaginatedResult(self, cursor, Resource, query,
                                     cursor.count())

    def create(self):
        pass


class Resource(royal.Resource):
    pass
