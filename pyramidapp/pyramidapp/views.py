from pyramidapp.models import DBSession
from pyramidapp.models import MyModel
from pyramidapp import forms

def my_view(request):
    dbsession = DBSession()
    root = dbsession.query(MyModel).filter(MyModel.name==u'root').first()
    fs = forms.GridMyModel.bind(instances=[root]).render()
    fs = forms.GridMyModelReadOnly.bind(instances=[root]).render()
    return {'root':root, 'project':'pyramidapp'}
