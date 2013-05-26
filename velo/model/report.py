from .base import Document


class Report(Document):

    __collection__ = 'report'

    structure = {
        'author': unicode,
        'description': unicode,
        'location': {
            'type': unicode,
            'coordinates': list,
            },
        'tags': list,
        }
