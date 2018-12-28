from sqlalchemy import Column, DateTime, Sequence, Integer
from sqlalchemy.ext.declarative import declared_attr, declarative_base
# http://derrickgilland.com/posts/demystifying-flask-sqlalchemy/

base = declarative_base()


class Entity(base):
    __abstract__ = True
    modified = False

    @declared_attr
    def id(self):
        return Column(Integer, Sequence('seq_' + self.__tablename__.lower()), primary_key=True)

    def getColumns(self):
        names = []
        for col in self.__table__.columns:
            names.append(col.name)
        return names

    def getUniqueColumns(self):
        names = []
        for col in self.__table__.columns:
            if col.unique:
                names.append(col.name)
        return names


class Creatable(Entity):
    __abstract__ = True
    created_date = Column(DateTime, nullable=False)


class Updateable(Creatable):
    __abstract__ = True
    updated_date = Column(DateTime)


class Removable(Creatable):
    __abstract__ = True
    removed_date = Column(DateTime)


class Deletable(Creatable):
    __abstract__ = True
