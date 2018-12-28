from api.config import api, app, jwt
from api.resources.access_resource import LoginResource, LogoutResource, RefreshResource
from api.resources.admin_resource import AdminUsersResource, AdminUserResource
from api.resources.password_resource import ChangePasswordResource
from api.resources.reservation_resource import ReservationResource, ReservationsResource, WeekReservationsResource
from api.resources.user_resource import UserResource
from api.utils.jwt_utils import identity, authenticate, isBlacklisted

jwt.user_identity_loader(identity)
jwt.user_loader_callback_loader(authenticate)
jwt.token_in_blacklist_loader(isBlacklisted)

api.add_resource(LoginResource, '/login')
api.add_resource(LogoutResource, '/logout')
api.add_resource(RefreshResource, '/refresh')

api.add_resource(ChangePasswordResource, '/changePassword')

api.add_resource(UserResource, '/user')

api.add_resource(AdminUsersResource, '/admin/users')
api.add_resource(AdminUserResource, '/admin/user/<int:user_id>')

api.add_resource(ReservationResource, '/reservation/<int:reservation_id>')
api.add_resource(ReservationsResource, '/reservations')
api.add_resource(WeekReservationsResource, '/week/reservations')

if __name__ == '__main__':
    app.run(port='5002', debug=True)
