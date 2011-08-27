import zope.component
__doc__ = """
Event subscription
==================

``pyramid_formalchemy`` provides four events: ``IBeforeValidateEvent``,
``IAfterSyncEvent``, ``IBeforeDeleteEvent`` and ``IBeforeRenderEvent``.
There are also two more specific render evnts: ``IBeforeShowRenderEvent``
and ``IBeforeEditRenderEvent``. You can use ``pyramid_formalchemy.events.subscriber``
decorator to subscribe:

.. literalinclude:: ../../pyramidapp/pyramidapp/events.py

"""


class IBeforeValidateEvent(zope.component.interfaces.IObjectEvent):
    """A model will be validated"""


class IAfterSyncEvent(zope.component.interfaces.IObjectEvent):
    """A model was synced with DB"""


class IBeforeDeleteEvent(zope.component.interfaces.IObjectEvent):
    """A model will be deleted"""


class IBeforeRenderEvent(zope.component.interfaces.IObjectEvent):
    """A model will rendered"""


class IBeforeListingRenderEvent(IBeforeRenderEvent):
    """Listing will be rendered"""


class IBeforeShowRenderEvent(IBeforeRenderEvent):
    """Show will be rendered"""


class IBeforeEditRenderEvent(IBeforeRenderEvent):
    """Edit will be rendered"""


class BeforeValidateEvent(zope.component.interfaces.ObjectEvent):
    """A model will be validated"""
    zope.interface.implements(IBeforeValidateEvent)

    def __init__(self, object, fs, request):
        self.object = object
        self.fs = fs
        self.request = request


class AfterSyncEvent(zope.component.interfaces.ObjectEvent):
    """A model was synced with DB"""
    zope.interface.implements(IAfterSyncEvent)

    def __init__(self, object, fs, request):
        self.object = object
        self.fs = fs
        self.request = request

class BeforeDeleteEvent(zope.component.interfaces.ObjectEvent):
    """A model will be deleted"""
    zope.interface.implements(IBeforeDeleteEvent)

    def __init__(self, object, request):
        self.object = object
        self.request = request


class BeforeRenderEvent(zope.component.interfaces.ObjectEvent):
    """A model will rendered"""
    zope.interface.implements(IBeforeRenderEvent)

    def __init__(self, object, request, **kwargs):
        self.object = object
        self.request = request
        self.kwargs = kwargs

class subscriber(object):
    """event subscriber decorator"""

    def __init__(self, ifaces):
        self.ifaces = ifaces

    def __call__(self, func):
        zope.component.provideHandler(func, self.ifaces)
