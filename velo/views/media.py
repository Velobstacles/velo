# -*- coding: utf-8 -*-
from velo.views import Base


class MediaView(Base):

    def index(self):
        # XXX: pagination
        media = self.request.db.medium.find()

        return {
            'data': [medium for medium in media],
            }

    def create(self):
        pass

    def show(self, id):
        return {}

    def update(self, id):
        return {}

    def delete(self, id):
        pass

    def edit(self, id):
        pass

    def new(self):
        pass
