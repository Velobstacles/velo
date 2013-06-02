from mongokit import document


class Document(document.Document):

    use_dot_notation = True


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
