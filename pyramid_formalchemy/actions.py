# -*- coding: utf-8 -*-
from chameleon.zpt.template import PageTemplate
from pyramid.util import DottedNameResolver
from pyramid_formalchemy.i18n import TranslationString
from pyramid_formalchemy.i18n import get_localizer
from pyramid_formalchemy.i18n import _
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
        ...     body = u'<a tal:attributes="%(attributes)s">${content}</a>'

        >>> action = MyAction('myaction', content=_('Click here'), 
        ...                   attrs={'href': repr('#'), 'onclick': repr('$.click()')})
        >>> action.render(request)
        u'<a href="#" id="myaction" onclick="$.click()">Click here</a>'

    """

    def __init__(self, id, content="", alt="", attrs=None, **rcontext):
        self.id = id
        self.attrs = attrs or {}
        self.rcontext = rcontext
        if 'id' not in self.attrs:
            self.attrs['id'] = repr(id)
        self.update()
        attributes = u';'.join([u'%s %s' % v for v in self.attrs.items()])
        rcontext.update(attrs=self.attrs, attributes=attributes, id=id)
        body = self.body % self.rcontext
        rcontext.update(content=content, alt=alt)
        self.template = PageTemplate(body)

    def update(self):
        pass

    def render(self, request):
        rcontext = {'action': self, 'request': request}
        rcontext.update(self.rcontext)
        localizer = get_localizer(request)
        mapping = getattr(request, 'action_mapping', {})
        if not mapping:
            for k in ('model_name', 'model_id'):
                mapping[k] = getattr(request, k, '')
            request.action_mapping = mapping
        for k in ('content', 'alt'):
            v = rcontext[k]
            if isinstance(v, TranslationString):
                v = TranslationString(v, domain=v.domain, mapping=request.action_mapping)
                rcontext[k] = localizer.translate(v)
        return self.template.render(**rcontext)

    def __repr__(self):
        return '<%s %s>' % (self.__class__.__name__, self.id)

class Link(Action):
    """
    An action rendered as a link::

        >>> from webob import Request
        >>> request = Request.blank('/')
        >>> action = Link('myaction',
        ...               attrs={'href': 'request.application_url'},
        ...               content=_('Click here'))
        >>> action.render(request)
        u'<a href="http://localhost" id="myaction">Click here</a>'

    """
    body = u'<a tal:attributes="%(attributes)s">${content}</a>'

class ListItem(Action):
    """
    An action rendered as a link::

        >>> from webob import Request
        >>> request = Request.blank('/')
        >>> action = ListItem('myaction',
        ...               attrs={'href': 'request.application_url'},
        ...               content=_('Click here'))
        >>> action.render(request)
        u'<li><a href="http://localhost" id="myaction">Click here</a></li>'

    """
    body = u'<li><a tal:attributes="%(attributes)s">${content}</a></li>'


class Input(Action):
    """An action rendered as an input::

        >>> from webob import Request
        >>> request = Request.blank('/')
        >>> action = Input('myaction',
        ...                value=_('Click here'))
        >>> action.render(request)
        u'<input type="submit" id="myaction" value="Myaction" />'

    """
    body = u'<input tal:attributes="%(attributes)s" />'

    def update(self):
        if 'value' not in self.attrs:
            self.attrs['value'] = repr(self.id.title())
        if 'type' not in self.attrs:
            self.attrs['type'] = repr('submit')

class UIButton(Action):
    """An action rendered as an jquery.ui aware link::

        >>> from webob import Request
        >>> request = Request.blank('/')
        >>> action = UIButton('myaction', icon='ui-icon-trash',
        ...                 content=_("Click here"))
        >>> print action.render(request)
        <a class="ui-widget-header ui-widget-link ui-widget-button ui-corner-all " id="myaction">
          <span class="ui-icon ui-icon-trash"></span>
          Click here
        </a>
        
        >>> action = UIButton('myaction', icon='ui-icon-trash',
        ...                 content=_("Click here"), attrs={'onclick':'$(#link).click();'})
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
  ${content}
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
        ...                   Link('link1', content=_('A link'), attrs={'href':'request.application_url'}))
        >>> actions
        [<UIButton delete>, <Link link1>]

        >>> from webob import Request
        >>> request = Request.blank('/')
        >>> print actions.render(request) #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
        <a class="ui-widget-header ...">
          <span class="ui-icon ui-icon-trash"></span>
          Delete
        </a>
        <a href="http://localhost" id="link1">A link</a>
        
    """

    def __init__(self, *args):
        res = DottedNameResolver('pyramid_formalchemy.actions')
        list.__init__(self, [res.maybe_resolve(a) for a in args])

    def render(self, request, **kwargs):
        return u'\n'.join([a.render(request, **kwargs) for a in self])

class Languages(Actions):
    """
        >>> langs = Languages('fr', 'en')
        >>> langs
        [<ListItem fr>, <ListItem en>]
        >>> from webob import Request
        >>> request = Request.blank('/')
        >>> request.cookies['_LOCALE_'] = 'fr'
        >>> request.route_url = lambda name, _query: 'http://localhost/set_language?_LOCALE_=%(_LOCALE_)s' % _query
        >>> print langs.render(request) #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
        <li><a href="http://localhost/set_language?_LOCALE_=fr" class="lang_fr lang_active" id="lang_fr">French</a></li>
        <li><a href="http://localhost/set_language?_LOCALE_=en" class="lang_en " id="lang_en">English</a></li>
        
    """
    translations = {
            'fr': _('French'),
            'en': _('English'),
            }

    def __init__(self, *args, **kwargs):
        list.__init__(self)
        klass=kwargs.get('class_', ListItem)
        for l in args:
            self.append(
                klass(id='lang_%s' % l,
                      content=self.translations.get(l, _(l)), attrs={
                        'class':"string:lang_%s ${request.cookies.get('_LOCALE_') == '%s' and 'lang_active' or ''}" % (l, l),
                        'href':"request.route_url('set_language', _query={'_LOCALE_': '%s'})" % l
                      }
                  ))

new = UIButton(
        id='new',
        content=_('New ${model_name}'),
        icon='ui-icon-circle-plus',
        attrs=dict(href="request.fa_url(request.model_name, 'new')"),
        )


save = UIButton(
        id='save',
        content=_('Save'),
        icon='ui-icon-check',
        attrs=dict(onclick="jQuery(this).parents('form').submit();"),
        )

save_and_add_another = UIButton(
        id='save_and_add_another',
        content=_('Save and add another'),
        icon='ui-icon-check',
        attrs=dict(onclick=("var f = jQuery(this).parents('form');"
                            "jQuery('#next', f).val(window.location.href);"
                            "f.submit();")),
        )

edit = UIButton(
        id='edit',
        content=_('Edit'),
        icon='ui-icon-check',
        attrs=dict(href="request.fa_url(request.model_name, request.model_id, 'edit')"),
        )

back = UIButton(
        id='back',
        content=_('Back'),
        icon='ui-icon-circle-arrow-w',
        attrs=dict(href="request.fa_url(request.model_name)"),
        )

delete = UIButton(
        id='delete',
        views='edit',
        content=_('Delete'),
        state='ui-state-error',
        icon='ui-icon-trash',
        attrs=dict(onclick=("string:var f = jQuery(this).parents('form');"
                      "f.attr('action', window.location.href.replace('/edit', '/delete'));"
                      "f.submit();")),
        )

cancel = UIButton(
        id='cancel',
        views='edit',
        content=_('Cancel'),
        icon='ui-icon-circle-arrow-w',
        attrs=dict(href="request.fa_url(request.model_name)"),
        )

defaults_actions = dict(
    listing_buttons=Actions(new),
    new_buttons=Actions(save, save_and_add_another, cancel),
    show_buttons=Actions(edit, back),
    edit_buttons=Actions(save, delete, cancel),
)
