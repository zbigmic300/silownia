from datetime import timedelta, datetime


def isPastDate(date):
    return date < currentDate()


def isDateBefore(start_date, end_date):
    return start_date > end_date


def currentDate():
    return datetime.utcnow()


def fromTimestamp(t):
    return datetime.utcfromtimestamp(t)


def startOfWeek(date):
    week_start = date.replace(hour=0, minute=0, second=0, microsecond=0)
    week_start = week_start - timedelta(days=week_start.weekday())
    return week_start


def endOfWeek(date):
    week_end = date.replace(hour=0, minute=0, second=0, microsecond=0)
    week_end = week_end + timedelta(days=7 - week_end.weekday())
    week_end = week_end - timedelta(microseconds=1)
    return week_end
