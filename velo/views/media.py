# -*- coding: utf-8 -*-
from mongokit.document import ObjectId

from pyramid.httpexceptions import HTTPCreated

from pyramid_rest.resource import method_config


from velo.views import Base


class MediaView(Base):

    def index(self):
        # XXX: pagination
        media = self.request.db.Medium.find()
        return {
            'data': [{
                'id': str(medium._id),
                'location': medium.location,
                'links': {
                    'self': self.request.rest_resource_url(
                        'medium',
                        medium._id,
                        ),
                    },
                } for medium in media],
            }

    def create(self):
        medium = self.request.db.Medium()
        medium.location = {
            'longitude': float(self.request.POST.getone('longitude')),
            'latitude': float(self.request.POST.getone('latitude')),
            }
        medium.save()
        medium.fs.source = self.request.POST.getone('source').file.read()
        return HTTPCreated(
            location=self.request.rest_resource_url('medium', medium._id)
            )

    def show(self, id):
        medium = self.request.db.Medium.find_one({'_id': ObjectId(id)})
        return {
            'id': str(medium._id),
            'location': medium.location,
            'links': {}
            }

    def update(self, id):
        return {}

    def delete(self, id):
        pass

    @method_config(renderer='media_form.mako')
    def edit(self, id):
        return {}

    @method_config(renderer='media_form.mako')
    def new(self):
        return {}
