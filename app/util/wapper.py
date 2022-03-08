from functools import wraps

func_lock_dc = {}

async def wait_lock():
    return {}, 'wait for lock'

def func_lock(lock_param):
    def func_lock_decorator(func):
        @wraps(func)
        def wrapped_function(*args, **kwargs):
            param = kwargs[lock_param]
            if func.__name__ not in func_lock_dc:
                func_lock_dc[func.__name__] = []
            if param in func_lock_dc[func.__name__]:
                return wait_lock
            func_lock_dc[func.__name__].append(param)
            res = func(*args, **kwargs)
            func_lock_dc[func.__name__].remove(param)
            return res
        return wrapped_function
    return func_lock_decorator
