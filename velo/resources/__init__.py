import royal

from . import photo, report


def includeme(config):
    config.set_root_factory(Root)


class Root(royal.Root):
    children = {
        'photos': photo.Collection,
        'reports': report.Collection,
        }

    def __getitem__(self, key):
        return self.children[key](key, self)
