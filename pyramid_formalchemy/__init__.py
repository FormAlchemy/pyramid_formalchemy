# -*- coding: utf-8 -*-

def include(config):
    """include formalchemy's zcml"""
    config.load_zcml('pyramid.includes:configure.zcml')
    config.load_zcml('pyramid_formalchemy:configure.zcml')
    config.load_zcml('pyramid_formalchemy:view.zcml')

def include_jquery(config):
    """include formalchemy's zcml"""
    config.load_zcml('pyramid.includes:configure.zcml')
    config.load_zcml('pyramid_formalchemy:configure.zcml')
    config.load_zcml('fa.jquery:configure.zcml')

def configure(config, models=None, forms=None, session_factory=None, package=None, use_jquery=True):
    """configure formalchemy's admin interface"""
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

    config.registry.settings.update({
        'fa.models': models,
        'fa.forms': forms,
        'fa.session_factory': session_factory,
        })

    if use_jquery:
        config.add_route('fa_admin', '/admin/*traverse',
                         factory='pyramid_formalchemy.resources.AdminView')
    else:
        config.add_route('fa_admin', '/admin/*traverse',
                         factory='pyramid_formalchemy.resources.AdminView')
