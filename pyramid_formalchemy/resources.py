# -*- coding: utf-8 -*-
from pyramid.exceptions import NotFound
from pyramid_formalchemy import actions
from sqlalchemy import exceptions as sqlalchemy_exceptions
import logging

log = logging.getLogger(__name__)

class Base(object):
    """Base class used for all traversed class.
    Allow to access to some useful attributes via request::

    - model_class
    - model_name
    - model_instance
    - model_id
    - fa_url
    """

    def __init__(self, request, name):
        self.__name__ = name
        self.__parent__ = None
        self.request = request
        if hasattr(self, '__fa_route_name__'):
            request.session_factory = self.__session_factory__
            request.query_factory = self.__query_factory__
            request.route_name = self.__fa_route_name__
            request.models = self.__models__
            request.forms = self.__forms__
            request.fa_url = self.fa_url
            request.model_instance = None
            request.model_class = None
            request.model_name = None
            request.model_id = None
            request.relation = None
            request.format = 'html'
            if self.__model_class__:
                request.model_class = self.__model_class__
                request.model_name = self.__model_class__.__name__
            request.actions = actions.RequestActions()
            langs = request.registry.settings.get('available_languages', '')
            if langs:
                if isinstance(langs, basestring):
                    langs = langs.split()
                request.actions['languages'] = actions.Languages(*langs)
            themes = request.registry.settings.get('available_themes', '')
            if themes:
                if isinstance(themes, basestring):
                    themes = themes.split()
                request.actions['themes'] = actions.Themes(*themes)

    def get_model(self):
        request = self.request
        if request.model_class:
            return request.model_class
        model_name = request.model_name
        model_class = None
        if isinstance(request.models, list):
            for model in request.models:
                if model.__name__ == model_name:
                    model_class = model
                    break
        elif hasattr(request.models, model_name):
            model_class = getattr(request.models, model_name)
        if model_class is None:
            raise NotFound(request.path)
        request.model_class = model_class
        return model_class

    def get_instance(self):
        model = self.get_model()
        session = self.request.session_factory()
        return session.query(model).get(self.request.model_id)

    def _fa_url(self, *args, **kwargs):
        matchdict = self.request.matchdict.copy()
        if 'traverse' in matchdict:
            del matchdict['traverse']
        if kwargs:
            matchdict['_query'] = kwargs
        return self.request.route_url(self.__fa_route_name__,
                                      traverse=tuple([str(a) for a in args]),
                                      **matchdict)



class Models(Base):
    """Root of the CRUD interface"""

    def __init__(self, request):
        Base.__init__(self, request, None)

    def fa_url(self, *args, **kwargs):
        return self._fa_url(*args, **kwargs)

    def __getitem__(self, item):
        if item in ('json', 'xhr'):
            self.request.format = item
            return self

        self.request.model_name = item
        model_class = self.get_model()
        mixin_name = '%sCustom%s_%s__%s' % (model_class.__name__, ModelListing.__name__,
                                           self.request.route_name, self.request.method)
        mixin = type(mixin_name, (ModelListing, ), {})
        factory = self.request.registry.pyramid_formalchemy_views.get(mixin.__name__, mixin)
        model = factory(self.request, item)
        model.__parent__ = self
        if hasattr(model, '__acl__'):
            # propagate permissions to parent
            self.__acl__ = model.__acl__
        return model

class ModelListing(Base):
    """Context used for model classes"""

    def __init__(self, request, name=None):
        Base.__init__(self, request, name)
        if name is None:
            # request.model_class and request.model_name are already set
            model = request.model_class
        else:
            request.model_name = name
            model = self.get_model()
        if hasattr(model, '__acl__'):
            # get permissions from SA class
            self.__acl__ = model.__acl__

    def fa_url(self, *args, **kwargs):
        return self._fa_url(*args[1:], **kwargs)

    def __getitem__(self, item):
        if item in ('json', 'xhr'):
            self.request.format = item
            return self

        name = self.request.path.split('/')[-1] #view name
        if name == item:
            name = ''

        mixin_name = '%sCustom%s_%s_%s_%s' % (self.request.model_class.__name__, Model.__name__,
                                              self.request.route_name, name, self.request.method)
        mixin = type(str(mixin_name), (Model, ), {})
        factory = self.request.registry.pyramid_formalchemy_views.get(mixin.__name__, mixin)
        try:
            model = factory(self.request, item)
        except NotFound:
            raise KeyError()
        model.__parent__ = self
        return model

class Model(Base):
    """Context used for model instances"""

    def fa_url(self, *args, **kwargs):
        return self._fa_url(*args[2:], **kwargs)

    def __init__(self, request, name):
        Base.__init__(self, request, name)
        query = request.session_factory.query(request.model_class)
        try:
            request.model_instance = request.query_factory(request, query, id=name)
        except sqlalchemy_exceptions.SQLAlchemyError, exc:
            log.exception(exc)
            request.session_factory().rollback()
            raise NotFound(request.path)

        if request.model_instance is None:
            raise NotFound(request.path)
        request.model_id = name

