This script does not want to tell you how your app should be set up.
As such, it does not set an app up for you.

Please use this template together with other templates, like Akhet,
pyramid_routesalchemy or pyramid_alchemy.

You should add pyramid_fanstatic and fa.jquery as dependencies in your
setup.py.

To finally include FormAlchemy, modify your main method were you
create the wsgi application, and include {{package}}.fainit to the
configuration, like that:

    >>> config.include("{{package}}.fainit")

If you are using pyramid_routesalchemy or pyramid_alchemy,
you must modify the models.py. For FormAlchemy to be able to use the
Model, the Model must have a constructer that can be called without
any argument.
So open up models.py and either remove the constructor of MyModel,
or add default values.

If you are using akhet, nothing special needs to be done.

After this modifications, you should find the FormAlchemy Admin
Interface under /admin


