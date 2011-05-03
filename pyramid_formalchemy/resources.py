# -*- coding: utf-8 -*-
from pyramid.exceptions import NotFound
import logging

log = logging.getLogger(__name__)

class Base(object):

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
            raise NotFound()
        request.model_class = model_class
        return model_class

    def get_instance(self):
        model = self.get_model()
        session = self.request.session_factory()
        return session.query(model).get(self.request.model_id)

    def _fa_url(self, *args):
        matchdict = self.request.matchdict.copy()
        if 'traverse' in matchdict:
            del matchdict['traverse']
        return self.request.route_url(self.__fa_route_name__,
                                      traverse=tuple([str(a) for a in args]),
                                      **matchdict)



class Models(Base):

    def __init__(self, request):
        Base.__init__(self, request, None)

    def fa_url(self, *args):
        return self._fa_url(*args)

    def __getitem__(self, item):
        if item in ('json', 'xhr'):
            self.request.format = item
            return self
        model = ModelListing(self.request, item)
        model.__parent__ = self
        if hasattr(model, '__acl__'):
            # propagate permissions to parent
            self.__acl__ = model.__acl__
        return model

class ModelListing(Base):

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

    def fa_url(self, *args):
        return self._fa_url(*args[1:])

    def __getitem__(self, item):
        if item in ('json', 'xhr'):
            self.request.format = item
            return self
        if item in ('new',):
            raise KeyError()
        model = Model(self.request, item)
        model.__parent__ = self
        return model

class Model(Base):

    def fa_url(self, *args):
        return self._fa_url(*args[2:])

    def __init__(self, request, name):
        Base.__init__(self, request, name)
        query = request.session_factory.query(request.model_class)
        request.model_instance = request.query_factory(request, query, id=name)
        request.model_id = name

