def response(code, message, data={}):
    return {
        "errorcode": code,
        "message": message,
        "data": data
    }