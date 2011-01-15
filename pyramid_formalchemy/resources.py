# -*- coding: utf-8 -*-

class AdminView(object):
    def __init__(self, request):
        self.request = request
        request.model_name = None
        request.model_id = None
        request.format = 'html'
        self.__parent__ = self.__name__ = None
    def __getitem__(self, item):
        if item in ('json', 'xhr'):
            self.request.format = item
            return self
        model = ModelListing(self.request, item)
        model.__parent__ = self
        return model

class ModelListing(object):
    def __init__(self, request, name):
        self.request = request
        request.model_name = name
        self.__name__ = name
        self.__parent__ = None
    def __getitem__(self, item):
        if item in ('json', 'xhr'):
            self.request.format = item
            return self
        if item in ('new',):
            raise KeyError()
        model = ModelItem(self.request, item)
        model.__parent__ = self
        return model

class ModelItem(object):
    def __init__(self, request, name):
        request.model_id = name
        self.__name__ = name
        self.__parent__ = None

