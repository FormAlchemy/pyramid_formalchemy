# -*- coding: utf-8 -*-
import zope.component.event
from zope.interface import alsoProvides
from webhelpers.paginate import Page
from sqlalchemy.orm import class_mapper
from formalchemy.fields import _pk
from formalchemy.fields import _stringify
from formalchemy.i18n import get_translator
from formalchemy.fields import Field
from formalchemy import fatypes
from pyramid.renderers import get_renderer
from pyramid.response import Response
from pyramid.security import has_permission
from pyramid.i18n import get_locale_name
from pyramid import httpexceptions as exc
from pyramid.exceptions import NotFound
from pyramid_formalchemy.utils import TemplateEngine
from pyramid_formalchemy.i18n import I18NModel
from pyramid_formalchemy import events
from pyramid_formalchemy import actions

try:
    from formalchemy.ext.couchdb import Document
except ImportError:
    Document = None

try:
    import simplejson as json
except ImportError:
    import json

class Session(object):
    """A abstract class to implement other backend than SA"""
    def add(self, record):
        """add a record"""
    def update(self, record):
        """update a record"""
    def delete(self, record):
        """delete a record"""
    def commit(self):
        """commit transaction"""

def set_language(request):
    """Set the _LOCALE_ cookie used by ``pyramid``"""
    resp = exc.HTTPFound(location=request.referer or request.application_url)
    resp.set_cookie('_LOCALE_', request.GET.get('_LOCALE_', 'en'))
    return resp

def set_theme(request):
    """Set the _THEME_ cookie used by ``pyramid_formalchemy`` to get a
    jquery.ui theme"""
    resp = exc.HTTPFound(location=request.referer or request.application_url)
    resp.set_cookie('_THEME_', request.GET.get('_THEME_', 'smoothness'))
    return resp

class ModelView(object):
    """A RESTful view bound to a model"""

    engine = TemplateEngine()
    pager_args = dict(link_attr={'class': 'ui-pager-link ui-state-default ui-corner-all'},
                      curpage_attr={'class': 'ui-pager-curpage ui-state-highlight ui-corner-all'})

    actions_categories = ('buttons',)
    defaults_actions = actions.defaults_actions

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.session = request.session_factory

        self.fieldset_class = request.forms.FieldSet
        self.grid_class = request.forms.Grid
        if '_LOCALE_' not in request.cookies:
            locale = get_locale_name(request)
            request.cookies['_LOCALE_'] = locale
        if '_LOCALE_' not in request.cookies:
            theme = request.registry.settings.get('default_theme_name', 'smoothness')
            request.cookies['_LOCALE_'] = theme

    def models(self, **kwargs):
        """Models index page"""
        request = self.request
        models = []
        if isinstance(request.models, list):
            for model in request.models:
                if has_permission('view', model, request) or not hasattr(model, '__acl__'):
                    key = model.__name__
                    models.append(model)
        else:
            for key, obj in request.models.__dict__.iteritems():
                if not key.startswith('_'):
                    if Document is not None:
                        try:
                            if issubclass(obj, Document):
                                if has_permission('view', obj, request) or not hasattr(model, '__acl__'):
                                    models.append(obj)
                                continue
                        except:
                            pass
                    try:
                        class_mapper(obj)
                    except:
                        continue
                    if not isinstance(obj, type):
                        continue
                    if has_permission('view', obj, request) or not hasattr(obj, '__acl__'):
                        models.append(obj)

        results = {}
        for m in models:
            if request.format == 'html':
                url = request.fa_url(m.__name__)
            else:
                url = request.fa_url(m.__name__, request.format)
            results[I18NModel(m, request).plural] = url

        if kwargs.get('json'):
            return results
        return self.render(models=results)

    def sync(self, fs, id=None):
        """sync a record. If ``id`` is None add a new record else save current one."""
        if id:
            self.session.merge(fs.model)
        else:
            self.session.add(fs.model)
        event = events.AfterSyncEvent(fs.model, fs, self.request)
        zope.component.event.objectEventNotify(event)

    def validate(self, fs):
        """validate fieldset"""
        event = events.BeforeValidateEvent(fs.model, fs, self.request)
        zope.component.event.objectEventNotify(event)
        return fs.validate()

    def breadcrumb(self, fs=None, **kwargs):
        """return items to build the breadcrumb"""
        items = []
        request = self.request
        model_name = request.model_name
        id = request.model_id
        items.append((request.fa_url(), 'root', 'root_url'))
        if request.model_name:
            items.append((request.fa_url(model_name), model_name, 'model_url'))
        if id and hasattr(fs.model, '__unicode__'):
            items.append((request.fa_url(model_name, id), u'%s' % self.context.get_instance(), 'instance_url'))
        elif id:
            items.append((request.fa_url(model_name, id), id, 'instance_url'))
        return items

    def render(self, **kwargs):
        """render the form as html or json"""
        request = self.request
        if request.format != 'html':
            meth = getattr(self, 'render_%s_format' % request.format, None)
            if meth is not None:
                return meth(**kwargs)
            else:
                raise NotFound()

        if request.model_class:
            request.model_class = model_class = I18NModel(request.model_class, request)
            request.model_label = model_label = model_class.label
            request.model_plural = model_plural = model_class.plural
        else:
            model_class = request.model_class
            model_label = model_plural = ''
        self.update_resources()
        kwargs.update(
                      main = get_renderer('pyramid_formalchemy:templates/admin/master.pt').implementation(),
                      model_class=model_class,
                      model_name=request.model_name,
                      model_label=model_label,
                      model_plural=model_plural,
                      breadcrumb=self.breadcrumb(**kwargs),
                      actions=request.actions,
                      F_=get_translator()),
        return kwargs

    def render_grid(self, **kwargs):
        """render the grid as html or json"""
        return self.render(is_grid=True, **kwargs)

    def render_json_format(self, fs=None, **kwargs):
        request = self.request
        request.override_renderer = 'json'
        if fs is not None:
            data = fs.to_dict(with_prefix=request.params.get('with_prefix', False))
            pk = _pk(fs.model)
            if pk:
                if 'id' not in data:
                    data['id'] = pk
                data['absolute_url'] = request.fa_url(request.model_name, 'json', pk)
        else:
            data = {}
        data.update(kwargs)
        return data

    def render_xhr_format(self, fs=None, **kwargs):
        self.request.response_content_type = 'text/html'
        if fs is not None:
            if 'field' in self.request.GET:
                field_name = self.request.GET.get('field')
                fields = fs.render_fields
                if field_name in fields:
                    field = fields[field_name]
                    return Response(field.render())
                else:
                    raise NotFound()
            return Response(fs.render())
        return Response('')

    def get_page(self, **kwargs):
        """return a ``webhelpers.paginate.Page`` used to display ``Grid``.
        """
        request = self.request
        def get_page_url(page, partial=None):
            url = "%s?page=%s" % (self.request.path, page)
            if partial:
                url += "&partial=1"
            return url
        options = dict(page=int(request.GET.get('page', '1')),
                       url=get_page_url)
        options.update(kwargs)
        if 'collection' not in options:
            query = self.session.query(request.model_class)
            options['collection'] = request.query_factory(request, query)
        collection = options.pop('collection')
        return Page(collection, **options)

    def get_fieldset(self, suffix='', id=None):
        """return a ``FieldSet`` object bound to the correct record for ``id``.
        """
        request = self.request
        model = id and request.model_instance or request.model_class
        form_name = request.model_name + suffix
        fs = getattr(request.forms, form_name, None)
        if fs is None:
            fs = getattr(request.forms, request.model_name,
                         self.fieldset_class)
        if fs is self.fieldset_class:
            fs = fs(request.model_class)
            if not isinstance(request.forms, list):
                # add default fieldset to form module eg: caching
                setattr(request.forms, form_name, fs)
        fs.engine = fs.engine or self.engine
        fs = id and fs.bind(model) or fs.copy()
        fs._request = request
        return fs

    def get_grid(self):
        """return a Grid object"""
        request = self.request
        model_name = request.model_name
        form_name = '%sGrid' % model_name
        if hasattr(request.forms, form_name):
            g = getattr(request.forms, form_name)
            g.engine = g.engine or self.engine
            g.readonly = True
            g._request = self.request
            self.update_grid(g)
            return g
        model = self.context.get_model()
        grid = self.grid_class(model)
        grid.engine = self.engine
        if not isinstance(request.forms, list):
            # add default grid to form module eg: caching
            setattr(request.forms, form_name, grid)
        grid = grid.copy()
        grid._request = self.request
        self.update_grid(grid)
        return grid


    def update_grid(self, grid):
        """Add edit and delete buttons to ``Grid``"""
        try:
            grid.edit
        except AttributeError:
            def edit_link():
                return lambda item: '''
                <form action="%(url)s" method="GET" class="ui-grid-icon ui-widget-header ui-corner-all">
                <input type="submit" class="ui-grid-icon ui-icon ui-icon-pencil" title="%(label)s" value="%(label)s" />
                </form>
                ''' % dict(url=self.request.fa_url(self.request.model_name, _pk(item), 'edit'),
                            label=get_translator(request=self.request)('edit'))
            def delete_link():
                return lambda item: '''
                <form action="%(url)s" method="POST" class="ui-grid-icon ui-state-error ui-corner-all">
                <input type="submit" class="ui-icon ui-icon-circle-close" title="%(label)s" value="%(label)s" />
                </form>
                ''' % dict(url=self.request.fa_url(self.request.model_name, _pk(item), 'delete'),
                           label=get_translator(request=self.request)('delete'))
            grid.append(Field('edit', fatypes.String, edit_link()))
            grid.append(Field('delete', fatypes.String, delete_link()))
            grid.readonly = True

    def update_resources(self):
        """A hook to add some fanstatic resources"""
        pass

    @actions.action()
    def listing(self, **kwargs):
        """listing page"""
        page = self.get_page(**kwargs)
        fs = self.get_grid()
        fs = fs.bind(instances=page, request=self.request)
        fs.readonly = True

        event = events.BeforeRenderEvent(self.request.model_class(), self.request, fs=fs, page=page)
        alsoProvides(event, events.IBeforeListingRenderEvent)
        zope.component.event.objectEventNotify(event)

        if self.request.format == 'json':
            values = []
            request = self.request
            for item in page:
                pk = _pk(item)
                fs._set_active(item)
                value = dict(id=pk,
                             absolute_url=request.fa_url(request.model_name, pk))
                if 'jqgrid' in request.GET:
                    fields = [_stringify(field.render_readonly()) for field in fs.render_fields.values()]
                    value['cell'] = [pk] + fields
                else:
                    value.update(fs.to_dict(with_prefix=bool(request.params.get('with_prefix'))))
                values.append(value)
            return self.render_json_format(rows=values,
                                           records=len(values),
                                           total=page.page_count,
                                           page=page.page)
        if 'pager' not in kwargs:
            pager = page.pager(**self.pager_args)
        else:
            pager = kwargs.pop('pager')
        return self.render_grid(fs=fs, id=None, pager=pager)

    @actions.action()
    def show(self):
        id = self.request.model_id
        fs = self.get_fieldset(suffix='View', id=id)
        fs.readonly = True

        event = events.BeforeRenderEvent(self.request.model_instance, self.request, fs=fs)
        alsoProvides(event, events.IBeforeShowRenderEvent)
        zope.component.event.objectEventNotify(event)

        return self.render(fs=fs, id=id)

    @actions.action()
    def new(self):
        fs = self.get_fieldset(suffix='Add')
        fs = fs.bind(session=self.session, request=self.request)

        event = events.BeforeRenderEvent(fs.model, self.request, fs=fs)
        alsoProvides(event, events.IBeforeEditRenderEvent)
        zope.component.event.objectEventNotify(event)

        return self.render(fs=fs, id=None)

    @actions.action('new')
    def create(self):
        request = self.request
        fs = self.get_fieldset(suffix='Add')

        event = events.BeforeRenderEvent(fs.model, self.request, fs=fs)
        alsoProvides(event, events.IBeforeEditRenderEvent)
        zope.component.event.objectEventNotify(event)

        if request.format == 'json' and request.method == 'PUT':
            data = json.load(request.body_file)
        elif request.content_type == 'application/json':
            data = json.load(request.body_file)
        else:
            data = request.POST

        with_prefix = True
        if request.format == 'json':
            with_prefix = bool(request.params.get('with_prefix'))

        fs = fs.bind(data=data, session=self.session, request=request, with_prefix=with_prefix)
        #try:
        #    fs = fs.bind(data=data, session=self.session, request=request, with_prefix=with_prefix)
        #except Exception:
        #    # non SA forms
        #    fs = fs.bind(self.context.get_model(), data=data, session=self.session,
        #                 request=request, with_prefix=with_prefix)

        if self.validate(fs):
            fs.sync()
            self.sync(fs)
            self.session.flush()
            if request.format in ('html', 'xhr'):
                if request.is_xhr or request.format == 'xhr':
                    return Response(content_type='text/plain')
                next = request.POST.get('next') or request.fa_url(request.model_name)
                return exc.HTTPFound(
                    location=next)
            else:
                fs.rebind(fs.model, data=None)
                return self.render(fs=fs)
        return self.render(fs=fs, id=None)

    @actions.action()
    def edit(self):
        id = self.request.model_id
        fs = self.get_fieldset(suffix='Edit', id=id)

        event = events.BeforeRenderEvent(self.request.model_instance, self.request, fs=fs)
        alsoProvides(event, events.IBeforeEditRenderEvent)
        zope.component.event.objectEventNotify(event)

        return self.render(fs=fs, id=id)

    @actions.action('edit')
    def update(self):
        request = self.request
        id = request.model_id
        fs = self.get_fieldset(suffix='Edit', id=id)

        event = events.BeforeRenderEvent(self.request.model_instance, self.request, fs=fs)
        alsoProvides(event, events.IBeforeEditRenderEvent)
        zope.component.event.objectEventNotify(event)

        if request.format == 'json' and request.method == 'PUT':
            data = json.load(request.body_file)
        elif request.content_type == 'application/json':
            data = json.load(request.body_file)
        else:
            data = request.POST

        with_prefix = True
        if request.format == 'json':
            with_prefix = bool(request.params.get('with_prefix'))

        fs = fs.bind(request=request, with_prefix=with_prefix)
        if self.validate(fs):
            fs.sync()
            self.sync(fs, id)
            self.session.flush()
            if request.format in ('html', 'xhr'):
                if request.is_xhr or request.format == 'xhr':
                    return Response(content_type='text/plain')
                return exc.HTTPFound(
                        location=request.fa_url(request.model_name, _pk(fs.model)))
            else:
                return self.render(fs=fs, status=0)
        if request.format == 'html':
            return self.render(fs=fs, id=id)
        else:
            return self.render(fs=fs, status=1)

    def delete(self):
        request = self.request
        record = request.model_instance

        event = events.BeforeDeleteEvent(record, self.request)
        zope.component.event.objectEventNotify(event)

        if record:
            self.session.delete(record)
        else:
            raise NotFound()

        if request.format == 'html':
            if request.is_xhr or request.format == 'xhr':
                return Response(content_type='text/plain')
            return exc.HTTPFound(location=request.fa_url(request.model_name))
        return self.render(id=request.model_id)

    def autocomplete(self, *args, **kwargs):
        filter_term = "%s%%" % self.request.params.get('term')
        filter_attr = getattr(self.request.model_class, self.request.params.get('filter_by'))
        query = self.session.query(self.request.model_class.id, filter_attr).filter(filter_attr.ilike(filter_term))
        items = self.request.query_factory(self.request, query)
        return Response(json.dumps([{'label' : x[1],
                                     'value' : x[0]} for x in items ]),
                        content_type='text/plain')

