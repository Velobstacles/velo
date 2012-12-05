# -*- coding: utf-8 -*-
from datetime import datetime

from mongokit import Document, INDEX_GEO2D


class Medium(Document):
    __collection__ = 'medium'

    use_dot_notation = True

    structure = {
        'creation_datetime': datetime,
        'location': {
            'longitude': float,
            'latitude': float,
            },
        'mime_type': basestring,
        }

    gridfs = {
        'files': ['content']
        }

    required_fields = [
        'creation_datetime',
        'location.longitude',
        'location.latitude',
        'mime_type'
        ]

    default_values = {
        'creation_datetime': datetime.utcnow,
        }

    # http://www.mongodb.org/display/DOCS/Geospatial+Indexing
    indexes = [{'fields': ('location', INDEX_GEO2D)}]
