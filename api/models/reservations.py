from api.config import db, ma
from api.db_lib.model import Deletable


class Reservation(db.Model, Deletable):
    __tablename__ = 'reservations'

    id = db.Column(db.Integer, db.Sequence('seq_reservations_id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return '<Reservation %i: %s - %s>' % (self.user_id, self.start_date, self.end_date)


class ReservationSchema(ma.ModelSchema):
    class Meta:
        model = Reservation
        sqla_session = db.session
