# -*- coding: utf-8 -*-

from functools import wraps
from typing import Any, Callable, Tuple

try:
    from http import HTTPStatus

except ImportError:
    from core_https.utils import HTTPStatus

from core_https import StatusInfo
from core_https.exceptions import AuthorizationException
from core_https.exceptions import InternalServerError
from core_https.exceptions import ServiceException


def wrapp_response(fnc: Callable[..., Tuple[HTTPStatus, Any]]):
    """
    This decorator provides a generic mechanism to return the response payload
    for the endpoints in the same format. This way each router or controller does not
    need to take care of it. It returns the response into the below format...

    Response payload:
        {
            "code": 2XX | 4XX | 5XX,
            "status": "success" | "error" | "failure",
            "result": ...
            "error": ...,
        }

    Where:
        code:
            - 2XX -> For success responses.
            - 4XX -> For service-managed errors.
            - 5XX -> For unmanaged or internal server errors.

        status:
            Contains the text: "success", "failure", or "error". Where "failure" is for HTTP status
            response values from 500 to 599, "error" is for statuses from 400 to 499, and "success" is
            for everything else (e.g. 1XX, 2XX and 3XX responses).

        result:
            Contains the result.

        error:
            Only used for "failure" and "error" statuses, and it contains the error information.
    """

    @wraps(fnc)
    def wrapper(*args, **kwargs):
        try:
            code, result = fnc(*args, **kwargs)

            return {
                "code": code,
                "result": result,
                "status": StatusInfo.SUCCESS
            }

        except (AuthorizationException, ServiceException) as error:
            return {
                "code": error.status_code,
                "status": StatusInfo.ERROR,
                "error": error.get_error_info()
            }

        except InternalServerError as error:
            return {
                "code": error.status_code,
                "status": StatusInfo.FAILURE,
                "error": error.get_error_info()
            }

        except Exception as error:
            return {
                "code": HTTPStatus.INTERNAL_SERVER_ERROR,
                "status": StatusInfo.FAILURE,
                "error": {
                    "type": error.__class__.__name__,
                    "details": str(error)
                }
            }

    return wrapper
