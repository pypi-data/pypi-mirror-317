from typing import Any
import json

from sqlalchemy import Dialect
from sqlalchemy.types import TypeDecorator, String

from belial_db.data import Vector3


class Vector3Type(TypeDecorator[Vector3]):
    """Custom SQLAlchemy type for handling Vector3 objects."""

    impl = String

    def process_bind_param(self, value: Any, dialect: Any) -> str | None:
        """Convert a Vector3 object to a JSON string for storage in the database.

        Args:
            value (Any): The value to be bound to the database.
            dialect (Any): The dialect in use.

        Returns:
            str | None: A JSON string representation of the Vector3 object, or the original value if not a Vector3.
        """
        if isinstance(value, Vector3):
            return value.model_dump_json()
        return value

    def process_result_value(self, value: str | None, dialect: Dialect) -> Vector3 | None:
        """Convert a JSON string from the database back to a Vector3 object.

        Args:
            value (str | None): The value retrieved from the database.
            dialect (Dialect): The dialect in use.

        Returns:
            Vector3 | None: A Vector3 object created from the JSON string, or None if the value is None.
        """
        if value is not None:
            return Vector3(**json.loads(value))
        return value
