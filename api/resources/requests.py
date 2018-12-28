from datetime import datetime

from flask_restful import reqparse

filterUserRequest = reqparse.RequestParser(bundle_errors=True)
filterUserRequest.add_argument('login', type=str, required=False)
filterUserRequest.add_argument('admin', type=bool, required=False)
filterUserRequest.add_argument('first_name', type=str, required=False)
filterUserRequest.add_argument('last_name', type=str, required=False)
filterUserRequest.add_argument('room', type=str, required=False)
filterUserRequest.add_argument('status', type=str, required=False)
filterUserRequest.add_argument('order', type=str, required=False)
filterUserRequest.add_argument('descending', type=bool, required=False)

createUserRequest = reqparse.RequestParser(bundle_errors=True)
createUserRequest.add_argument('login', type=str, required=True)
createUserRequest.add_argument('password', type=str, required=True)
createUserRequest.add_argument('admin', type=bool, required=False)
createUserRequest.add_argument('first_name', type=str, required=False)
createUserRequest.add_argument('last_name', type=str, required=False)
createUserRequest.add_argument('room', type=str, required=False)

simpleCreateUserRequest = reqparse.RequestParser(bundle_errors=True)
simpleCreateUserRequest.add_argument('login', type=str, required=True)
simpleCreateUserRequest.add_argument('password', type=str, required=True)
simpleCreateUserRequest.add_argument('first_name', type=str, required=False)
simpleCreateUserRequest.add_argument('last_name', type=str, required=False)
simpleCreateUserRequest.add_argument('room', type=str, required=False)

modifyUserRequest = reqparse.RequestParser(bundle_errors=True)
modifyUserRequest.add_argument('admin', type=bool, required=False)
modifyUserRequest.add_argument('first_name', type=str, required=False)
modifyUserRequest.add_argument('last_name', type=str, required=False)
modifyUserRequest.add_argument('room', type=str, required=False)

simpleModifyUserRequest = reqparse.RequestParser(bundle_errors=True)
simpleModifyUserRequest.add_argument('first_name', type=str, required=False)
simpleModifyUserRequest.add_argument('last_name', type=str, required=False)
simpleModifyUserRequest.add_argument('room', type=str, required=False)

changePasswordRequest = reqparse.RequestParser(bundle_errors=True)
changePasswordRequest.add_argument('old_password', type=str, required=True)
changePasswordRequest.add_argument('new_password', type=str, required=True)

loginRequest = reqparse.RequestParser(bundle_errors=True)
loginRequest.add_argument('login', type=str, required=True)
loginRequest.add_argument('password', type=str, required=True)

logoutRequest = reqparse.RequestParser(bundle_errors=True)
logoutRequest.add_argument('refresh_token', type=str, required=True)

reservationRequest = reqparse.RequestParser(bundle_errors=True)
reservationRequest.add_argument('start_date', type=lambda x: datetime.strptime(x, '%Y-%m-%dT%H:%M:%S'), required=True)
reservationRequest.add_argument('end_date', type=lambda x: datetime.strptime(x, '%Y-%m-%dT%H:%M:%S'), required=True)
