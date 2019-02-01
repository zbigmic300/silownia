from flask_jwt_extended import get_current_user, jwt_required
from flask_restful import Resource

from api.config import dao, app
from api.models.reservations import Reservation
from api.models.schemas import ReservationSchema
from api.resources.requests import reservationRequest, weekReservationRequest
from api.utils.datetime_utils import startOfWeek, currentDate, endOfWeek
from api.utils.reservation_utils import checkDateRelations, checkOverlapping, checkUserBookedInterval
from api.utils.response_utils import defaultErrorResponse, response, defaultErrorLogMessage

reservation_schema = ReservationSchema()
many_reservation_schema = ReservationSchema(many=True)


class ReservationResource(Resource):

    # get reservation
    @jwt_required
    def get(self, reservation_id):
        current_user = get_current_user()

        reservation = dao.getById(Reservation, reservation_id)
        if not reservation or reservation.user_id != current_user.id:
            return response('Not found reservation for id %d' % reservation_id, 404)

        return reservation_schema.dump(reservation).data

    # delete reservation (cancel)
    @jwt_required
    def delete(self, reservation_id):
        current_user = get_current_user()

        reservation = dao.getById(Reservation, reservation_id)
        if not reservation or reservation.user_id != current_user.id:
            return response('Not found reservation for id %d' % reservation_id, 404)

        if currentDate() >= reservation.start_date:
            return response('Cannot cancel past reservations', 404)

        current_user.booked_interval = current_user.booked_interval - (reservation.end_date - reservation.start_date)

        try:
            dao.delete(reservation, False)
            dao.update(current_user)
        except Exception:
            app.logger.exception(defaultErrorLogMessage())
            return defaultErrorResponse()


class ReservationsResource(Resource):

    # get reservations
    @jwt_required
    def get(self):
        user = get_current_user()
        result = many_reservation_schema.dump(user.reservations)
        return result.data

    # create reservation
    @jwt_required
    def post(self):
        request = reservationRequest.parse_args()

        current_user = get_current_user()

        reservation = Reservation()
        reservation.user_id = current_user.id
        reservation.start_date = request.get('start_date')
        reservation.end_date = request.get('end_date')

        # check reservation restrictions
        checkDateRelations(reservation.start_date, reservation.end_date)
        checkOverlapping(reservation.start_date, reservation.end_date)
        checkUserBookedInterval(current_user, reservation.start_date, reservation.end_date)

        # update last reservation date and booked interval
        current_user.last_reservation_date = reservation.start_date
        current_user.booked_interval = current_user.booked_interval + (reservation.end_date - reservation.start_date)

        try:
            dao.create(reservation, False)
            dao.update(current_user)
        except Exception:
            app.logger.exception(defaultErrorLogMessage())
            return defaultErrorResponse()


class WeekReservationsResource(Resource):

    # get reservation for this week
    @jwt_required
    def get(self):
        request = weekReservationRequest.parse_args()
        date = request.get('date')
        if not date:
            date = currentDate()
        week_start = startOfWeek(date)
        week_end = endOfWeek(date)

        result = dao.query(Reservation).filter(
            Reservation.start_date >= week_start, Reservation.end_date <= week_end).all()
        return many_reservation_schema.dump(result).data
