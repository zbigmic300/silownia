from flask_restful import abort

from api.config import dao, app
from api.models.reservations import Reservation
from api.utils.datetime_utils import isPastDate, isDateBefore, endOfWeek, currentDate


def checkDateRelations(start_date, end_date):
    if isPastDate(start_date):
        abort(400, message='Start Date is a past date')
    if isPastDate(end_date):
        abort(400, message='End Date is a past date')
    if isDateBefore(start_date, end_date):
        abort(400, message='End Date cannot be before start date')

    if end_date - start_date > app.config['MAX_AMOUNT_OF_TIME_AT_GYM_PER_WEEK']:
        abort(400, message='Date range too big')
    week_end = endOfWeek(currentDate())
    if end_date > week_end:
        abort(400, message='Date range cannot spread to many weeks')


def checkOverlapping(start_date, end_date):
    result = dao.query(Reservation).filter(
        ~((end_date <= Reservation.start_date) | (start_date >= Reservation.end_date))).first()
    if result:
        abort(400, message='Overlapping reservation found')


def checkUserBookedInterval(user, start_date, end_date):
    delta = end_date - start_date
    if user.booked_interval + delta > app.config['MAX_AMOUNT_OF_TIME_AT_GYM_PER_WEEK']:
        abort(400, message='User cannot reserve that much')
