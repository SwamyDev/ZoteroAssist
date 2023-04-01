from typing import TypeVar, Generic, Optional

ResultT = TypeVar('ResultT')


class Result(Generic[ResultT]):
    class InvalidResult(RuntimeError):
        ...

    def __init__(self, value: Optional[ResultT] = None, err_msg: Optional[str] = None):
        self._value = value
        self._err_msg = err_msg

    @classmethod
    def ok(cls, value: ResultT) -> "Result":
        return cls(value=value)

    @classmethod
    def error(cls, err_msg: str) -> "Result":
        return cls(err_msg=err_msg)

    def unwrap(self) -> ResultT:
        if self.is_err():
            raise Result.InvalidResult(self._err_msg)
        return self._value

    def is_err(self) -> bool:
        return self._err_msg is not None

    def __or__(self, other: ResultT):
        if self.is_err():
            return other
        return self
