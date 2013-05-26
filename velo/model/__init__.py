from pyramid_mongokit import register_document

from . import mongokit_patch  # monkey patch to enable 2dsphere index
mongokit_patch.patch()

from .photo import Photo


__all__ = [
    'Medium',
    ]


def includeme(config):
    register_document(config.registry, Photo)
