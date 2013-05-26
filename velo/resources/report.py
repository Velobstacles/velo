from . import meta

schema = {

    }


class Collection(meta.Collection):

    def __getitem__(self, key):
        return Resource(key, self)


class Resource(meta.Resource):
    pass
