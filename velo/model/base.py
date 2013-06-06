from bson.objectid import ObjectId
from mongokit import document
from pymongo import DESCENDING


class Document(document.Document):

    use_dot_notation = True

    @classmethod
    def get_newests(cls, db, page, page_size):
        skip = page * page_size
        return (db[cls.__name__].find()
                                .sort('_id', DESCENDING)
                                .limit(page_size)
                                .skip(skip)
                )

    @classmethod
    def get_by_location(cls, db, page, page_size, coordinates, radius,
                        field='location'):
        skip = page_size * page
        return (
            db[cls.__name__]
            .find(get_geoquery('location', coordinates, radius))
            .limit(page_size)
            .skip(skip)
            )

    @classmethod
    def get_by_id(cls, db, _id):
        if isinstance(_id, (str, unicode)):
            _id = ObjectId(_id)
        return db[cls.__name__].one({'_id': _id})


def get_geoquery(field, coordinates, radius):
    return {
        field: {
            '$near': {
                '$geometry': {
                    "type": "Point",
                    "coordinates": coordinates,
                    },
                '$maxDistance': radius
                }
            }
        }
