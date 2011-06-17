from tempita import paste_script_template_renderer
from pyramid.paster import PyramidTemplate

class PyramidFormAlchemyTemplate(PyramidTemplate):
    _template_dir = ('pyramid_formalchemy', 'paster_templates/pyramid_fa')
    summary = "Pyramid application template to extend other templates with "
    "formalchemy"
    template_renderer = staticmethod(paste_script_template_renderer)
