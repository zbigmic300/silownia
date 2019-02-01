from api.config import db, ma
from api.models.reservations import Reservation
from api.models.revoked_tokens import RevokedToken
from api.models.users import User


class UserSchema(ma.ModelSchema):
    class Meta:
        model = User
        sqla_session = db.session


class RevokedTokenSchema(ma.ModelSchema):
    class Meta:
        model = RevokedToken
        sqla_session = db.session


class ReservationSchema(ma.ModelSchema):
    class Meta:
        model = Reservation
        sqla_session = db.session

    user = ma.Nested(UserSchema, only=['login', 'first_name', 'last_name', 'room'])
    start_date = ma.DateTime(format='%Y-%m-%dT%H:%M:%S')
    end_date = ma.DateTime(format='%Y-%m-%dT%H:%M:%S')
