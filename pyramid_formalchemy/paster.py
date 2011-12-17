try: # pyramid 1.0.X
    # "pyramid.paster.paste_script..." doesn't exist past 1.0.X
    from pyramid.paster import paste_script_template_renderer
    from pyramid.paster import PyramidTemplate
except ImportError:
    try:  # pyramid 1.1.X, 1.2.X
        # trying to import "paste_script_template_renderer" fails on 1.3.X
        from pyramid.scaffolds import paste_script_template_renderer
        from pyramid.scaffolds import PyramidTemplate
    except ImportError: # pyramid >=1.3a2
        paste_script_template_renderer = None
        from pyramid.scaffolds import PyramidTemplate


class PyramidFormAlchemyTemplate(PyramidTemplate):
    _template_dir = ('pyramid_formalchemy', 'paster_templates/pyramid_fa')
    summary = "Pyramid application template to extend other templates with "
    "formalchemy"
    template_renderer = staticmethod(paste_script_template_renderer)
