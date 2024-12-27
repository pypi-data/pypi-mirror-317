import threading

from flask import copy_current_request_context


def run_in_thread(func_list):
    results = []
    threads = []

    def wrapper(_func, _kwargs, _result, _lock=None):
        @copy_current_request_context
        def _thread_func():
            try:
                res = func(**kwargs)
                _result.append(res)
            except Exception as e:
                _result.append(e)

        return _thread_func

    for sub_list in func_list:
        func = sub_list[0]
        kwargs = sub_list[1]
        result = []
        thread_func = wrapper(func, kwargs, result, None)
        t = threading.Thread(target=thread_func)
        threads.append(t)
        results.append(result)
        t.start()

    for t in threads:
        t.join()

    return results
