# -*- coding: utf-8 -*-

def includeme(config):
    """include formalchemy's zcml"""
    config.add_static_view('fa_admin', 'pyramid_formalchemy:static')
    config.add_directive('formalchemy_admin', 'pyramid_formalchemy.formalchemy_admin')

def formalchemy_admin(config, route_name,
                      factory='pyramid_formalchemy.resources.Models',
                      view='pyramid_formalchemy.views.ModelView',
                      package=None, models=None, forms=None, session_factory=None):
    """configure formalchemy's admin interface"""

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

    factory_args = {
        '__models__': models,
        '__forms__': forms,
        '__session_factory__': session_factory,
        '__fa_route_name__': route_name,
        }

    factory = config.maybe_dotted(factory)

    factory = type('%s_%s' % (factory.__name__, route_name), (factory,), factory_args)

    config.add_route(route_name, '%s/*traverse' % route_name,
                     factory=factory)

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

