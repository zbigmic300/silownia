import hashlib
import api.models.reservations

from api.config import db, ma
from api.db_lib.model import Updateable, Removable


class User(db.Model, Updateable, Removable):
    __tablename__ = 'users'

    id = db.Column(db.Integer, db.Sequence('seq_users_id'), primary_key=True)
    status = db.Column(db.String(1), nullable=False)
    login = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    admin = db.Column(db.Boolean, default=False, nullable=False)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    room = db.Column(db.String(3))
    last_login_date = db.Column(db.DateTime)
    booked_interval = db.Column(db.Interval, default='0', nullable=False)
    last_reservation_date = db.Column(db.DateTime)

    reservations = db.relationship('Reservation', backref='User', lazy=True)

    # user statuses
    WAITING_FOR_ACCEPTANCE = 'W'
    INACTIVE = 'I'
    ACTIVE = 'A'

    def __repr__(self):
        return '<User %s>' % self.login

    @classmethod
    def hashPassword(cls, password):
        return hashlib.sha256(password.encode('utf-8')).hexdigest()

    def validatePassword(self, password_hash):
        return password_hash == self.password

    def isActive(self):
        return self.status == User.ACTIVE and self.removed_date is None


class UserSchema(ma.ModelSchema):
    class Meta:
        model = User
        sqla_session = db.session
