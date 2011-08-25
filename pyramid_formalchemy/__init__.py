# -*- coding: utf-8 -*-
from pyramid.httpexceptions import HTTPFound
from pyramid_formalchemy.resources import Models

def includeme(config):
    """include formalchemy's zcml"""
    config.add_translation_dirs('formalchemy:i18n_resources/', 'pyramid_formalchemy:locale/')
    config.add_static_view('fa_admin', 'pyramid_formalchemy:static')
    config.add_directive('formalchemy_admin', 'pyramid_formalchemy.formalchemy_admin')
    config.add_directive('formalchemy_model', 'pyramid_formalchemy.formalchemy_model')
    config.add_directive('formalchemy_model_view', 'pyramid_formalchemy.formalchemy_model_view')
    config.registry.pyramid_formalchemy_views = {}

    config.add_route('set_language', '/set_language')
    config.add_view('pyramid_formalchemy.views.set_language', route_name='set_language')
    config.add_route('set_theme', '/set_theme')
    config.add_view('pyramid_formalchemy.views.set_theme', route_name='set_theme')

def formalchemy_model_view(config, route_name,
                           model=None,
                           name='',
                           view='pyramid_formalchemy.views.ModelView',
                           context='pyramid_formalchemy.resources.Model', **kwargs):
    """custom model view registration"""

    model = config.maybe_dotted(model)
    context = config.maybe_dotted(context)
    mixin_name = '%sCustom%s_%s_%s_%s' % (model.__name__, context.__name__,
                                       route_name, name, kwargs.get('request_method','GET'))

    factory = type(mixin_name, (context,), {})
    config.registry.pyramid_formalchemy_views[factory.__name__] = factory

    kw = dict(route_name=route_name, view=view)
    kw.update(kwargs)

    config.add_view(context=factory,
                    name=name,
                    **kw)

def formalchemy_model(config, route_name,
                      factory='pyramid_formalchemy.resources.ModelListing',
                      view='pyramid_formalchemy.views.ModelView', model=None, **kwargs):
    model = config.maybe_dotted(model)
    return formalchemy_admin(config, route_name, factory=factory,
                             view=view, models=[model], model=model, **kwargs)

def formalchemy_admin(config, route_name,
                      factory='pyramid_formalchemy.resources.Models',
                      view='pyramid_formalchemy.views.ModelView',
                      package=None, models=None, forms=None,
                      session_factory=None,
                      query_factory=None, **kwargs):
    """configure formalchemy's admin interface"""

    route_name = route_name.strip('/')

    kw = dict(route_name=route_name, view=view)

    if models:
        models = config.maybe_dotted(models)
    if forms:
        forms = config.maybe_dotted(forms)
    if session_factory:
        session_factory = config.maybe_dotted(session_factory)

    if package:
        if not models:
            models = config.maybe_dotted('%s.models' % package)
        if not forms:
            forms = config.maybe_dotted('%s.forms' % package)
        if not session_factory:
            session_factory = config.maybe_dotted('%s.models.DBSession' % package)

    if not query_factory:
        def query_factory(request, query, id=None):
            if id is not None:
                return query.get(id)
            else:
                return query

    factory_args = {
        '__forms__': forms,
        '__models__': models,
        '__model_class__': kwargs.get('model'),
        '__session_factory__': session_factory,
        '__query_factory__': staticmethod(query_factory),
        '__fa_route_name__': route_name,
        }

    factory = config.maybe_dotted(factory)

    factory = type('%s_%s' % (factory.__name__, route_name), (factory,), factory_args)

    def redirect(request):
        """redirect /route_name to /route_name/"""
        matchdict = request.matchdict.copy()
        url = request.route_url(route_name, traverse=(), **matchdict)
        return HTTPFound(location=url)

    config.add_route('%s_redirect' % route_name, route_name)
    config.add_view(redirect, route_name = '%s_redirect' % route_name)

    config.add_route(route_name, '%s/*traverse' % route_name,
                     factory=factory)

    if issubclass(factory, Models):
        # don't want all models
        config.add_view(context=factory,
                        renderer='pyramid_formalchemy:templates/admin/models.pt',
                        attr='models',
                        request_method='GET',
                        permission='view',
                        **kw)

    config.add_view(context='pyramid_formalchemy.resources.ModelListing',
                    renderer='pyramid_formalchemy:templates/admin/listing.pt',
                    attr='listing',
                    request_method='GET',
                    permission='view',
                    **kw)

    config.add_view(context='pyramid_formalchemy.resources.ModelListing',
                    renderer='pyramid_formalchemy:templates/admin/new.pt',
                    name='new',
                    attr='new',
                    request_method='GET',
                    permission='new',
                    **kw)

    config.add_view(context='pyramid_formalchemy.resources.ModelListing',
                    renderer='pyramid_formalchemy:templates/admin/new.pt',
                    attr='create',
                    request_method='POST',
                    permission='new',
                    **kw)

    config.add_view(context='pyramid_formalchemy.resources.Model',
                    renderer='pyramid_formalchemy:templates/admin/edit.pt',
                    name='edit',
                    attr='edit',
                    request_method='GET',
                    permission='edit',
                    **kw)

    config.add_view(context='pyramid_formalchemy.resources.Model',
                    renderer='pyramid_formalchemy:templates/admin/edit.pt',
                    name='edit',
                    attr='update',
                    request_method='POST',
                    permission='edit',
                    **kw)

    config.add_view(context='pyramid_formalchemy.resources.Model',
                    renderer='json',
                    name='',
                    attr='update',
                    request_method='POST',
                    permission='edit',
                    **kw)

    config.add_view(context='pyramid_formalchemy.resources.Model',
                    renderer='pyramid_formalchemy:templates/admin/edit.pt',
                    name='delete',
                    attr='delete',
                    request_method='POST',
                    permission='delete',
                    **kw)

    config.add_view(context='pyramid_formalchemy.resources.Model',
                    renderer='pyramid_formalchemy:templates/admin/edit.pt',
                    attr='delete',
                    request_method='DELETE',
                    permission='delete',
                    **kw)

    config.add_view(context='pyramid_formalchemy.resources.Model',
                    renderer='pyramid_formalchemy:templates/admin/show.pt',
                    request_method='GET',
                    permission='view',
                    name='',
                    attr='show',
                    **kw)

    config.add_view(context='pyramid_formalchemy.resources.ModelListing',
                    attr='autocomplete',
                    name='autocomplete',
                    request_method='GET',
                    permission='view',
                    **kw)

