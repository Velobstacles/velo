# -*- coding: utf-8 -*-
import logging
import os

from pyramid.events import NewRequest

from velo.model.meta import (
    DATABASE_NAME,
    IMongoConnection,
    MongoConnection,
    )
from velo.model.medium import Medium


log = logging.getLogger(__name__)


def includeme(config):
    log.info('Configure model...')
    connection = MongoConnection(
        os.environ['MONGO_URI'],
        auto_start_request=False,
        tz_aware=True,
        )
    config.registry.registerUtility(connection)
    config.add_request_method(db_connection, 'db_connection', property=True)
    config.add_request_method(db, 'db', property=True)
    config.add_subscriber(start_request, NewRequest)

    connection.register([
        Medium,
        ])

    log.info('Model configured...')


def db_connection(request):
    return request.registry.getUtility(IMongoConnection)


def db(request):
    return getattr(request.db_connection, DATABASE_NAME)


def start_request(event):
    """"""
    event.request.db_connection.start_request()
    event.request.add_finished_callback(end_request)


def end_request(request):
    request.db_connection.end_request()
