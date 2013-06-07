from bson.objectid import ObjectId
from mongokit import document
from pymongo import DESCENDING


class Document(document.Document):

    use_dot_notation = True

    @classmethod
    def get_newests(cls, db, offset, limit):
        skip = offset * limit
        return (db[cls.__name__].find()
                                .sort('_id', DESCENDING)
                                .limit(limit)
                                .skip(skip)
                )

    @classmethod
    def get_by_location(cls, db, offset, limit, coordinates, radius,
                        field='location'):
        skip = limit * offset
        return (
            db[cls.__name__]
            .find(get_geoquery('location', coordinates, radius))
            .limit(limit)
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
