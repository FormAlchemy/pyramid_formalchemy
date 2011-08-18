# -*- coding: utf-8 -*-
from chameleon.zpt.template import PageTemplate
from pyramid.util import DottedNameResolver
from pyramid.security import has_permission
from pyramid_formalchemy.i18n import TranslationString
from pyramid_formalchemy.i18n import get_localizer
from pyramid_formalchemy.i18n import _
import functools

__doc__ = """
pyramid_formalchemy provide a way to use some ``actions`` in your template.
Action are basically links or input button.

By default there is only one category ``buttons`` which are the forms buttons
but you can add some categories like this::

    >>> from pyramid_formalchemy.views import ModelView
    >>> from pyramid_formalchemy import actions

    >>> class MyView(ModelView):
    ...     # keep default action categorie and add the custom_actions categorie
    ...     actions_categories = ('buttons', 'custom_actions')
    ...     # update the default actions for all models
    ...     defaults_actions = actions.defaults_actions.copy()
    ...     defaults_actions.update(edit_custom_actions=Actions())

Where ``myactions`` is an :class:`~pyramid_formalchemy.actions.Actions` instance

You can also customize the actions per Model::


    >>> from sqlalchemy import Column, Integer
    >>> from sqlalchemy.ext.declarative import declarative_base
    >>> Base = declarative_base()
    >>> class MyArticle(Base):
    ...     __tablename__ = 'myarticles'
    ...     edit_buttons = Actions()
    ...     id = Column(Integer, primary_key=True)

The available actions are:

- listing

- new

- edit

But you can add your own::

    >>> from pyramid_formalchemy.views import ModelView
    >>> from pyramid_formalchemy import actions
    >>> class MyView(ModelView):
    ...     actions.action()
    ...     def extra(self):
    ...         # do stuff
    ...         return self.render(**kw)

Then pyramid_formalchemy will try to load some ``extra_buttons`` actions.
"""

def action(name=None):
    """A decorator use to add some actions to the request.
    """
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
                    request.actions[key] = objects
                request.action = func.__name__
            return func(self, *args, **kwargs)
        return wrapped
    return wrapper


class Action(object):
    """A model action is used to add some action in model views. The content
    and alt parameters should be a :py:class:`pyramid.i18n.TranslationString`::

        >>> from webob import Request
        >>> request = Request.blank('/')

        >>> class MyAction(Action):
        ...     body = u'<a tal:attributes="%(attributes)s">${content}</a>'

        >>> action = MyAction('myaction', content=_('Click here'), 
        ...                   attrs={'href': repr('#'), 'onclick': repr('$.click()')})
        >>> action.render(request)
        u'<a href="#" id="myaction" onclick="$.click()">Click here</a>'

    """

    def __init__(self, id, content="", alt="", permission=None, attrs=None, **rcontext):
        self.id = id
        self.attrs = attrs or {}
        self.permission = permission
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
            for k in ('model_name', 'model_label', 'model_id'):
                mapping[k] = localizer.translate(getattr(request, k, ''))
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
    An action rendered as a link contained by a list item::

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
        ...                content=_('Click here'))

    Rendering::

        >>> action.render(request)
        u'<input value="Click here" type="submit" id="myaction" />'

    """
    body = u'<input tal:attributes="%(attributes)s" value="${content}"/>'

    def update(self):
        if 'type' not in self.attrs:
            self.attrs['type'] = repr('submit')

class Option(Action):
    """An action rendered as a select option::

        >>> from webob import Request
        >>> request = Request.blank('/')
        >>> action = Option('myaction',
        ...                  value='request.application_url',
        ...                  content=_('Click here'))

    Rendering::

        >>> action.render(request)
        u'<option id="myaction" value="http://localhost">Click here</option>'

    """

    body = u'<option tal:attributes="%(attributes)s">${content}</option>'

    def update(self):
        if 'value' not in self.attrs:
            self.attrs['value'] = self.rcontext.get('value', None)

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
        
    You can use javascript::

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
    """A action list. Can contain :class:`pyramid_formalchemy.actions.Action` or a dotted name::

        >>> actions = Actions('pyramid_formalchemy.actions.delete',
        ...                   Link('link1', content=_('A link'), attrs={'href':'request.application_url'}))
        >>> actions
        <Actions [<UIButton delete>, <Link link1>]>

    You must use a request to render them::

        >>> from webob import Request
        >>> request = Request.blank('/')
        >>> print actions.render(request) #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
        <a class="ui-widget-header ...">
          <span class="ui-icon ui-icon-trash"></span>
          Delete
        </a>
        <a href="http://localhost" id="link1">A link</a>

    You can add actions::

        >>> new_actions = Actions('pyramid_formalchemy.actions.new') + actions
        >>> new_actions
        <Actions [<UIButton new>, <UIButton delete>, <Link link1>]>
        
    """
    tag = u''
    def __init__(self, *args, **kwargs):
        self.sep = kwargs.get('sep', u'\n')
        res = DottedNameResolver('pyramid_formalchemy.actions')
        list.__init__(self, [res.maybe_resolve(a) for a in args])

    def render(self, request, **kwargs):
        allowed_permissions = []
        for a in self:
            if a.permission is None or has_permission(a.permission, request.context, request):
                allowed_permissions.append(a)
        return self.sep.join([a.render(request, **kwargs) for a in allowed_permissions])

    def __add__(self, other):
        actions = list(self)+list(other)
        actions = self.__class__(*actions)
        actions.sep = self.sep
        return actions

    def __nonzero__(self):
        return bool(len(self))

    def __repr__(self):
        return '<%s %s>' % (self.__class__.__name__, list.__repr__(self))

class RequestActions(dict):
    """An action container used to store action in requests.
    Return an empty Actions instance if actions are not found"""

    def __getattr__(self, attr):
        actions = self.get(attr, Actions())
        if actions:
            return actions.render
        return None

class Languages(Actions):
    """Languages actions::

        >>> langs = Languages('fr', 'en')
        >>> langs
        <Languages [<ListItem lang_fr>, <ListItem lang_en>]>

    It take care about the active language::

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
            'pt_BR': _('Brazilian'),
            }

    def __init__(self, *args, **kwargs):
        Actions.__init__(self)
        klass=kwargs.get('class_', ListItem)
        for l in args:
            self.append(
                klass(id='lang_%s' % l,
                      content=self.translations.get(l, _(l)), attrs={
                        'class':"string:lang_%s ${request.cookies.get('_LOCALE_') == '%s' and 'lang_active' or ''}" % (l, l),
                        'href':"request.route_url('set_language', _query={'_LOCALE_': '%s'})" % l
                      }
                  ))


class Themes(Actions):
    themes = (
        'black_tie',
        'blitzer',
        'cupertino',
        'dark_hive',
        'dot_luv',
        'eggplant',
        'excite_bike',
        'flick',
        'hot_sneaks',
        'humanity',
        'le_frog',
        'mint_choc',
        'overcast',
        'pepper_grinder',
        'redmond',
        'smoothness',
        'south_street',
        'start',
        'sunny',
        'swanky_purse',
        'trontastic',
        'ui_darkness',
        'ui_lightness',
        'vader',
      )

    def __init__(self, *args, **kwargs):
        Actions.__init__(self)
        klass=kwargs.get('class_', Option)
        if len(args) == 1 and args[0] == '*':
            args = self.themes
        for theme in args:
            label = theme.replace('_', ' ')
            self.append(
                klass(id='theme_%s' % theme,
                      content=_(label), attrs={
                        'selected':"string:${request.cookies.get('_THEME_') == '%s' and 'selected' or None}" % theme,
                        'value':"request.route_url('set_theme', _query={'_THEME_': '%s'})" % theme
                      }
                  ))


new = UIButton(
        id='new',
        content=_('New ${model_label}'),
        permission='new',
        icon='ui-icon-circle-plus',
        attrs=dict(href="request.fa_url(request.model_name, 'new')"),
        )


save = UIButton(
        id='save',
        content=_('Save'),
        permission='edit',
        icon='ui-icon-check',
        attrs=dict(onclick="jQuery(this).parents('form').submit();"),
        )

save_and_add_another = UIButton(
        id='save_and_add_another',
        content=_('Save and add another'),
        permission='edit',
        icon='ui-icon-check',
        attrs=dict(onclick=("var f = jQuery(this).parents('form');"
                            "jQuery('#next', f).val(window.location.href);"
                            "f.submit();")),
        )

edit = UIButton(
        id='edit',
        content=_('Edit'),
        permission='edit',
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
        content=_('Delete'),
        permission='delete',
        state='ui-state-error',
        icon='ui-icon-trash',
        attrs=dict(onclick=("var f = jQuery(this).parents('form');"
                      "f.attr('action', window.location.href.replace('/edit', '/delete'));"
                      "f.submit();")),
        )

cancel = UIButton(
        id='cancel',
        content=_('Cancel'),
        permission='view',
        icon='ui-icon-circle-arrow-w',
        attrs=dict(href="request.fa_url(request.model_name)"),
        )

defaults_actions = RequestActions(
    listing_buttons=Actions(new),
    new_buttons=Actions(save, save_and_add_another, cancel),
    show_buttons=Actions(edit, back),
    edit_buttons=Actions(save, delete, cancel),
)
