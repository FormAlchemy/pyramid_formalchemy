from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from pyramidapp.models import initialize_sql
from pyramidapp import events; events #pyflakes

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    initialize_sql(engine)
    config = Configurator(settings=settings)
    config.add_static_view('static', 'pyramidapp:static')
    config.add_route('home', '/', view='pyramidapp.views.my_view',
                     view_renderer='templates/mytemplate.pt')

    # pyramid_formalchemy's configuration
    config.include('pyramid_formalchemy')

    # register an admin UI
    config.formalchemy_admin('admin', package='pyramidapp')

    # register an admin UI for a single model
    config.formalchemy_model('foo', package='pyramidapp', model='pyramidapp.models.Foo')

    # register custom model listing
    config.formalchemy_model_view('admin',
                                  model='pyramidapp.models.Foo',
                                  context='pyramid_formalchemy.resources.ModelListing',
                                  renderer='templates/foolisting.pt',
                                  attr='listing',
                                  request_method='GET',
                                  permission='view')

    # register custom model view
    config.formalchemy_model_view('admin',
                                  model='pyramidapp.models.Foo',
                                  context='pyramid_formalchemy.resources.Model',
                                  name='',
                                  renderer='templates/fooshow.pt',
                                  attr='show',
                                  request_method='GET',
                                  permission='view')

    return config.make_wsgi_app()


