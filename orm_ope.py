from sqlalchemy.orm import scoped_session,sessionmaker
import os
import sys
basedir=os.path.dirname(os.path.abspath(__file__))
print(basedir)
sys.path.append(basedir)
import orm

SessionType = scoped_session(sessionmaker(bind=orm.engine))

def GetSession():
    return SessionType()


from contextlib import contextmanager

@contextmanager
def session_scope():
    session = GetSession()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise
    finally:
        session.close()

from sqlalchemy import or_
def GetAccount(id=None,user_name=None):
    with session_scope() as session:
        res = session.query(orm.Account).filter(or_(orm.Account.id == id,orm.Account.user_name == user_name)).first()
        yield res

def GetAllAccount():
    with session_scope() as session:
        for account in session.query(orm.Account).all():
            yield account

def InsertAccount(user,password,salary):
    with session_scope() as session:
        account = orm.Account(user_name=user,password=password,salary=salary)
        session.add(account)

def DeleteAccount(id):
    with session_scope() as session:
        account = session.query(orm.Account).get(id)
        session.delete(account)
