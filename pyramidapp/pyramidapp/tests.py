import unittest2 as unittest
from pyramid.config import Configurator
from pyramid import testing
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

from zope.sqlalchemy import ZopeTransactionExtension

import os
import shutil
import tempfile
from webtest import TestApp
from pyramidapp import main
from pyramidapp import models
from paste.deploy import loadapp

dirname = os.path.abspath(__file__)
dirname = os.path.dirname(dirname)
dirname = os.path.dirname(dirname)

class Test_1_UI(unittest.TestCase):

    config = os.path.join(dirname, 'test.ini')
    extra_environ = {}

    def setUp(self):
        app = loadapp('config:%s' % self.config, global_conf={'db':'sqlite://'})
        self.app = TestApp(app, extra_environ=self.extra_environ)
        self.config = Configurator(autocommit=True)
        self.config.begin()

    def test_index(self):
        resp = self.app.get('/')

    def test_1_crud(self):
        # index
        resp = self.app.get('/admin')
        self.assertEqual(resp.status_int, 302)
        assert '/admin/' in resp.location, resp

        resp = self.app.get('/admin/')
        resp.mustcontain('/admin/Foo')
        resp = resp.click('Foo')

        ## Simple model

        # add page
        resp.mustcontain('/admin/Foo/new')
        resp = resp.click(linkid='new')
        resp.mustcontain('/admin/Foo"')
        form = resp.forms[0]
        form['Foo--bar'] = 'value'
        resp = form.submit()
        assert resp.headers['location'] == 'http://localhost/admin/Foo', resp

        # model index
        resp = resp.follow()
        resp.mustcontain('<td>value</td>')
        form = resp.forms[0]
        resp = form.submit()

        # edit page
        form = resp.forms[0]
        form['Foo-1-bar'] = 'new value'
        #form['_method'] = 'PUT'
        resp = form.submit()
        resp = resp.follow()

        # model index
        resp.mustcontain('<td>new value</td>')

        # delete
        resp = self.app.get('/admin/Foo')
        resp.mustcontain('<td>new value</td>')
        resp = resp.forms[1].submit()
        resp = resp.follow()

        assert 'new value' not in resp, resp

    def test_2_model(self):
        # index
        resp = self.app.get('/foo')
        self.assertEqual(resp.status_int, 302)
        assert '/' in resp.location, resp

        ## Simple model
        resp = self.app.get('/foo/')

        # add page
        resp.mustcontain('/foo/new')
        resp = resp.click(linkid='new')
        resp.mustcontain('/foo')
        form = resp.forms[0]
        form['Foo--bar'] = 'value'
        resp = form.submit()
        assert resp.headers['location'] == 'http://localhost/foo/', resp

        # model index
        resp = resp.follow()
        resp.mustcontain('<td>value</td>')
        form = resp.forms[0]
        resp = form.submit()

        # edit page
        form = resp.forms[0]
        form['Foo-1-bar'] = 'new value'
        #form['_method'] = 'PUT'
        resp = form.submit()
        resp = resp.follow()

        # model index
        resp.mustcontain('<td>new value</td>')

        # delete
        resp = self.app.get('/foo/')
        resp.mustcontain('<td>new value</td>')
        resp = resp.forms[1].submit()
        resp = resp.follow()

        assert 'new value' not in resp, resp



    def test_3_json(self):
        # index
        response = self.app.get('/admin/json')
        response.mustcontain('{"models": {', '"Foo": "http://localhost/admin/Foo/json"')

        ## Simple model

        # add page
        response = self.app.post('/admin/Foo/json',
                                    {'bar': 'value'})

        data = response.json
        id = data['absolute_url'].split('/')[-1]

        response.mustcontain('"bar": "value"')


        # get data
        response = self.app.get(str(data['absolute_url']))
        response.mustcontain('"bar": "value"')

        # edit page
        response = self.app.post(str(data['absolute_url']), {'bar': 'new value'})
        response.mustcontain('"bar": "new value"')

        # delete
        response = self.app.delete(str(data['absolute_url']))
        self.assert_(response.json['id'] > 0)

    def test_4_json_prefix(self):
        # index
        response = self.app.get('/admin/json')
        response.mustcontain('{"models": {', '"Foo": "http://localhost/admin/Foo/json"')

        ## Simple model

        # add page
        response = self.app.post('/admin/Foo/json?with_prefix=True',
                                 {'Foo--bar': 'value', 'with_prefix': 'true'})

        data = response.json
        id = data['absolute_url'].split('/')[-1]

        response.mustcontain('"Foo-%s-bar": "value"' % id)


        # get data
        response = self.app.get(str(data['absolute_url'])+'?with_prefix=True')
        response.mustcontain('"Foo-%s-bar": "value"' % id)

        # edit page
        response = self.app.post(str(data['absolute_url']+'?with_prefix=True'), {'Foo-%s-bar' % id: 'new value', 'with_prefix': 'true'})
        response.mustcontain('"Foo-%s-bar": "new value"' % id)

        # delete
        response = self.app.delete(str(data['absolute_url']+'?with_prefix=True'))
        self.assert_(response.json['id'] > 0)

    def test_5_xhr(self):
        # add page
        resp = self.app.post('/admin/Foo/', {'Foo--bar':'value'}, extra_environ={'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'})
        self.assertEqual(resp.content_type, 'text/plain')

        resp = self.app.post('/admin/Foo/1', {'Foo-1-bar':'value'}, extra_environ={'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'})
        self.assertEqual(resp.content_type, 'text/plain')

        # assume all are deleted
        response = self.app.delete('/admin/Foo/1', extra_environ={'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'})
        self.assertEqual(resp.content_type, 'text/plain')


class Test_2_Security(Test_1_UI):

    config = os.path.join(dirname, 'security.ini')
    extra_environ = {'REMOTE_USER': 'admin'}

    def test_model_security(self):
        resp = self.app.get('/admin/', extra_environ={'REMOTE_USER': 'editor'})
        self.assertEqual(resp.status_int, 200)

        resp = self.app.get('/admin/Foo', extra_environ={'REMOTE_USER': 'editor'})
        self.assertEqual(resp.status_int, 200)

        resp = self.app.get('/admin/Foo/new', status=403, extra_environ={'REMOTE_USER': 'editor'})
        self.assertEqual(resp.status_int, 403)

        resp = self.app.get('/admin/Bar', status=403, extra_environ={'REMOTE_USER': 'editor'})
        self.assertEqual(resp.status_int, 403)

        resp = self.app.get('/admin/Bar', extra_environ={'REMOTE_USER': 'bar_manager'})
        self.assertEqual(resp.status_int, 200)

        resp = self.app.post('/admin/Bar', {'Bar--foo':'bar'}, extra_environ={'REMOTE_USER': 'bar_manager'})
        resp = self.app.get('/admin/Bar/1/edit', extra_environ={'REMOTE_USER': 'admin'})
        self.assertEqual(resp.status_int, 200)
        resp.mustcontain('Delete')
        resp = self.app.get('/admin/Bar/1/edit', extra_environ={'REMOTE_USER': 'bar_manager'})
        self.assertEqual(resp.status_int, 200)
        assert 'Delete' not in resp.body, resp.body

    def test_2_model(self):
        pass



class Test_3_JQuery(Test_1_UI):

    config = os.path.join(dirname, 'jquery.ini')

    def test_1_crud(self):
        # index
        resp = self.app.get('/admin/')
        resp.mustcontain('/admin/Foo')
        resp = resp.click('Foo')

        ## Simple model

        # add page
        resp.mustcontain('/admin/Foo/new')
        resp = resp.click(linkid='new')
        resp.mustcontain('/admin/Foo"')
        form = resp.forms[0]
        form['Foo--bar'] = 'value'
        resp = form.submit()
        assert resp.headers['location'] == 'http://localhost/admin/Foo', resp

        # model index
        resp = resp.follow()

        # edit page
        resp = self.app.get('/admin/Foo/1/edit')
        form = resp.forms[0]
        form['Foo-1-bar'] = 'new value'
        #form['_method'] = 'PUT'
        resp = form.submit()
        resp = resp.follow()

        # model index
        resp.mustcontain('<td>new value</td>')

        # delete
        resp = self.app.get('/admin/Foo')
        resp.mustcontain('jQuery')

    def test_2_model(self):
        pass
