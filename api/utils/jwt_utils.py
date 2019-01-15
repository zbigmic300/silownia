from datetime import datetime

from api.config import dao
from api.models.revoked_tokens import RevokedToken
from api.models.users import User
from api.utils.datetime_utils import currentDate


def authenticate(login):
    user = dao.getByUnique(User, 'login', login)
    if user and user.isActive():
        return user


def identity(payload):
    login = payload.get('login')
    return login


def isBlacklisted(decrypted_token):
    jti = decrypted_token['jti']
    tokens = dao.get(RevokedToken, jti=jti)
    # jti not found
    if tokens is None or len(tokens) == 0:
        return False
    # found many results
    if len(tokens) > 1:
        # delete expired
        for token in tokens:
            if token.expire_date < currentDate():
                dao.delete(token, False)
            dao.commit()
        return True
    # found 1 result
    # token expired
    if tokens[0].expire_date < currentDate():
        dao.delete(tokens[0])
        return False
    # token still active
    return True


def getUserClaims(payload):
    user = dao.getByUnique(User, 'login', payload.get('login'))
    return 'admin' if user.admin else 'user'
