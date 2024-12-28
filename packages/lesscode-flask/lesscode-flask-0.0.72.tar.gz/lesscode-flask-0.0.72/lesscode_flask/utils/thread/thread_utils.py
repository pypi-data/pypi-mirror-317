import threading
from typing import List

from flask import copy_current_request_context


class MyThread:
    def __init__(self, target, args, kwargs):
        self.target = target
        self.args = args
        self.kwargs = kwargs


def run_in_thread(func_list: List[MyThread], is_throw_error=False):
    results = []
    threads = []
    result_locks = []

    def wrapper(_func, _args, _kwargs, _result, _lock, _is_throw_error=True):
        @copy_current_request_context
        def _thread_func():
            try:
                res = _func(*_args, **kwargs)
                with _lock:
                    _result.append(res)
            except Exception as e:
                if _is_throw_error:
                    raise e
                else:
                    with _lock:
                        _result.append(None)

        return _thread_func

    for obj in func_list:
        target = obj.target
        args = obj.args or []
        kwargs = obj.kwargs or dict()
        result = []
        lock = threading.Lock()
        result_locks.append(lock)
        thread_func = wrapper(_func=target, _args=args, _kwargs=kwargs, _result=result, _lock=lock,
                              _is_throw_error=is_throw_error)
        t = threading.Thread(target=thread_func)
        threads.append(t)
        results.append(result)
        t.start()

    for t in threads:
        t.join()

    final_results = []
    for result, lock in zip(results, result_locks):
        with lock:
            final_results.append(result[0])
    return final_results
