from . import meta, photo, report


def includeme(config):
    config.add_route('api', '/*traverse', factory=Root)


class Root(meta.Root):
    children = {
        'photos': photo.Collection,
        'reports': report.Collection,
        }

    def __getitem__(self, key):
        return self.children[key](key, self)
