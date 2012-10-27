# -*- coding: utf-8 -*-
from pyramid_rest.resource import Resource


hello = Resource('hello_world')

@hello.index()
def yo(context, request):
    return {'Hello': 'World!'}
