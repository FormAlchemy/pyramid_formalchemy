from pyramid.config import Configurator
from sqlalchemy import engine_from_config
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.authentication import RemoteUserAuthenticationPolicy
from pyramid_formalchemy.resources import Models
from pyramid.security import Allow, Authenticated, ALL_PERMISSIONS

from pyramidapp.models import initialize_sql

class ModelsWithACL(Models):
    """A factory to override the default security setting"""
    __acl__ = [
            (Allow, 'admin', ALL_PERMISSIONS),
            (Allow, Authenticated, 'view'),
            (Allow, 'editor', 'edit'),
            (Allow, 'manager', ('new', 'edit', 'delete')),
        ]

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    initialize_sql(engine)

    # configure the security stuff
    config = Configurator(settings=settings,
                          authentication_policy=RemoteUserAuthenticationPolicy(),
                          authorization_policy=ACLAuthorizationPolicy())

    config.add_static_view('static', 'pyramidapp:static')
    config.add_route('home', '/', view='pyramidapp.views.my_view',
                     view_renderer='templates/mytemplate.pt')

    # pyramid_formalchemy's configuration
    config.include('pyramid_formalchemy')
    config.formalchemy_admin('admin', package='pyramidapp',
                             factory=ModelsWithACL) # use the secure factory

    return config.make_wsgi_app()


