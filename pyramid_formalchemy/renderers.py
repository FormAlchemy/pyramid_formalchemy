from formalchemy import fields
from formalchemy import helpers as h
from fa.jquery.renderers import jQueryFieldRenderer, alias


def PyramidAutocompleteFieldRenderer(filter_by='id', renderer=fields.IntegerFieldRenderer, **jq_options):
    """Use http://docs.jquery.com/UI/Autocomplete with pyramid"""

    class Renderer(renderer):

        def __init__(self, *args, **kwargs):
            super(Renderer, self).__init__(*args, **kwargs)
            self.field.render_opts['options'] = []

        def update_options(self, options, kwargs):
            kwargs['source'] = self.request.fa_url(
                    self.field.relation_type().__name__, 'autocomplete')

        def render(self, **kwargs):
            filter_by = self.jq_options.get('filter_by')
            if self.raw_value:
                label = getattr(self.raw_value, filter_by, u'Not selected')
            else:
                label = u''

            html = h.radio_button(self.name, value=self.value, **kwargs)
            html += h.label(label)

            return ''.join(html)

    jq_options.update(filter_by=filter_by, show_input=False)

    return jQueryFieldRenderer('pyramidautocomplete', renderer=Renderer, **jq_options)

@alias(PyramidAutocompleteFieldRenderer)
def pyramid_autocomplete(): pass
