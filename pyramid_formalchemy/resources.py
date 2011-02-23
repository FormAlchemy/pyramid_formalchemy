# -*- coding: utf-8 -*-

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
            request.model_name = None
            request.model_id = None
            request.format = 'html'

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
        return model

class ModelListing(Base):

    def __init__(self, request, name):
        Base.__init__(self, request, name)
        request.model_name = name

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

