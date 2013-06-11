import logging

from pymongo import errors, GEOSPHERE

from .base import Document

log = logging.getLogger(__name__)


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

    required_fields = [
        'author',
        'description',
        'location.type',
        'location.coordinates',
        'tags',
        ]

    indexes = [
        {'fields': ('location', GEOSPHERE)},
        {'fields': 'tags'},
        ]

    @staticmethod
    def create(db, author, description, longitude, latitude, tags):
        report = db.Report()
        report.author = author
        report.description = description
        report.location.type = u"Point"
        report.location.coordinates = [longitude, latitude]
        report.tags = tags
        try:
            report.save()
        except errors.PyMongoError:
            log.exception('report.save() db=%s report=%s', db, report)
            raise
        return report

    @staticmethod
    def get_by_author(db, username, offset, limit):
        return db.Report.find({'author': username}).skip(offset).limit(limit)
