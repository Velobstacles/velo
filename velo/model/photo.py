import logging
import shutil

from bson.objectid import ObjectId
from pymongo import errors, GEOSPHERE

from .base import Document

log = logging.getLogger(__name__)

#http://docs.mongodb.org/manual/applications/2dsphere/#store-geojson-objects


class Photo(Document):

    __collection__ = 'photo'

    structure = {
        'report_id': ObjectId,
        'author': unicode,
        'location': {
            'type': unicode,
            'coordinates': list,
            },
        }

    gridfs = {
        'files': ['content']
        }

    required_fields = [
        'report_id',
        'author',
        'location.type',
        'location.coordinates',
        ]

    indexes = [
        {'fields': ('location', GEOSPHERE)},
        {'fields': 'report_id'},
        ]

    def get_content_grid_out(self):
        try:
            return self.fs.get_last_version('content')
        except errors.PyMongoError:
            log.exception('%s.get_image_grid_out', self)
            raise

    @staticmethod
    def create(db, report_id, author, longitude, latitude, fs, mime_type):
        photo = db.Photo()
        photo.report_id = report_id
        photo.author = author
        photo.location.type = u"Point"
        photo.location.coordinates = [longitude, latitude]
        try:
            photo.save()
        except errors.PyMongoError:
            log.exception('photo.save() on db=%s', db)
            raise
        with photo.fs.new_file('content') as fp:
            try:
                fp.content_type = mime_type
                shutil.copyfileobj(fs, fp)
            except:
                log.exception('content file copy on db=%s', db)
                raise
        return photo

    @staticmethod
    def get_by_report(db, report_id):
        return db.find({'report_id': report_id}).all()

    @staticmethod
    def get_by_id(db, photo_id):
        if isinstance(photo_id, (str, unicode)):
            photo_id = ObjectId(photo_id)
        return db.Photo.one({'_id': photo_id})
