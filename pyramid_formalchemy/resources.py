# -*- coding: utf-8 -*-

class Base(object):

    def __init__(self, request, name):
        self.__name__ = name
        self.__parent__ = None
        self.request = request
        if hasattr(self, '__fa_route_name__'):
            request.forms = self.__forms__
            request.model = self.__models__
            request.route_name = self.__fa_route_name__
            request.session_factory = self.__session_factory__

class Models(Base):

    def __init__(self, request):
        Base.__init__(self, request, None)
        request.model_name = None
        request.model_id = None
        request.format = 'html'

    def __getitem__(self, item):
        if item in ('json', 'xhr'):
            self.request.format = item
            return self
        model = ModelListing(self.request, item)
        model.__parent__ = self
        return model

class ModelListing(Base):

    def __init__(self, request, name):
        Base.__init__(self, request, name)
        request.model_name = name

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

    def __init__(self, request, name):
        Base.__init__(self, request, name)
        request.model_id = name

