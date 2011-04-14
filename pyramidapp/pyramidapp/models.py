import transaction

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Unicode

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

from zope.sqlalchemy import ZopeTransactionExtension
from pyramid.security import Allow, ALL_PERMISSIONS

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()

class MyModel(Base):
    __tablename__ = 'models'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(255), unique=True)
    value = Column(Integer)

class Foo(Base):
    __tablename__ = 'foo'
    id = Column(Integer, primary_key=True)
    bar = Column(Unicode(255))


class Bar(Base):
    __tablename__ = 'bar'
    __acl__ = [
            (Allow, 'admin', ALL_PERMISSIONS),
            (Allow, 'bar_manager', ALL_PERMISSIONS),
        ]
    id = Column(Integer, primary_key=True)
    foo = Column(Unicode(255))

def populate():
    session = DBSession()
    model = MyModel(name=u'root',value=55)
    session.add(model)
    session.flush()
    for i in range(50):
        model = MyModel(name=u'root%i' % i,value=i)
        session.add(model)
        session.flush()
    transaction.commit()
    
def initialize_sql(engine):
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    Base.metadata.create_all(engine)
    try:
        populate()
    except IntegrityError:
        DBSession.rollback()
