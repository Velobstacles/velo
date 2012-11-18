# -*- coding: utf-8 -*-
from datetime import datetime

from mongokit import INDEX_GEO2D

from velo.model.meta import Document


class Medium(Document):
    __collection__ = 'medium'

    use_dot_notation = True

    structure = {
        'creation_datetime': datetime,
        'location': {
            'longitude': float,
            'latitude': float,
            },
        }

    gridfs = {
        'files': ['source']
        }

    required_fields = [
        'creation_datetime',
        'location.longitude',
        'location.latitude',
        ]

    default_values = {
        'creation_datetime': datetime.utcnow,
        }

    indexes = [
        {'fields': ('location', INDEX_GEO2D), }
        ]
