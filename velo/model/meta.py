# -*- coding: utf-8 -*-
from __future__ import absolute_import
import os

import mongokit

from zope.interface import implementer
from zope.interface import Interface

DATABASE_NAME = os.environ['VELO_DB_NAME']


class Document(mongokit.Document):
    """Base class for all db documents."""
    __database__ = DATABASE_NAME


class IMongoConnection(Interface):
    pass


@implementer(IMongoConnection)
class MongoConnection(mongokit.Connection):
    pass
