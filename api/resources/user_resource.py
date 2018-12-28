from datetime import datetime, timedelta

from flask_jwt_extended import get_current_user, jwt_required
from flask_restful import Resource

from api.config import dao, app
from api.models.users import User, UserSchema
from api.resources.requests import simpleModifyUserRequest, simpleCreateUserRequest
from api.utils.datetime_utils import startOfWeek, currentDate
from api.utils.response_utils import defaultErrorResponse, response, defaultErrorLogMessage

user_schema = UserSchema()


class UserResource(Resource):

    # get user data
    @jwt_required
    def get(self):
        user = get_current_user()

        now = currentDate()
        week_start = startOfWeek(now)

        # reset booked_interval at start of week
        if user.booked_interval and user.last_reservation_date < week_start:
            user.booked_interval = timedelta()
            try:
                dao.update(user)
            except Exception:
                app.logger.exception(defaultErrorLogMessage())
                return defaultErrorResponse()

        result = user_schema.dump(user)
        return result.data

    # modify user data
    @jwt_required
    def put(self):
        request = simpleModifyUserRequest.parse_args()
        user = get_current_user()
        user.first_name = request.get('first_name')
        user.last_name = request.get('last_name')
        user.room = request.get('room')

        try:
            dao.update(user)
        except Exception:
            app.logger.exception(defaultErrorLogMessage())
            return defaultErrorResponse()

    # create new user application
    def post(self):
        request = simpleCreateUserRequest.parse_args()
        new_user = User()
        new_user.login = request.get('login')
        new_user.password = User.hashPassword(request.get('password'))
        new_user.first_name = request.get('first_name')
        new_user.last_name = request.get('last_name')
        new_user.room = request.get('room')
        new_user.status = User.WAITING_FOR_ACCEPTANCE

        deduplication = dao.getByUnique(User, 'login', new_user.login)
        if deduplication:
            return response('User with given login already exists', 409)

        try:
            dao.create(new_user)
        except Exception:
            app.logger.exception(defaultErrorLogMessage())
            return defaultErrorResponse()
