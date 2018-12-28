_response_message_attribute = 'msg'
_response_error_message = 'Something went wrong'
_error_log_text = 'Error occurred: '


def response(msg, http_code=200):
    return {_response_message_attribute: msg}, http_code


def tokenResponse(access_token=None, refresh_token=None):
    res = {}
    if access_token:
        res['access_token'] = access_token
    if refresh_token:
        res['refresh_token'] = refresh_token

    return res, 200


def defaultErrorResponse():
    return response(_response_error_message, 500)


def defaultErrorLogMessage():
    return _error_log_text
