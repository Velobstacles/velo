# -*- coding: utf-8 -*-
from velo.model.medium import Medium

from pyramid_rest.mongo import register_document

__all__ = [
    'Medium',
    ]


def includeme(config):
    register_document(config.registry, Medium)
