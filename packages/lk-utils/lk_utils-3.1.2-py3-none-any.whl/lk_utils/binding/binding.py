import typing as t
from functools import partial
from traceback import extract_stack
from collections import defaultdict

from .signal import get_func_id


class T:
    Func = t.TypeVar('Func', bound=t.Callable[[], t.Any])
    FuncWrapper = t.Callable[[Func], Func]
    Trigger = t.Callable  # callable[[func, *args, **kwargs], any]


class TARGET:
    pass


_bound_funcs = set()


def call_once(*_args, **_kwargs) -> T.FuncWrapper:
    def wrapper(func: T.Func) -> T.Func:
        func(*_args, **_kwargs)
        return func
    return wrapper


def bind_with(trigger: T.Trigger) -> T.FuncWrapper:
    def decorator(func: T.Func) -> T.Func:
        if (x := (id(trigger), get_func_id(func))) not in _bound_funcs:
            _bound_funcs.add(x)
            trigger(func)
        return func
    return decorator


class DeferredFunctions:
    # class Slot:
    #     pass
    
    def __init__(self) -> None:
        # self._funcs = defaultdict(list)
        self._funcs = {}
        # self._slots = {}
        
    def add(self, name: str = None):
        if name is None:
            stack = extract_stack(limit=2)[0]
            name = '{}:{}'.format(stack.filename, stack.lineno)
        self._funcs.setdefault(name, [])
        return partial(self.call, __name=name)
        
    def call(self, *args, __name: str, **kwargs) -> None:
        if self._funcs[__name]:
            for f in self._funcs[__name]:
                f(*args, **kwargs)
        else:
            print(f'no slot for {__name}!', ':pv8')


# -----------------------------------------------------------------------------


# def call_once(*_args, **_kwargs) -> T.FuncWrapper:
#     def decorator(func: T.Func) -> T.Func:
#         func(*_args, **_kwargs)
#         return func
#     return decorator
#
#
# def bind(
#     trigger: t.Callable,
#     *_args,
#     **_kwargs,
#     # args: tuple = (TARGET,),
#     # kwargs: dict = None,
#     # *,
#     # args0: t.Optional[tuple] = None,
#     # kwargs0: t.Optional[dict] = None,
#     # args1: t.Optional[tuple] = None,
#     # kwargs1: t.Optional[dict] = None,
# ) -> t.Callable[[T.Func], T.Func]:
#     _is_func_in_params = bool(
#         TARGET in _args or
#         any(x is TARGET for x in _kwargs.values())
#     )
#
#     def decorator(func: T.Func) -> T.Func:
#         bound_id = (id(trigger), get_func_id(func))
#         if bound_id not in _bound_funcs:
#             _bound_funcs.add(bound_id)
#             # if class `TARGET` in `_args` or in `_kwargs`, replace it \
#             # with `func`.
#             if _is_func_in_params:
#                 args = (func if x is TARGET else x for x in _args)
#                 kwargs = {k: (func if v is TARGET else v) for k, v in _kwargs.items()}
#             trigger(*args, **kwargs)
#         return func
#
#     return decorator
