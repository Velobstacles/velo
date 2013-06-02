from pyramid_mongokit import register_document, generate_index

from . import mongokit_patch  # monkey patch to enable 2dsphere index
mongokit_patch.patch()

from .photo import Photo
from .report import Report


__all__ = [
    'Photo',
    'Report',
    ]


def includeme(config):
    config.include('pyramid_mongokit')

    register_document(config.registry, Photo)
    generate_index(config.registry, Photo)

    register_document(config.registry, Report)
    generate_index(config.registry, Report)
