from flask_jwt_extended import jwt_required, jwt_refresh_token_required, create_access_token, get_raw_jwt, decode_token, \
    get_current_user, create_refresh_token
from flask_restful import Resource

from api.config import dao, app
from api.models.revoked_tokens import RevokedToken
from api.models.users import User
from api.resources.requests import logoutRequest, loginRequest
from api.utils.datetime_utils import currentDate, fromTimestamp
from api.utils.response_utils import tokenResponse, defaultErrorResponse, response, defaultErrorLogMessage


class LoginResource(Resource):

    # login
    def post(self):
        request = loginRequest.parse_args()
        login = request.get('login')
        password = User.hashPassword(request.get('password'))

        user = dao.getByUnique(User, 'login', login)
        if user is None or not user.validatePassword(password):
            return response('Wrong login/password', 401)

        now = currentDate()
        if not user.isActive():
            return response('Your account is inactive', 401)
        if user.last_login_date and now - user.last_login_date > app.config['MAX_INACTIVITY_TIME']:
            user.status = User.INACTIVE
            dao.update(user)
            return response('Your account is inactive', 401)

        user.last_login_date = currentDate()

        try:
            dao.update(user)
            return tokenResponse(create_access_token(request), create_refresh_token(request))
        except Exception:
            app.logger.exception('Error occurred:')
            return defaultErrorResponse()


class LogoutResource(Resource):

    # logout
    @jwt_required
    def post(self):
        request = logoutRequest.parse_args()
        raw_access_token = get_raw_jwt()
        access_jti = raw_access_token['jti']
        access_exp = fromTimestamp(raw_access_token['exp'])
        raw_refresh_token = decode_token(request.get('refresh_token'))
        refresh_jti = raw_refresh_token['jti']
        refresh_exp = fromTimestamp(raw_refresh_token['exp'])

        access_revoke = RevokedToken(jti=access_jti, expire_date=access_exp)
        refresh_revoke = RevokedToken(jti=refresh_jti, expire_date=refresh_exp)

        try:
            dao.create(access_revoke, False)
            dao.create(refresh_revoke, False)
            dao.commit()
            return response('Token has been successfully revoked')
        except Exception:
            app.logger.exception(defaultErrorLogMessage())
            return defaultErrorResponse()


class RefreshResource(Resource):

    # refresh access_token
    @jwt_refresh_token_required
    def post(self):
        current_user = get_current_user()
        return tokenResponse(create_access_token(current_user))
