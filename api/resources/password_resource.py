from flask_jwt_extended import get_current_user, jwt_required
from flask_restful import Resource

from api.config import dao, app
from api.models.users import User
from api.resources.requests import changePasswordRequest
from api.utils.response_utils import defaultErrorResponse, response, defaultErrorLogMessage


class ChangePasswordResource(Resource):

    # change password
    @jwt_required
    def patch(self):
        request = changePasswordRequest.parse_args()
        old_password = User.hashPassword(request.get('old_password'))
        new_password = User.hashPassword(request.get('new_password'))

        current_user = get_current_user()
        if not current_user.validatePassword(old_password):
            return response('Wrong password', 401)

        current_user.password = new_password
        try:
            dao.update(current_user)
        except Exception:
            app.logger.exception(defaultErrorLogMessage())
            return defaultErrorResponse()
