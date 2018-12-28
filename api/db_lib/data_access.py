from abc import ABC, abstractmethod
from datetime import datetime

from .model import Entity, Creatable, Updateable, Removable, Deletable


class DAOError(Exception):
    pass


def _checkIdentitySet(idnSet):
    while len(idnSet) > 0:
        item = idnSet.pop()
        if (not isinstance(item, Entity)
                or item.modified is False):
            raise DAOError('Unmanaged object change in session')
        item.modified = False


def _checkClass(entity):
    if not issubclass(entity, Entity):
        raise TypeError('Expected Entity class')


def _checkObject(obj):
    if not isinstance(obj, Entity):
        raise TypeError('Expected Entity object')


def _checkIfExists(obj):
    if obj.id is None or obj.created_date is None:
        return False
    return True


class UniversalDAO:

    def __init__(self, alchemyDB, date_func=None):
        self.db = alchemyDB
        if date_func:
            self._date_func = date_func
        else:
            self._date_func = datetime.utcnow

    def _checkInstances(self):
        _checkIdentitySet(self.db.session.dirty)
        _checkIdentitySet(self.db.session.new)
        _checkIdentitySet(self.db.session.deleted)

    def create(self, obj, commit=True):
        if isinstance(obj, Creatable):
            if _checkIfExists(obj):
                raise DAOError('Object already exists')
            obj.created_date = self._date_func()
            obj.modified = True
            self.db.session.add(obj)
            if commit:
                self.commit()
        else:
            raise TypeError("Expected Creatable object")

    def update(self, obj, commit=True):
        if isinstance(obj, Updateable):
            if not _checkIfExists(obj):
                raise DAOError('Object does not exists')
            obj.updated_date = self._date_func()
            obj.modified = True
            result = self.db.session.merge(obj)
            if commit:
                self.commit()
            return result
        else:
            raise TypeError("Expected Updateable object")

    def remove(self, obj, commit=True):
        if isinstance(obj, Removable):
            if not _checkIfExists(obj):
                raise DAOError('Object does not exists')
            if obj.removed_date is not None:
                raise DAOError('Object already removed')
            obj.removed_date = self._date_func()
            obj.modified = True
            self.db.session.merge(obj)
            if commit:
                self.commit()
        else:
            raise TypeError("Expected Removable object")

    def delete(self, obj, commit=True):
        if isinstance(obj, Deletable):
            if not _checkIfExists(obj):
                raise DAOError('Object does not exists')
            obj.modified = True
            self.db.session.delete(obj)
            if commit:
                self.commit()
        else:
            raise TypeError("Expected Deletable object")

    def commit(self):
        self._checkInstances()
        self.db.session.commit()

    def rollback(self):
        self.db.session.rollback()

    def getById(self, entity, itemId):
        _checkClass(entity)
        return self.db.session.query(entity).filter(entity.id == itemId).first()

    def getByUnique(self, entity, unique, value):
        _checkClass(entity)
        if unique not in entity().getUniqueColumns():
            raise DAOError('Field is not unique')
        return self.db.session.query(entity).filter_by(**{unique: value}).one_or_none()

    def getAll(self, entity, *order):
        _checkClass(entity)
        if issubclass(entity, Removable):
            return self.db.session.query(entity).filter(entity.removed_date == None).order_by(*order).all()
        else:
            return self.db.session.query(entity).order_by(*order).all()

    def get(self, entity, *order, **kwargs):
        _checkClass(entity)
        return self.db.session.query(entity).filter_by(**kwargs).order_by(*order).all()

    def getByObject(self, obj, *order):
        _checkObject(obj)
        fields = {}
        for f in obj.getColumns():
            v = getattr(obj, f)
            if v is not None:
                fields[f] = v
        return self.get(obj.__class__, *order, **fields)

    def query(self, entity):
        _checkClass(entity)
        return self.db.session.query(entity)

    def session(self):
        return self.db.session


class AbstractDAO(ABC):

    def __init__(self, universal):
        if not isinstance(universal, UniversalDAO):
            raise TypeError('Expected UniversalDAO object')
        self.dao = universal

    @abstractmethod
    def _getEntityAbstract(self):
        pass

    def _getEntity(self):
        entity = self._getEntityAbstract()
        if not issubclass(entity, Entity):
            raise TypeError('Expected Entity class')
        return entity

    def _checkObject(self, obj):
        if not isinstance(obj, self._getEntity()):
            raise TypeError('Expected %s object' % self._getEntity().__name__)

    def create(self, obj, commit=True):
        self._checkObject(obj)
        self.dao.create(obj, commit)

    def update(self, obj, commit=True):
        self._checkObject(obj)
        return self.dao.update(obj, commit)

    def remove(self, obj, commit=True):
        self._checkObject(obj)
        self.dao.remove(obj, commit)

    def delete(self, obj, commit=True):
        self._checkObject(obj)
        self.dao.delete(obj, commit)

    def commit(self):
        self.dao.commit()

    def rollback(self):
        self.dao.rollback()

    def getById(self, itemId):
        return self.dao.getById(self._getEntity(), itemId)

    def getByUnique(self, unique, value):
        return self.dao.getByUnique(self._getEntity(), unique, value)

    def getAll(self, order):
        return self.dao.getAll(self._getEntity(), *order)

    def get(self, *order, **kwargs):
        return self.dao.get(self._getEntity(), *order, **kwargs)

    def getByObject(self, obj, *order):
        self._checkObject(obj)
        return self.dao.getByObject(obj, *order)

    def query(self):
        return self.dao.query(self._getEntity())

    def session(self):
        return self.dao.session()
