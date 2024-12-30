from typing import Any


class ValidationError(Exception):
    detail: str
    input_value: Any

    def __init__(self, detail: str, *, input_value: Any, **kwargs: Any) -> None:
        self.detail = detail
        self.input_value = input_value
        self.arguments = kwargs
