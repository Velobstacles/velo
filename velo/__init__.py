# -*- coding: utf-8 -*-
import logging

from pyramid.config import Configurator

log = logging.getLogger(__name__)


def main(global_config, **settings):
    log.info('Starting...')
    config = Configurator(settings=settings)
    config.include('pyramid_rest')
    config.scan('velo.views')
    log.info('Ready to serve...')
    return config.make_wsgi_app()
