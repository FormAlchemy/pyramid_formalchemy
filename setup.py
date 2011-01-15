import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.txt')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = ['pyramid', 'WebError', 'FormAlchemy']

setup(name='pyramid_formalchemy',
      version='0.0',
      description='pyramid_formalchemy',
      long_description=README + '\n\n' +  CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pylons",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='Gael Pasgrimaud',
      author_email='gael@gawel.org',
      url='',
      keywords='web pyramid pylons formalchemy',
      packages=find_packages(exclude=['pyramidapp']),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      )

