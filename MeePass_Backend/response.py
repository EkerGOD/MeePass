from enum import Enum

class StatusCode(Enum):
    OK = 200000
    CREATED = 201000

    WRONG = 400000
    WRONG_OTP = 400001



class Response:
    success : bool
    code : StatusCode
    message : str
    data : dict

    def to_dict(self):
        result = {key: getattr(self, key) for key in dir(self)
                  if not key.startswith("__") and not callable(getattr(self, key))}
        return result

class OkResponse(Response):
    success = True
    code = StatusCode.OK.value
    message = 'OK'
    data = {}

class FailResponse(Response):
    success = False
    code = StatusCode.WRONG.value
    message = 'Fail'
    data = {}
