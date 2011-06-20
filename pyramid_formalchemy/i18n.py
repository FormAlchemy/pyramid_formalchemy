# -*- coding: utf-8 -*-
from pyramid.i18n import TranslationStringFactory
from pyramid.i18n import TranslationString
from pyramid.i18n import get_localizer

_ = TranslationStringFactory('pyramid_formalchemy')

class I18NModel(object):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @property
    def label(self):
        return getattr(self.context, '__label__', self.context.__name__)

    @property
    def plural(self):
        value = getattr(self.context, '__plural__', None)
        if value:
            return value
        else:
            return self.label

    def __getattr__(self, attr):
        return getattr(self.context, attr)

