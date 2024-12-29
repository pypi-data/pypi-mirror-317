from dataclasses import dataclass, asdict, fields
from datetime import datetime
from typing import Any, Dict, Type, TypeVar, Union
from enum import Enum
import json

T = TypeVar("T", bound="BaseModel")

@dataclass
class BaseModel:
    """
    A generic base class for models with dataclass support.
    Provides generic encode and decode methods.
    """

    @classmethod
    def decode(cls: Type[T], data: Union[str, Dict[str, Any]]) -> T:
        """
        Decodes a JSON string or dictionary into an instance of the class.

        Args:
            data: A JSON string or dictionary representing the object.

        Returns:
            An instance of the class.

        Raises:
            ValueError: If the data is invalid or required fields are missing.
        """
        if isinstance(data, str):
            try:
                data = json.loads(data)
            except json.JSONDecodeError as e:
                raise ValueError(f"Invalid JSON string: {e}")

        parsed_data = {}
        for field in fields(cls):
            field_name = field.name
            field_type = field.type
            if field_name in data:
                value = data[field_name]
                if field_type == datetime and isinstance(value, str):
                    parsed_data[field_name] = datetime.fromisoformat(value)
                elif isinstance(field_type, type) and issubclass(field_type, Enum):
                    parsed_data[field_name] = field_type(value)
                elif hasattr(field_type, "decode") and callable(getattr(field_type, "decode")):
                    parsed_data[field_name] = field_type.decode(value)
                else:
                    parsed_data[field_name] = value
            elif field.default is not None or field.default_factory is not None:
                parsed_data[field_name] = field.default if field.default != field.default_factory else field.default_factory()
            else:
                raise ValueError(f"Missing required field: {field_name}")

        return cls(**parsed_data)

    def encode(self) -> str:
        """
        Encodes the instance into a JSON string.

        Returns:
            A JSON string representation of the instance.
        """
        return json.dumps(asdict(self), default=str, indent=4)
