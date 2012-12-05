# -*- coding: utf-8 -*-
from bson.objectid import InvalidId, ObjectId

from pyramid.httpexceptions import HTTPCreated, HTTPNotFound, HTTPOk

from pyramid_rest.resource import method_config

from velo.views import Base


class MediaView(Base):

    def _get_one_or_404(self, id):
        try:
            medium = self.request.mongo_db.Medium.find_one({'_id': ObjectId(id)})
        except InvalidId:
            raise HTTPNotFound()
        if not medium:
            raise HTTPNotFound()
        return medium

    def _save_medium(self, medium):
        content = self.request.POST.getone('content')
        medium.location = {
            'longitude': float(self.request.POST.getone('longitude')),
            'latitude': float(self.request.POST.getone('latitude')),
            }
        medium.mime_type = content.type
        medium.save()
        medium.fs.put(
            content.file,
            filename='content',
            )

    def _format_medium(self, medium):
        return {
            'id': str(medium._id),
            'location': medium.location,
            'creation_datetime': medium.creation_datetime.isoformat(),
            'mime_type': medium.mime_type,
            'links': {
                'self': self.request.rest_resource_url('medium', medium._id,),
                'content': self.request.rest_resource_url(
                    'medium.content',
                    medium._id,
                    )
                },
            }

    def index(self):
        # XXX: pagination
        media = self.request.mongo_db.Medium.find()
        return {'data': [self._format_medium(medium) for medium in media]}

    def create(self):
        medium = self.request.mongo_db.Medium()
        self._save_medium(medium)
        return HTTPCreated(
            location=self.request.rest_resource_url('medium', medium._id)
            )

    def show(self, id):
        medium = self._get_one_or_404(id)
        return self._format_medium(medium)

    def update(self, id):
        medium = self._get_one_or_404(id)
        self._save_medium(medium)
        return HTTPOk()

    def delete(self, id):
        medium = self._get_one_or_404(id)
        medium.delete()
        return HTTPOk()

    @method_config(renderer='media_form.mako')
    def edit(self, id):
        return {'medium': self._get_one_or_404(id)}

    @method_config(renderer='media_form.mako')
    def new(self):
        return {'medium': self.request.mongo_db.Medium()}
