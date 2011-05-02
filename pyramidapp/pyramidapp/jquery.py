# -*- coding: utf-8 -*-
from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from pyramidapp.models import initialize_sql

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
    config.include('fa.jquery')

    # register an admin UI
    config.formalchemy_admin('/admin', package='pyramidapp', view='fa.jquery.pyramid.ModelView')

    # register an admin UI for a single model
    config.formalchemy_model('/foo', package='pyramidapp',
                                    view='fa.jquery.pyramid.ModelView',
                                    model='pyramidapp.models.Foo')

    return config.make_wsgi_app()


