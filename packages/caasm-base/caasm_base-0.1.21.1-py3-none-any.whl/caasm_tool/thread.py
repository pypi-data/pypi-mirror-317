import ctypes
import inspect


def async_raise(tid, exc_type=SystemExit()):
    """
    线程退出，这种方法是强制杀死线程，但是如果线程中涉及获取释放锁，可能会导致死锁。
    :param tid: thread id
    :param exc_type: https://docs.python.org/zh-cn/3.8/library/exceptions.html
    :return: None
    """
    """raises the exception, performs cleanup if needed"""
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exc_type):
        exc_type = type(exc_type)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exc_type))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")
