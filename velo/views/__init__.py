import logging

from pyramid.httpexceptions import HTTPOk
from pyramid.view import view_config

log = logging.getLogger(__name__)


def includeme(config):
    config.add_route('index', '/')
    config.add_route('health', '/health')
    config.scan()


@view_config(route_name='health')
def get_health(request):
    return HTTPOk()


@view_config(route_name='index', renderer='index.mako')
def get_index(request):
    return {}


@view_config(context='gridfs.grid_file.GridOut')
def render_file(context, request):
    request.content_md5 = str(context.md5)
    request.response.etag = str(context.md5)
    request.response.content_type = str(context.content_type)
    request.response.app_iter = context
    return request.response
