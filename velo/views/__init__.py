import logging
from functools import wraps

from onctuous import All, Coerce, InRange, Required, Schema

from pyramid.view import view_defaults, view_config
from pyramid.httpexceptions import (
    HTTPOk,
    HTTPCreated,
    HTTPConflict,
    HTTPBadRequest,
    HTTPInternalServerError,
    HTTPNotFound,
    HTTPMethodNotAllowed,
    )

from velo import exceptions as exc
from velo.resources import meta

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


class BaseView(object):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def wrap_dict(self, item, item_dict):
        links = dict((k, self.request.resource_url(v))
                     for k, v in item.links.iteritems())
        return {'links': links, item.resource_name: item_dict}


def get_params(request):
    try:
        return request.POST
    except Exception:
        log.debug('Error parsing POST', exc_info=True)
        raise HTTPBadRequest('Error parsing request parameters')


@view_defaults(route_name='api', context=meta.Collection, renderer='velo')
class CollectionView(BaseView):

    index_schema = Schema({
        Required('page', 0): All(Coerce(int), InRange(min=0)),
        Required('page_size', 20): All(Coerce(int), InRange(min=1)),
        }, extra=True)

    @view_config(request_method='GET')
    def index(self):
        query = self.index_schema(dict(self.request.GET))
        page = query['page']
        page_size = query['page_size']

        result = self.context.index(limit=page_size, page=page)

        items = [self.wrap_dict(item, item.model) for item in result]

        self_url = self.request.resource_url(
            self.context,
            query={'page': page, 'page_size': page_size},
            )
        links = {'self': self_url}
        if page > 0:
            links['previous_page'] = self.request.resource_url(
                self.context,
                query={'page': page - 1, 'page_size': page_size},
                )
        total = result.total
        if total > (page + 1) * page_size:
            links['next_page'] = self.request.resource_url(
                self.context,
                query={'page': page + 1, 'page_size': page_size},
                )
        links['last_page'] = self.request.resource_url(
            self.context,
            query={'page': total / page_size - 1, 'page_size': page_size},
            )
        return {self.context.collection_name: items, 'links': links}

    @view_config(request_method='POST', permission='edit')
    def create(self):
        item = self.context.create(get_params(self.request))
        item_url = self.request.resource_url(item)
        self.request.response.headers['Location'] = item_url
        self.request.response.status_int = HTTPCreated.code
        return self.wrap_dict(item, item.model)


@view_defaults(route_name='api', context=meta.Resource, renderer='velo')
class ResourceView(BaseView):

    @view_config(request_method='GET')
    def show(self):
        item = self.context.show()
        return self.wrap_dict(self.context, item)

    @view_config(request_method='PUT', permission='edit')
    def put(self):
        item = self.context.put(get_params(self.request))
        return self.wrap_dict(self.context, item)

    @view_config(request_method='PATCH', permission='edit')
    def patch(self):
        self.context.patch(get_params(self.request))
        return self.request.response

    @view_config(request_method='DELETE', permission='edit')
    def delete(self):
        self.context.delete()
        return self.request.response


@view_config(route_name='api', context=exc.MethodNotAllowed)
@view_config(route_name='api', context=meta.Collection)
@view_config(route_name='api', context=meta.Resource)
@view_config(route_name='api', context=meta.Root)
def not_allowed(context, request):
    return HTTPMethodNotAllowed()


def log_error_dict(view_callable):
    @wraps(view_callable)
    def wrapper(context, request):
        result = view_callable(context, request)
        log.debug('%s: %s', type(context), result)
        return result
    return wrapper


@view_config(route_name='api', context=exc.NotFound, renderer='velo')
@log_error_dict
def item_not_found(context, request):
    request.response.status_int = HTTPNotFound.code
    return {
        'error': 'not_found',
        'resource': request.resource_url(context.resource)
        }


@view_config(route_name='api', context=exc.Conflict, renderer='velo')
@log_error_dict
def conflict(context, request):
    request.response.status_int = HTTPConflict.code
    return {
        'error': 'already_exists',
        'resource': request.resource_url(context.resource)
        }


@view_config(route_name='api', context='onctuous.errors.Invalid',
             renderer='velo')
@log_error_dict
def invalid_parameters(context, request):
    request.response.status_int = HTTPBadRequest.code
    return {
        'error': 'invalid_parameters',
        'message': unicode(context)
        }


@view_config(route_name='api', context=exc.BadParameter, renderer='velo')
@log_error_dict
def bad_parameter(context, request):
    request.response.status_int = HTTPBadRequest.code
    return {
        'error': 'invalid_parameters',
        'message': '%s="%s"' % (context.name, context.value)
        }


#@view_config(route_name='api', context=Exception, renderer='velo')
@log_error_dict
def exception(context, request):
    request.response.status_int = HTTPInternalServerError.code
    return {
        'error': 'unexpected_error',
        'message': unicode(context),
        'error_class': type(context).__name__,
        }


@view_config(route_name='api', context='gridfs.grid_file.GridOut')
def render_file(context, request):
    request.content_md5 = str(context.md5)
    request.response.etag = str(context.md5)
    request.response.content_type = str(context.content_type)
    request.response.app_iter = context
    return request.response
