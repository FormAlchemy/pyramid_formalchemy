# -*- coding: utf-8 -*-
from chameleon.zpt.template import PageTemplate
from pyramid.util import DottedNameResolver
import functools

def action(name=None):
    def wrapper(func):
        action = name or func.__name__
        @functools.wraps(func)
        def wrapped(self, *args, **kwargs):
            request = self.request
            if request.format in ('html', 'xhr') and request.model_class is not None:
                for key in self.actions_categories:
                    attr = '%s_%s' % (action, key)
                    objects = getattr(request.model_class, attr, None)
                    if objects is None:
                        objects = self.defaults_actions.get(attr, Actions())
                    setattr(request, key, objects)
                request.action = func.__name__
            return func(self, *args, **kwargs)
        return wrapped
    return wrapper


class Action(object):
    """A model action is used to add some action in model views::

        >>> from webob import Request
        >>> request = Request.blank('/')

        >>> class MyAction(Action):
        ...     body = u'<a tal:attributes="%(attributes)s" tal:content="%(content)s"></a>'

        >>> action = MyAction('myaction', content=repr('Click here'), 
        ...                   attrs={'href': repr('#'), 'onclick': repr('$.click()')})
        >>> action.render(request)
        u'<a href="#" id="myaction" onclick="$.click()">Click here</a>'

    """

    def __init__(self, id, action='', content="", attrs=None, **rcontext):
        self.id = id
        self.attrs = attrs or {}
        self.rcontext = rcontext
        if 'id' not in self.attrs:
            self.attrs['id'] = repr(id)
        self.update()
        attributes = u';'.join([u'%s %s' % v for v in self.attrs.items()])
        rcontext.update(attrs=self.attrs, attributes=attributes, id=id, content=content, action=action)
        body = self.body % self.rcontext
        self.template = PageTemplate(body)

    def update(self):
        pass

    def render(self, request):
        rcontext = {'action': self, 'request': request}
        rcontext.update(self.rcontext)
        return self.template.render(**rcontext)

    def __repr__(self):
        return '<%s %s>' % (self.__class__.__name__, self.id)

class Link(Action):
    """
    An action rendered as a link::

        >>> from webob import Request
        >>> request = Request.blank('/')
        >>> action = Link('myaction', content='label',
        ...               attrs={'href': 'request.application_url'},
        ...               label='Click here')
        >>> action.render(request)
        u'<a href="http://localhost" id="myaction">Click here</a>'

    """
    body = u'<a tal:attributes="%(attributes)s" tal:content="%(content)s"></a>'

class Input(Action):
    """An action rendered as an input::

        >>> from webob import Request
        >>> request = Request.blank('/')
        >>> action = Input('myaction',
        ...                value=repr('Click here'))
        >>> action.render(request)
        u'<input type="submit" id="myaction" value="Myaction" />'

    """
    body = u'<input tal:attributes="%(attributes)s" />'

    def update(self):
        if 'value' not in self.attrs:
            self.attrs['value'] = repr(self.id.title())
        if 'type' not in self.attrs:
            self.attrs['type'] = repr('submit')

class UILink(Action):
    """An action rendered as an jquery.ui aware link::

        >>> from webob import Request
        >>> request = Request.blank('/')
        >>> action = UILink('myaction', icon='ui-icon-trash',
        ...                 label="string:Click here")
        >>> print action.render(request)
        <a class="ui-widget-header ui-widget-link ui-widget-button ui-corner-all " id="myaction">
          <span class="ui-icon ui-icon-trash"></span>
          Click here
        </a>
        
        >>> action = UILink('myaction', icon='ui-icon-trash',
        ...                 label="'Click here'", attrs={'onclick':'$(#link).click();'})
        >>> print action.render(request)
        <a class="ui-widget-header ui-widget-link ui-widget-button ui-corner-all " href="#" id="myaction" onclick="$(#link).click();">
          <span class="ui-icon ui-icon-trash"></span>
          Click here
        </a>
        
    """
    body = '''
<a class="ui-widget-header ui-widget-link ui-widget-button ui-corner-all ${state}"
   tal:attributes="%(attributes)s">
  <span class="ui-icon ${icon}"></span>
  <span tal:replace="%(label)s"></span>
</a>'''
    def update(self):
        if 'state' not in self.rcontext:
            self.rcontext['state'] = ''
        if 'onclick' in self.attrs:
            self.rcontext['onclick'] = self.attrs.pop('onclick')
            self.attrs['onclick'] = 'onclick'
            if 'href' not in self.attrs:
                self.attrs['href'] = repr('#')

class Actions(list):
    """
        >>> actions = Actions('pyramid_formalchemy.actions.delete',
        ...                   Link('link1', content=repr('A link'), attrs={'href':'request.application_url'}))
        >>> actions
        [<UILink delete>, <Link link1>]

        >>> from webob import Request
        >>> request = Request.blank('/')
        >>> print actions.render(request) #doctest: +ELLIPSIS
        <a class="ui-widget-header ...">
          <span class="ui-icon ui-icon-trash"></span>
          Delete
        </a><a href="http://localhost" id="link1">A link</a>
        
    """

    def __init__(self, *args):
        res = DottedNameResolver('pyramid_formalchemy.actions')
        list.__init__(self, [res.maybe_resolve(a) for a in args])

    def render(self, request, **kwargs):
        return u''.join([a.render(request, **kwargs) for a in self])


new = UILink(
        id='new',
        label='string:New ${request.model_name}',
        icon='ui-icon-circle-plus',
        attrs=dict(href="request.fa_url(request.model_name, 'new')"),
        )


save = UILink(
        id='save',
        label='string:Save',
        icon='ui-icon-check',
        attrs=dict(onclick="jQuery(this).parents('form').submit();"),
        )

save_and_add_another = UILink(
        id='save_and_add_another',
        label='string:Save and add another',
        icon='ui-icon-check',
        attrs=dict(onclick=("var f = jQuery(this).parents('form');"
                            "jQuery('#next', f).val(window.location.href);"
                            "f.submit();")),
        )

edit = UILink(
        id='edit',
        label='string:Edit',
        icon='ui-icon-check',
        attrs=dict(href="request.fa_url(request.model_name, request.model_id, 'edit')"),
        )

delete = UILink(
        id='delete',
        views='edit',
        label='string:Delete',
        state='ui-state-error',
        icon='ui-icon-trash',
        attrs=dict(onclick=("string:var f = jQuery(this).parents('form');"
                      "f.attr('action', window.location.href.replace('/edit', '/delete'));"
                      "f.submit();")),
        )

cancel = UILink(
        id='cancel',
        views='edit',
        label='string:Cancel',
        icon='ui-icon-circle-arrow-w',
        attrs=dict(href="request.fa_url(request.model_name)"),
        )

defaults_actions = dict(
    listing_buttons=Actions(new),
    new_buttons=Actions(save, save_and_add_another, cancel),
    show_buttons=Actions(edit, cancel),
    edit_buttons=Actions(save, delete, cancel),
)
