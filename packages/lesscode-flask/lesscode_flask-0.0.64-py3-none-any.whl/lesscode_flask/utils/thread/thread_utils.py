import threading

from flask import copy_current_request_context


def run_in_thread(func_list, is_throw_error=False):
    results = []
    threads = []
    result_locks = []

    def wrapper(_func, _kwargs, _result, _lock, _is_throw_error=True):
        @copy_current_request_context
        def _thread_func():
            try:
                res = func(**kwargs)
                with _lock:
                    _result.append(res)
            except Exception as e:
                if _is_throw_error:
                    raise e
                else:
                    with _lock:
                        _result.append(None)

        return _thread_func

    for sub_list in func_list:
        func = sub_list[0]
        kwargs = sub_list[1]
        result = []
        lock = threading.Lock()
        result_locks.append(lock)
        thread_func = wrapper(func, kwargs, result, lock, is_throw_error)
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
