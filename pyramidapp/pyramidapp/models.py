import transaction

from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Unicode
from sqlalchemy import ForeignKey

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import relation
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

from zope.sqlalchemy import ZopeTransactionExtension
from pyramid.security import Allow, Authenticated, ALL_PERMISSIONS

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()

class MyModel(Base):
    __tablename__ = 'models'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(255), unique=True)
    value = Column(Integer)

class Foo(Base):
    __tablename__ = 'foo'
    __acl__ = [
            (Allow, 'admin', ALL_PERMISSIONS),
            (Allow, Authenticated, 'view'),
            (Allow, 'editor', 'edit'),
            (Allow, 'manager', ('new', 'edit', 'delete')),
        ]
    id = Column(Integer, primary_key=True)
    bar = Column(Unicode(255))


class Bar(Base):
    __tablename__ = 'bar'
    __acl__ = [
            (Allow, 'admin', ALL_PERMISSIONS),
            (Allow, 'bar_manager', ('view', 'new', 'edit')),
        ]
    id = Column(Integer, primary_key=True)
    foo = Column(Unicode(255))

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode)
    group_id = Column(Integer, ForeignKey('groups.id'))
    group = relation("Group", backref='users')

    def __unicode__(self):
        return self.name

group_permissions = Table('group_permissions', Base.metadata,
        Column('permission_id', Integer, ForeignKey('permissions.id')),
        Column('group_id', Integer, ForeignKey('groups.id')),
    )

class Group(Base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode)
    permissions = relation("Permission", secondary=group_permissions, backref="groups")

    def __unicode__(self):
        return self.name

class Permission(Base):
    __tablename__ = 'permissions'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode)

    def __unicode__(self):
        return self.name

def populate():
    session = DBSession()
    model = MyModel(name=u'root',value=55)
    session.add(model)
    session.flush()
    for i in range(50):
        model = MyModel(name=u'root%i' % i,value=i)
        session.add(model)
        session.flush()
    g = Group()
    g.id = 1
    g.name = 'group1'
    transaction.commit()

def initialize_sql(engine):
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    Base.metadata.create_all(engine)
    try:
        populate()
    except IntegrityError:
        DBSession.rollback()
