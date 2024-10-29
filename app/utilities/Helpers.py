import inspect
from datetime import datetime, timedelta, tzinfo, time
from decimal import Decimal
from json import JSONEncoder, dumps
from http import HTTPStatus

from pydantic import ValidationError

def _encodeutf8(item):
    return item.encode("utf-8")


def _decodeutf8(item):
    return item.decode("utf-8")


def get_status_response(status_code, response_msg, raw=False):
    if raw is True:
        return
    try:
        status_code_description = HTTPStatus(status_code).phrase
    except KeyError:
        status_code_description = "Unknown"

    return (
        f"{status_code} {status_code_description}",
        [("Content-Type", "text/plain")],
        _encodeutf8(f"{response_msg}")
    )


def _badRequestHandler(
    args=None,
    function=None,
    exception=None,
    response_msg=None,
    status=None,
    req_args=None
):
    """Handles bad requests and returns a 400 Bad Request response

    Parameters:
        args (dict): The request arguments
        function (function): The function to inspect
        exception (Exception): The exception to handle
        response_msg (str): The response message
        status (int): The response status code
        req_args (list): The required arguments

    Returns:
        (tuple): A tuple containing the response status, headers, and body
    """
    # if exception is a ValidationError
    if isinstance(exception, ValidationError):
        return get_status_response(400, exception.json())
    # chekc for Mysql OperationalError
    elif exception and isinstance(exception, tuple):
        response_msg = ("Exception Raised: {}").format("".join(exception))
        return get_status_response(500, exception.args[0])
    elif exception and not args:
        response_msg = ("Exception Raised: {}").format("".join(exception.args[0]))
        return get_status_response(400, response_msg)
    elif response_msg and status:
        return get_status_response(status, response_msg)
    elif args and function:
        sig = inspect.signature(function)
        sig_values = sig.parameters.values()
        required_args = [
            param.name for param in sig_values if param.default == inspect._empty
        ]

        missing_params = []
        for param in required_args:
            if param not in args:
                missing_params.append(param)
        if missing_params:
            return get_status_response(
                400, f'Missing required param(s): {", ".join(missing_params)}'
            )
        elif exception:
            return _badRequestHandler(exception=exception)
        else:
            return get_status_response(400, "Exception Raised")
    elif args and req_args:
        missing_params = []
        for param in req_args:
            if param not in args:
                missing_params.append(param)
        if missing_params:
            return get_status_response(
                400, f'Missing required param(s): {", ".join(missing_params)}'
            )
        elif exception:
            return _badRequestHandler(exception=exception)
    else:
        return get_status_response(400, "Exception Raised")


def interval(start, end):
    """start and end are datetime instances"""
    diff = end - start
    ret = diff.days * 24 * 60 * 60 * 1000000
    ret += diff.seconds * 1000000
    ret += diff.microseconds
    return ret


def convert(d):
    diff = d - datetime(1970,1,1,0,0, tzinfo=None)
    ret = diff.days * 24 * 60 * 60
    ret += diff.seconds
    return ret


def converttime(t):
    ret = t.hour * 60 * 60 * 1000000
    ret += t.minute * 60 * 1000000
    ret += t.second * 1000000
    ret += t.microsecond
    return ret


class GMT0(tzinfo):
    def utcoffset(self, dt): return timedelta(hours=0) + self.dst(dt)
    def tzname(self,dt): return "GMT +0"
    def dst(self, dt): return timedelta(0)

gmt0 = GMT0()
epoch = datetime(1970,1,1,0,0, tzinfo=gmt0)


def makedatetime(d): return epoch+timedelta(microseconds=d)


def epochMidnight():
    #this ONLY works for today at present
    midnight = datetime.combine(datetime.today(), time.min)
    epochMidnight = int((midnight - datetime(1970,1,1)).total_seconds())+28800
    print("Utilities.today.epochMidnight:", epochMidnight)
    return epochMidnight


CORSHeaders = [
    ("Access-Control-Allow-Methods", "GET, PUT, POST, DELETE, OPTIONS"),
#   ('Access-Control-Allow-Origin', 'jason.bendhelps.com'),
    ("Access-Control-Allow-Credentials","true"),
    ("Access-Control-Allow-Headers", "access-control-allow-origin,Authorization,Content-Type,Accept,Origin,User-Agent,DNT,Cache-Control,X-Mx-ReqToken,Keep-Alive,X-Requested-With,If-Modified-Since,X-Request")
]


CardinalLookup = [ "th","st","nd","rd","th","th","th","th","th","th" ]


def intToCardinal(n):
    if n % 100 >= 11 and n % 100 <= 13:
        return str(n)+"th"
    return str(n)+CardinalLookup[n % 10]


class DecimalEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            # wanted a simple yield str(o) in the next line,
            # but that would mean a yield on the line with super(...),
            # which wouldn't work (see my comment below), so...
            return float(o)
        return super().default(o)


def formatReturnData(data, raw=True, code=None):

    if raw is True:
        return data
    return [
        "200 OK" if code is None else code,
        [("Content-Type", "application/json")],
        _encodeutf8(dumps(data))
    ]
