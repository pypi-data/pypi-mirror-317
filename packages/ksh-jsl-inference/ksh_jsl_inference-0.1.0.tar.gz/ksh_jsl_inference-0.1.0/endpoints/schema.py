from typing import Dict, List, Type


MODEL_LOCATION = "/opt/ml/model"
DEFAULT_INPUT_KEYS = ["text", "input_text", "texts", "input_texts"]


class Schema:
    def __init__(
        self,
        field: str,
        typing: Type,
        default=None,
        required: bool = False,
        dtypes: List[str] = [],
    ):
        self._field = field
        self._required = required
        self._typing = typing
        self._dtypes = dtypes
        self._default = default

    def validate(self, data: Dict):
        if self._required and self._field not in data:
            raise ValueError(f"Key {self._field} is missing in the data")
        value = data.get(self._field, self._default)
        if self._dtypes:
            if value not in self._dtypes:
                raise ValueError(f"Key {self._field} must be of type {self._dtypes}")
        if isinstance(value, list):
            for item in value:
                if not isinstance(item, self._typing):
                    raise ValueError(
                        f"Key {self._field} must be of type {self._typing}"
                    )
        elif not isinstance(value, self._typing):
            raise ValueError(f"Key {value} must be of type {self._typing}")
        return value
