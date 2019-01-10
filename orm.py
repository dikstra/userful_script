
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine,Column,Integer,String

engine = create_engine("mysql://root:!EjhECkhth77@192.168.8.143:3306/zhoujz")
#engine = create_engine(do_engine)

Base = declarative_base()

class Account(Base):
    __tablename__ = 'account'
    id = Column(Integer,primary_key=True)
    user_name = Column(String(50),nullable=False)
    password = Column(String(200),nullable=False)
    salary = Column(Integer)

    def is_active(self):
        return True

    def is_anonymous(self):
        return False
 
    def get_id(self):
        return self.id

    def get_authorized(self):
        return True

    def __repr__(self):
        return "<type 'Account'>{}:{}".format(self.id,self.user_name)

Base.metadata.create_all(engine)
