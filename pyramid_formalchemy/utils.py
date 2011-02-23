# -*- coding: utf-8 -*-
from formalchemy.templates import TemplateEngine as BaseTemplateEngine
from formalchemy import config
from formalchemy import fatypes
from webhelpers.html import literal
from pyramid.renderers import render

class TemplateEngine(BaseTemplateEngine):
    """A template engine aware of pyramid"""

    def __init__(self, *args, **kwargs):
        """Do nothing. Almost all the mechanism is deleged to pyramid.renderers"""

    def render(self, name=None, renderer=None, template=None, **kwargs):
        renderer = renderer or template
        if renderer is None:
            name = name.strip('/')
            if not name.endswith('.pt'):
                name = '%s.pt' % name
            renderer = 'pyramid_formalchemy:templates/forms/%s' % name
        kwargs.update(dict(
            fatypes=fatypes,
        ))
        return literal(render(renderer, kwargs))

config.engine = TemplateEngine()
