from typing import Any
import json

from sqlalchemy import Dialect
from sqlalchemy.types import TypeDecorator, String

from belial_db.data import Vector4


class Vector4Type(TypeDecorator[Vector4]):
    """Custom SQLAlchemy type for storing Vector4 objects as JSON strings."""

    impl = String

    def process_bind_param(self, value: Any, dialect: Any) -> str | None:
        """Convert a Vector4 object to a JSON string for storage in the database.

        Args:
            value (Any): The value to be bound to the database.
            dialect (Any): The dialect in use.

        Returns:
            str | None: A JSON string representation of the Vector4 object, or None.
        """
        if isinstance(value, Vector4):
            return value.model_dump_json()
        return value

    def process_result_value(self, value: str | None, dialect: Dialect) -> Vector4 | None:
        """Convert a JSON string from the database back to a Vector4 object.

        Args:
            value (str | None): The value retrieved from the database.
            dialect (Dialect): The dialect in use.

        Returns:
            Vector4 | None: A Vector4 object created from the JSON string, or None.
        """
        if value is not None:
            return Vector4(**json.loads(value))
        return value
