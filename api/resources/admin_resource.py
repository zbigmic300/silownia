from flask_jwt_extended import get_current_user, jwt_required
from flask_restful import Resource
from sqlalchemy import desc

from api.config import dao, app
from api.models.users import User, UserSchema
from api.resources.requests import createUserRequest, modifyUserRequest, filterUserRequest
from api.utils.response_utils import defaultErrorResponse, response, defaultErrorLogMessage

user_schema = UserSchema()
many_user_schema = UserSchema(many=True)


class AdminUserResource(Resource):

    # get user
    @jwt_required
    def get(self, user_id):
        current_user = get_current_user()
        if not current_user.admin:
            return response('Insufficient privileges', 403)

        user = dao.getById(User, user_id)
        if not user:
            return response('Not found user for id %d' % user_id, 404)

        return user_schema.dump(user).data

    # modify user
    @jwt_required
    def put(self, user_id):
        request = modifyUserRequest.parse_args()

        current_user = get_current_user()
        if not current_user.admin:
            return response('Insufficient privileges', 403)

        user = dao.getById(User, user_id)
        if not user:
            return response('Not found user for id %d' % user_id, 404)

        user.admin = request.get('admin')
        user.first_name = request.get('first_name')
        user.last_name = request.get('last_name')
        user.room = request.get('room')

        try:
            dao.update(user)
        except Exception:
            app.logger.exception(defaultErrorLogMessage())
            return defaultErrorResponse()

    # activate user
    @jwt_required
    def patch(self, user_id):
        current_user = get_current_user()
        if not current_user.admin:
            return response('Insufficient privileges', 403)

        user = dao.getById(User, user_id)
        if not user:
            return response('Not found user for id %d' % user_id, 404)

        if user.status == User.ACTIVE:
            return response('User already activated', 400)

        user.status = User.ACTIVE

        try:
            dao.update(user)
        except Exception:
            app.logger.exception(defaultErrorLogMessage())
            return defaultErrorResponse()

    # remove user
    @jwt_required
    def delete(self, user_id):
        current_user = get_current_user()
        if not current_user.admin:
            return response('Insufficient privileges', 403)

        user = dao.getById(User, user_id)
        if not user:
            return response('Not found user for id %d' % user_id, 404)

        # admin account is off limits
        if user.login == 'admin':
            return response('Insufficient privileges', 403)

        if user.removed_date:
            return response('User already removed', 400)

        try:
            dao.remove(user)
        except Exception:
            app.logger.exception(defaultErrorLogMessage())
            return defaultErrorResponse()


class AdminUsersResource(Resource):

    # get users, with filtering, ordering
    @jwt_required
    def get(self):
        request = filterUserRequest.parse_args()

        current_user = get_current_user()
        if not current_user.admin:
            return response('Insufficient privileges', 403)

        user = User()
        user.login = request.get('login')
        user.admin = request.get('admin')
        user.first_name = request.get('first_name')
        user.last_name = request.get('last_name')
        user.room = request.get('room')
        user.status = request.get('status')
        order = request.get('order')
        descending = request.get('descending')

        if order and order not in user.getColumns():
            return response('Wrong ordering', 400)

        if descending and order:
            result = dao.getByObject(user, desc(order))
        else:
            result = dao.getByObject(user, order)

        return many_user_schema.dump(result).data

    # create user
    @jwt_required
    def post(self):
        request = createUserRequest.parse_args()

        current_user = get_current_user()
        if not current_user.admin:
            return response('Insufficient privileges', 403)

        new_user = User()
        new_user.login = request.get('login')
        new_user.password = User.hashPassword(request.get('password'))
        new_user.admin = request.get('admin')
        new_user.first_name = request.get('first_name')
        new_user.last_name = request.get('last_name')
        new_user.room = request.get('room')
        new_user.status = User.ACTIVE

        deduplication = dao.getByUnique(User, 'login', new_user.login)
        if deduplication:
            return response('User with given login already exists', 409)

        try:
            dao.create(new_user)
        except Exception:
            app.logger.exception(defaultErrorLogMessage())
            return defaultErrorResponse()
