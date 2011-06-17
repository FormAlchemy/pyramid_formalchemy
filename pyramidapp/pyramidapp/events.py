from pyramid_formalchemy import events
from pyramidapp.models import Foo
import logging

log = logging.getLogger(__name__)

@events.subscriber([Foo, events.IBeforeValidateEvent])
def before_foo_validate(context, event):
    log.info("%r will be validated" % context)

@events.subscriber([Foo, events.IAfterSyncEvent])
def after_foo_sync(context, event):
    log.info("%r foo has been synced" % context)

@events.subscriber([Foo, events.IBeforeDeleteEvent])
def before_foo_delete(context, event):
    log.info("%r foo will be deleted" % context)

@events.subscriber([Foo, events.IBeforeRenderEvent])
def before_foo_render(context, event):
    log.info("%r foo will be rendered" % event.object)

@events.subscriber([Foo, events.IBeforeShowRenderEvent])
def before_foo_show_render(context, event):
    log.info("%r foo show will be rendered" % event.object)

@events.subscriber([Foo, events.IBeforeEditRenderEvent])
def before_foo_edit_render(context, event):
    log.info("%r foo edit will be rendered" % event.object)
