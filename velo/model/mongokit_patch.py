"""Monkey patch mongokit to support:
     #. 2dsphere indexes
"""
from __future__ import absolute_import
from mongokit import mongo_exceptions as exc
from mongokit.document import DocumentProperties
from mongokit.schema_document import STRUCTURE_KEYWORDS, SchemaProperties

import pymongo


def patch():
    DocumentProperties._validate_descriptors = classmethod(_validate_descriptors)


def _validate_descriptors(cls, attrs):  # pragma: no cover
    SchemaProperties._validate_descriptors(attrs)
    # validate index descriptor
    if attrs.get('migration_handler') and attrs.get('use_schemaless'):
        raise exc.OptionConflictError('You cannot set a migration_handler with use_schemaless set to True')
    if attrs.get('indexes'):
        for index in attrs['indexes']:
            if index.get('check', True):
                if 'fields' not in index:
                    raise exc.BadIndexError(
                        "'fields' key must be specify in indexes")
                for key, value in index.iteritems():
                    if key == "fields":
                        if isinstance(value, basestring):
                            if value not in attrs['_namespaces'] and value not in STRUCTURE_KEYWORDS:
                                raise ValueError(
                                    "Error in indexes: can't find %s in structure" % value )
                        elif isinstance(value, tuple):
                            if len(value) != 2:
                                raise exc.BadIndexError(
                                  "Error in indexes: a tuple must contain "
                                  "only two value : the field name and the direction")
                            if not (isinstance(value[1], int) or isinstance(value[1], basestring)):
                                raise exc.BadIndexError(
                                  "Error in %s, the direction must be int or basestring (got %s instead)" % (value[0], type(value[1])))
                            if not isinstance(value[0], basestring):
                                raise exc.BadIndexError(
                                  "Error in %s, the field name must be string (got %s instead)" % (value[0], type(value[0])))
                            if value[0] not in attrs['_namespaces'] and value[0] not in STRUCTURE_KEYWORDS:
                                raise ValueError(
                                  "Error in indexes: can't find %s in structure" % value[0] )
                            if not value[1] in [pymongo.DESCENDING, pymongo.ASCENDING, pymongo.OFF, pymongo.ALL, pymongo.GEO2D, pymongo.GEOSPHERE]:
                                raise exc.BadIndexError(
                                  "index direction must be INDEX_DESCENDING, INDEX_ASCENDING, INDEX_OFF, INDEX_ALL or INDEX_GEO2D. Got %s" % value[1])
                        elif isinstance(value, list):
                            for val in value:
                                if isinstance(val, tuple):
                                    field, direction = val
                                    if field not in attrs['_namespaces'] and field not in STRUCTURE_KEYWORDS:
                                        raise ValueError(
                                          "Error in indexes: can't find %s in structure" % field )
                                    if not direction in [pymongo.DESCENDING, pymongo.ASCENDING, pymongo.OFF, pymongo.ALL, pymongo.GEO2D, pymongo.GEOSPHERE]:
                                        raise exc.BadIndexError(
                                          "index direction must be INDEX_DESCENDING, INDEX_ASCENDING, INDEX_OFF, INDEX_ALL or INDEX_GEO2D. Got %s" % direction)
                                else:
                                    if val not in attrs['_namespaces'] and val not in STRUCTURE_KEYWORDS:
                                        raise ValueError(
                                          "Error in indexes: can't find %s in structure" % val )
                        else:
                            raise exc.BadIndexError(
                              "fields must be a string, a tuple or a list of tuple (got %s instead)" % type(value))
                    elif key == "ttl":
                        assert isinstance(value, int)
