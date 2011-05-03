# -*- coding: utf-8 -*-
from webhelpers.paginate import Page
from sqlalchemy.orm import class_mapper
from formalchemy.fields import _pk
from formalchemy.fields import _stringify
from formalchemy.i18n import get_translator
from formalchemy.fields import Field
from formalchemy import fatypes
from pyramid.renderers import get_renderer
from pyramid.response import Response
from pyramid import httpexceptions as exc
from pyramid.exceptions import NotFound
from pyramid_formalchemy.utils import TemplateEngine
import logging

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

class ModelView(object):
    """A RESTful view bound to a model"""

    engine = TemplateEngine()
    pager_args = dict(link_attr={'class': 'ui-pager-link ui-state-default ui-corner-all'},
                      curpage_attr={'class': 'ui-pager-curpage ui-state-highlight ui-corner-all'})

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.session = request.session_factory

        self.fieldset_class = request.forms.FieldSet
        self.grid_class = request.forms.Grid

    def models(self, **kwargs):
        """Models index page"""
        request = self.request
        models = {}
        if isinstance(request.models, list):
            for model in request.models:
                key = model.__name__
                models[key] = request.fa_url(key, request.format)
        else:
            for key, obj in request.models.__dict__.iteritems():
                if not key.startswith('_'):
                    if Document is not None:
                        try:
                            if issubclass(obj, Document):
                                models[key] = request.fa_url(key, request.format)
                                continue
                        except:
                            pass
                    try:
                        class_mapper(obj)
                    except:
                        continue
                    if not isinstance(obj, type):
                        continue
                    models[key] = request.fa_url(key, request.format)
        if kwargs.get('json'):
            return models
        return self.render(models=models)

    def sync(self, fs, id=None):
        """sync a record. If ``id`` is None add a new record else save current one."""
        if id:
            self.session.merge(fs.model)
        else:
            self.session.add(fs.model)

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
        kwargs.update(
                      main = get_renderer('pyramid_formalchemy:templates/admin/master.pt').implementation(),
                      model_name=request.model_name,
                      breadcrumb=self.breadcrumb(**kwargs),
                      F_=get_translator().gettext)
        return kwargs

    def render_grid(self, **kwargs):
        """render the grid as html or json"""
        return self.render(is_grid=True, **kwargs)

    def render_json_format(self, fs=None, **kwargs):
        request = self.request
        request.override_renderer = 'json'
        if fs:
            try:
                fields = fs.jsonify()
            except AttributeError:
                fields = dict([(field.renderer.name, field.model_value) for field in fs.render_fields.values()])
            data = dict(fields=fields)
            pk = _pk(fs.model)
            if pk:
                data['item_url'] = request.fa_url(request.model_name, 'json', pk)
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
        fs.engine = fs.engine or self.engine
        return id and fs.bind(model) or fs

    def get_grid(self):
        """return a Grid object"""
        request = self.request
        model_name = request.model_name
        if hasattr(request.forms, '%sGrid' % model_name):
            g = getattr(request.forms, '%sGrid' % model_name)
            g.engine = g.engine or self.engine
            g.readonly = True
            self.update_grid(g)
            return g
        model = self.context.get_model()
        grid = self.grid_class(model)
        grid.engine = self.engine
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
                            label=get_translator().gettext('edit'))
            def delete_link():
                return lambda item: '''
                <form action="%(url)s" method="POST" class="ui-grid-icon ui-state-error ui-corner-all">
                <input type="submit" class="ui-icon ui-icon-circle-close" title="%(label)s" value="%(label)s" />
                </form>
                ''' % dict(url=self.request.fa_url(self.request.model_name, _pk(item), 'delete'),
                           label=get_translator().gettext('delete'))
            grid.append(Field('edit', fatypes.String, edit_link()))
            grid.append(Field('delete', fatypes.String, delete_link()))
            grid.readonly = True

    def listing(self, **kwargs):
        """listing page"""
        page = self.get_page(**kwargs)
        fs = self.get_grid()
        fs = fs.bind(instances=page)
        fs.readonly = True
        if self.request.format == 'json':
            values = []
            request = self.request
            for item in page:
                pk = _pk(item)
                fs._set_active(item)
                value = dict(id=pk,
                             item_url=request.fa_url(request.model_name, pk))
                if 'jqgrid' in request.GET:
                    fields = [_stringify(field.render_readonly()) for field in fs.render_fields.values()]
                    value['cell'] = [pk] + fields
                else:
                    value.update(dict([(field.key, field.model_value) for field in fs.render_fields.values()]))
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

    def create(self):
        request = self.request
        fs = self.get_fieldset(suffix='Add')

        if request.format == 'json' and request.method == 'PUT':
            data = json.load(request.body_file)
        else:
            data = request.POST

        try:
            fs = fs.bind(data=data, session=self.session)
        except Exception, e:
            # non SA forms
            fs = fs.bind(self.context.get_model(), data=data, session=self.session)
        if fs.validate():
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
        return self.render(fs=fs, action='new', id=None)

    def show(self):
        id = self.request.model_id
        fs = self.get_fieldset(suffix='View', id=id)
        fs.readonly = True
        return self.render(fs=fs, action='show', id=id)

    def new(self, **kwargs):
        fs = self.get_fieldset(suffix='Add')
        fs = fs.bind(session=self.session)
        return self.render(fs=fs, action='new', id=None)

    def edit(self, id=None, **kwargs):
        id = self.request.model_id
        fs = self.get_fieldset(suffix='Edit', id=id)
        return self.render(fs=fs, action='edit', id=id)

    def update(self, **kwargs):
        request = self.request
        id = request.model_id
        fs = self.get_fieldset(suffix='Edit', id=id)
        fs = fs.bind(data=request.POST)
        if fs.validate():
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
            return self.render(fs=fs, action='edit', id=id)
        else:
            return self.render(fs=fs, status=1)

    def delete(self, **kwargs):
        request = self.request
        record = request.model_instance
        if record:
            self.session.delete(record)
        else:
            raise NotFound()
        if request.format == 'html':
            if request.is_xhr or request.format == 'xhr':
                return Response(content_type='text/plain')
            return exc.HTTPFound(location=request.fa_url(request.model_name))
        return self.render(id=request.model_id)

