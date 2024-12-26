from typing import Callable, Generic, Hashable, Tuple, TypeVar


T = TypeVar('T')


class DistinctFilter(Generic[T]):
    def __init__(self, f:Callable[[T], Hashable]) -> None:
        self.__encounters = set()
        self.__f = f


    def __call__(self, val: T) -> bool:
        __val = self.__f(val)
        if __val in self.__encounters:
            return False
        self.__encounters.add(__val)
        return True


class Rangifier(Generic[T]):
    def __init__(self, init_val: T) -> None:
        self.__prev: T = init_val

    def __call__(self, val: T) -> Tuple[T, T]:
        res = (self.__prev, val)
        self.__prev = val
        return res