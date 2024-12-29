# -*- coding: utf-8 -*-

from functools import wraps
from typing import Callable


def cache(fcn: Callable):
    """ Keep a cache of previous function calls """

    @wraps(fcn)
    def wrapper_cache(*args, **kwargs):
        cache_key = args + tuple(kwargs.items())
        if cache_key not in wrapper_cache.cache:
            wrapper_cache.cache[cache_key] = fcn(*args, **kwargs)

        return wrapper_cache.cache[cache_key]

    wrapper_cache.cache = dict()
    return wrapper_cache
