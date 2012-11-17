# -*- coding: utf-8 -*-
from datetime import datetime

from bson.binary import Binary

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
        'content': Binary,
        }

    required_fields = [
        'creation_datetime',
        'location.longitude',
        'location.latitude',
        ]

    default_values = {
        'creation_datetime': datetime.utcnow
    }
