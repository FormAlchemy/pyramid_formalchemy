from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from pyramidapp.models import initialize_sql
import pyramid_formalchemy

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    initialize_sql(engine)
    config = Configurator(settings=settings)
    config.add_static_view('static', 'pyramidapp:static')
    config.add_route('home', '/', view='pyramidapp.views.my_view',
                     view_renderer='templates/mytemplate.pt')
    pyramid_formalchemy.include_jquery(config)
    pyramid_formalchemy.configure(config, package='pyramidapp', use_jquery=True)
    return config.make_wsgi_app()


