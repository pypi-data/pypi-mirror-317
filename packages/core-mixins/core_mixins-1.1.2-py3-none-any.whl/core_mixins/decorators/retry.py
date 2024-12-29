# -*- coding: utf-8 -*-

from functools import wraps
from logging import Logger
from time import sleep
from typing import Callable, Type, Tuple


def retry(
        fcn: Callable = None, tries: int = 3, delay: int = 1, backoff: int = 2,
        exceptions: Tuple[Type[BaseException]] = (Exception,),
        logger: Logger = None):

    """
    It retries the decorated function using an exponential
    backoff in case of errors (exceptions) in the
    execution...
    """

    def decorator_retry(_fcn):
        @wraps(_fcn)
        def function_retry(*args, **kwargs):
            _tries, _delay = tries, delay
            while _tries > 1:
                try:
                    return _fcn(*args, **kwargs)

                except exceptions as error:
                    if logger:
                        logger.warning(f"Retrying in {_delay}. Because: {error}")

                    sleep(delay)
                    _tries -= 1
                    _delay *= backoff

            return _fcn(*args, **kwargs)

        return function_retry

    if not fcn:
        return decorator_retry

    return decorator_retry(fcn)
