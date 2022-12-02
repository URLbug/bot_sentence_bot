from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, Table
from sqlalchemy.orm import sessionmaker
from sqlalchemy import MetaData

DATABASE_NAME = 'Bot'

engine = create_engine('mysql+pymysql://user:pass@HOST:3306/DB')

Base = declarative_base()
metadata_obj = MetaData()

Session = sessionmaker(bind=engine)

session = Session()

user = Table(
  "user",
  metadata_obj,
  Column("id", Integer, primary_key=True),
  Column("id_user", String(100)),
  Column("language", String(100)),
  Column("count_offers", Integer),
  Column('created', String(100)),
)


class User(Base):

  __tablename__ = 'user'

  id = Column(Integer, primary_key=True)
  id_user = Column(String(100))
  language = Column(String(100))
  count_offers = Column(Integer)
  created = Column(String(100))
  
  def update_count_offers(id_to_update, new_desc):
    try:
        query = session.query(User).filter(User.id_user == id_to_update).\
            update({User.count_offers: new_desc}, synchronize_session=False)
        session.commit()
    except:
        session.rollback()


def creates(what):
  try:
    what.create(engine)
  except:
    return ''


creates(user)
