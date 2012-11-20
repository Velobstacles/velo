# -*- coding: utf-8 -*-
from __future__ import absolute_import
from bson.objectid import ObjectId

from pyramid.response import Response, FileIter

from velo.views import Base


class MediumContentView(Base):

    def show(self, medium_id):
        medium = self.request.db.Medium.find_one({'_id': ObjectId(medium_id)})
        response = Response(
            app_iter=FileIter(medium.fs.get_last_version('content')),
            content_type=str(medium.mime_type),
            )
        return response
