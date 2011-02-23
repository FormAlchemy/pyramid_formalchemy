from pyramidapp.models import DBSession
from pyramidapp.models import MyModel
from pyramidapp import forms

def my_view(request):
    dbsession = DBSession()
    root = dbsession.query(MyModel).filter(MyModel.name==u'root').first()
    fs = forms.GridMyModel.bind([root]).render()
    return {'root':root, 'project':'pyramidapp'}
