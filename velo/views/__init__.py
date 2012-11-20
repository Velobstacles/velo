# -*- coding: utf-8 -*-
from __future__ import absolute_import
from pyramid.view import view_config


class Base(object):
    """Base class for all views."""

    def __init__(self, context, request):
        self.context = context
        self.request = request


@view_config(renderer='index.mako')
def index(context, request):
    return {}
