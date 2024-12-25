import hashlib
import functools
from typing import Callable


class ErrorHandler:
    def __init__(self, func: Callable):
        functools.update_wrapper(self, func)
        self.func = func

    def __call__(self, *args, **kwargs):
        # 获取函数名
        func_name = self.func.__name__

        # 构建参数信息
        params = []
        if len(args) > 1:  # 跳过 self 参数
            params.extend([str(arg) for arg in args[1:]])
        if kwargs:
            params.extend([f"{k}={v}" for k, v in kwargs.items()])
        params_str = ", ".join(params)

        try:
            return self.func(*args, **kwargs)
        except Exception as e:
            raise Exception(
                f"Function '{func_name}' failed. "
                f"Parameters: [{params_str}]. "
                f"Error: {str(e)}"
            )

    def __get__(self, obj, objtype):
        """Support instance methods"""
        return functools.partial(self.__call__, obj)

