import sqlalchemy
from sqlalchemy.sql.expression import text
from sqlalchemy import interfaces
import os
import sys
basedir=os.path.dirname(os.path.abspath(__file__))
print(basedir)
sys.path.append(basedir)
import sql_query

FLUSH = text("FLUSH PRIVILEGES;")
ENGINE = None

class LocalSqlClient(object):
    """A sqlalchemy wrapper to manage transactions."""

    def __init__(self, engine, use_flush=True):
        self.engine = engine
        self.use_flush = use_flush

    def __enter__(self):
        self.conn = self.engine.connect()
        self.trans = self.conn.begin()
        return self.conn

    def __exit__(self, type, value, traceback):
        if self.trans:
            if type is not None:  # An error occurred
                self.trans.rollback()
            else:
                if self.use_flush:
                    self.conn.execute(FLUSH)
                self.trans.commit()
        self.conn.close()

    def execute(self, t, **kwargs):
        try:
            return self.conn.execute(t, kwargs)
        except Exception:
            self.trans.rollback()
            self.trans = None
            raise


def get_engine(username, password, ipaddress, database):
    """Create the default engine with the updated admin user."""
    #TODO(rnirmal):Based on permissions issues being resolved we may revert
    #url = URL(drivername='mysql', host='localhost',
    #          query={'read_default_file': '/etc/mysql/my.cnf'})
    global ENGINE
    if ENGINE:
        return ENGINE
    if database:
        ENGINE = sqlalchemy.create_engine("mysql://%s:%s@%s:3306/%s" %
                                      (username, password, ipaddress,database),
                                      pool_recycle=7200,
                                      listeners=[KeepAliveConnection()])
    else:
        ENGINE = sqlalchemy.create_engine("mysql://%s:%s@%s:3306" %
                                      (username, password, ipaddress),
                                      pool_recycle=7200,
                                      listeners=[KeepAliveConnection()])
    return ENGINE

class KeepAliveConnection(interfaces.PoolListener):
    """
    A connection pool listener that ensures live connections are returned
    from the connection pool at checkout. This alleviates the problem of
    MySQL connections timing out.
    """

    def checkout(self, dbapi_con, con_record, con_proxy):
        """Event triggered when a connection is checked out from the pool."""
        try:
            try:
                dbapi_con.ping(False)
            except TypeError:
                dbapi_con.ping()
        except dbapi_con.OperationalError as ex:
            if ex.args[0] in (2006, 2013, 2014, 2045, 2055):
                raise ex.DisconnectionError()
            else:
                raise

if __name__ =="__main__":
    username="root"
    password="!EjhECkhth77"
    ip="192.168.8.143"
    mydb="zhoujz"
    character_set="UTF8"
    collate="utf8_general_ci"
    with LocalSqlClient(get_engine(username,password,ip)) as client:
        #q = "create database zhoujz"
        cd=sql_query.CreateDatabase(mydb,character_set,collate)
        #cd=sql_query.DropDatabase(mydb)
        t = text(str(cd))
        #client.execute(text(str(q)))
