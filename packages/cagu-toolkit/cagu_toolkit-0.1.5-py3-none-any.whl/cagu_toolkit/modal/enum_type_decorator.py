from enum import Enum
from typing import Optional

from sqlalchemy import Integer, TypeDecorator, String


class EnumTypeDecorator(TypeDecorator):
    """
    TypeDecorator for Enum, dynamically determines whether to store
    the Enum as Integer (TINYINT) or String (VARCHAR) based on the Enum values.
    """
    impl = Integer  # Default type is Integer (TINYINT)

    def __init__(self, enum_class, *args, **kwargs):
        """
        Initialize with enum class. This determines whether the Enum values
        are of type int or str to decide the column type in the database.
        """
        self.enum_class = enum_class
        # Choose the appropriate type based on the enum values
        if all(isinstance(e.value, int) for e in enum_class):
            self.impl = Integer  # Use Integer (TINYINT) for integer values
        else:
            self.impl = String  # Use String (VARCHAR) for non-integer values

        super().__init__(*args, **kwargs)

    def process_bind_param(self, value: Optional['Enum'], dialect):
        """
        Converts Enum value to a format suitable for storage in the database:
        - If the database column is Integer (TINYINT), convert to integer;
        - If the database column is String (VARCHAR), convert to string.
        """
        if value is not None:
            if isinstance(value, self.enum_class):
                return value.value  # Convert Enum to its value (integer or string)
            else:
                raise ValueError(f"Invalid value for Enum: {value}")
        return value

    def process_result_value(self, value: Optional[int], dialect):
        """
        Converts a database value back to the corresponding Enum:
        - If the column is Integer (TINYINT), convert to Enum;
        - If the column is String (VARCHAR), convert to Enum.
        """
        if value is not None:
            # Ensure the value is valid for the Enum class before trying to convert
            return self.enum_class(value)
        return value
