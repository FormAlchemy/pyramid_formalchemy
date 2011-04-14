# -*- coding: utf-8 -*-
import logging

log = logging.getLogger(__name__)

class Base(object):

    def __init__(self, request, name):
        self.__name__ = name
        self.__parent__ = None
        self.request = request
        if hasattr(self, '__fa_route_name__'):
            request.session_factory = self.__session_factory__
            request.route_name = self.__fa_route_name__
            request.model = self.__models__
            request.forms = self.__forms__
            request.fa_url = self.fa_url
            request.model_class = None
            request.model_name = None
            request.model_id = None
            request.format = 'html'

    def get_model(self):
        request = self.request
        if request.model_class:
            return request.model_class
        if request.model_name:
            if isinstance(request.model, list):
                for model in request.model:
                    if model.__name__ == request.model_name:
                        request.model_class = model
                        return request.model_class
            elif hasattr(request.model, request.model_name):
                request.model_class = getattr(request.model, request.model_name)
                return request.model_class
        raise NotFound()


class Models(Base):

    def __init__(self, request):
        Base.__init__(self, request, None)

    def fa_url(self, *args):
        return self.request.route_url(self.__fa_route_name__,
                                      traverse='/'.join([str(a) for a in args]))

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

    def __init__(self, request, name):
        Base.__init__(self, request, name)
        request.model_name = name
        model = self.get_model()
        if hasattr(model, '__acl__'):
            # get permissions from SA class
            self.__acl__ = model.__acl__

    def fa_url(self, *args):
        args = args[1:]
        return self.request.route_url(self.__fa_route_name__,
                                      traverse='/'.join([str(a) for a in args]))
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
        args = args[2:]
        return self.request.route_url(self.__fa_route_name__,
                                      traverse='/'.join([str(a) for a in args]))

    def __init__(self, request, name):
        Base.__init__(self, request, name)
        request.model_id = name

