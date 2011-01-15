# -*- coding: utf-8 -*-

def include(config):
    config.load_zcml('pyramid_formalchemy:configure.zcml')

def configure(config, models=None, forms=None, session_factory=None, package=None):
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

    config.add_route('fa_admin', '/admin/*traverse',
                     factory='pyramid_formalchemy.resources.AdminView')

