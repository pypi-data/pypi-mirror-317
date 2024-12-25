from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Literal, Type, TypeVar, cast

from iceaxe.base import (
    DBFieldClassDefinition,
)
from iceaxe.comparison import ComparisonBase
from iceaxe.queries_str import QueryLiteral
from iceaxe.sql_types import get_python_to_sql_mapping
from iceaxe.typing import is_column, is_function_metadata

T = TypeVar("T")

DATE_PART_FIELD = Literal[
    "century",
    "day",
    "decade",
    "dow",
    "doy",
    "epoch",
    "hour",
    "isodow",
    "isoyear",
    "microseconds",
    "millennium",
    "milliseconds",
    "minute",
    "month",
    "quarter",
    "second",
    "timezone",
    "timezone_hour",
    "timezone_minute",
    "week",
    "year",
]
DATE_PRECISION = Literal[
    "microseconds",
    "milliseconds",
    "second",
    "minute",
    "hour",
    "day",
    "week",
    "month",
    "quarter",
    "year",
    "decade",
    "century",
    "millennium",
]


class FunctionMetadata(ComparisonBase):
    """
    Represents metadata for SQL aggregate functions and other SQL function operations.
    This class bridges the gap between Python function calls and their SQL representations,
    maintaining type information and original field references.

    ```python {{sticky: True}}
    # Internal representation of function calls:
    metadata = FunctionMetadata(
        literal=QueryLiteral("count(users.id)"),
        original_field=User.id,
        local_name="user_count"
    )
    # Used in query: SELECT count(users.id) AS user_count
    ```
    """

    literal: QueryLiteral
    """
    The SQL representation of the function call
    """

    original_field: DBFieldClassDefinition
    """
    The database field this function operates on
    """

    local_name: str | None = None
    """
    Optional alias for the function result in the query
    """

    def __init__(
        self,
        literal: QueryLiteral,
        original_field: DBFieldClassDefinition,
        local_name: str | None = None,
    ):
        self.literal = literal
        self.original_field = original_field
        self.local_name = local_name

    def to_query(self):
        """
        Converts the function metadata to its SQL representation.

        :return: A tuple of the SQL literal and an empty list of variables
        """
        return self.literal, []


class FunctionBuilder:
    """
    Builder class for SQL aggregate functions and other SQL operations.
    Provides a Pythonic interface for creating SQL function calls with proper type hints.

    This class is typically accessed through the global `func` instance:
    ```python {{sticky: True}}
    from iceaxe import func

    query = select((
        User.name,
        func.count(User.id),
        func.max(User.age)
    ))
    ```
    """

    def count(self, field: Any) -> int:
        """
        Creates a COUNT aggregate function call.

        :param field: The field to count. Can be a column or another function result
        :return: A function metadata object that resolves to an integer count

        ```python {{sticky: True}}
        # Count all users
        total = await conn.execute(select(func.count(User.id)))

        # Count distinct values
        unique = await conn.execute(
            select(func.count(func.distinct(User.status)))
        )
        ```
        """
        metadata = self._column_to_metadata(field)
        metadata.literal = QueryLiteral(f"count({metadata.literal})")
        return cast(int, metadata)

    def distinct(self, field: T) -> T:
        """
        Creates a DISTINCT function call that removes duplicate values.

        :param field: The field to get distinct values from
        :return: A function metadata object preserving the input type

        ```python {{sticky: True}}
        # Get distinct status values
        statuses = await conn.execute(select(func.distinct(User.status)))

        # Count distinct values
        unique_count = await conn.execute(
            select(func.count(func.distinct(User.status)))
        )
        ```
        """
        metadata = self._column_to_metadata(field)
        metadata.literal = QueryLiteral(f"distinct {metadata.literal}")
        return cast(T, metadata)

    def sum(self, field: T) -> T:
        """
        Creates a SUM aggregate function call.

        :param field: The numeric field to sum
        :return: A function metadata object preserving the input type

        ```python {{sticky: True}}
        # Get total of all salaries
        total = await conn.execute(select(func.sum(Employee.salary)))

        # Sum with grouping
        by_dept = await conn.execute(
            select((Department.name, func.sum(Employee.salary)))
            .group_by(Department.name)
        )
        ```
        """
        metadata = self._column_to_metadata(field)
        metadata.literal = QueryLiteral(f"sum({metadata.literal})")
        return cast(T, metadata)

    def avg(self, field: T) -> T:
        """
        Creates an AVG aggregate function call.

        :param field: The numeric field to average
        :return: A function metadata object preserving the input type

        ```python {{sticky: True}}
        # Get average age of all users
        avg_age = await conn.execute(select(func.avg(User.age)))

        # Average with grouping
        by_dept = await conn.execute(
            select((Department.name, func.avg(Employee.salary)))
            .group_by(Department.name)
        )
        ```
        """
        metadata = self._column_to_metadata(field)
        metadata.literal = QueryLiteral(f"avg({metadata.literal})")
        return cast(T, metadata)

    def max(self, field: T) -> T:
        """
        Creates a MAX aggregate function call.

        :param field: The field to get the maximum value from
        :return: A function metadata object preserving the input type

        ```python {{sticky: True}}
        # Get highest salary
        highest = await conn.execute(select(func.max(Employee.salary)))

        # Max with grouping
        by_dept = await conn.execute(
            select((Department.name, func.max(Employee.salary)))
            .group_by(Department.name)
        )
        ```
        """
        metadata = self._column_to_metadata(field)
        metadata.literal = QueryLiteral(f"max({metadata.literal})")
        return cast(T, metadata)

    def min(self, field: T) -> T:
        """
        Creates a MIN aggregate function call.

        :param field: The field to get the minimum value from
        :return: A function metadata object preserving the input type

        ```python {{sticky: True}}
        # Get lowest salary
        lowest = await conn.execute(select(func.min(Employee.salary)))

        # Min with grouping
        by_dept = await conn.execute(
            select((Department.name, func.min(Employee.salary)))
            .group_by(Department.name)
        )
        ```
        """
        metadata = self._column_to_metadata(field)
        metadata.literal = QueryLiteral(f"min({metadata.literal})")
        return cast(T, metadata)

    def abs(self, field: T) -> T:
        """
        Creates an ABS function call to get the absolute value.

        :param field: The numeric field to get the absolute value of
        :return: A function metadata object preserving the input type

        ```python {{sticky: True}}
        # Get absolute value of balance
        abs_balance = await conn.execute(select(func.abs(Account.balance)))
        ```
        """
        metadata = self._column_to_metadata(field)
        metadata.literal = QueryLiteral(f"abs({metadata.literal})")
        return cast(T, metadata)

    def date_trunc(self, precision: DATE_PRECISION, field: T) -> T:
        """
        Truncates a timestamp or interval value to specified precision.

        :param precision: The precision to truncate to ('microseconds', 'milliseconds', 'second', 'minute', 'hour', 'day', 'week', 'month', 'quarter', 'year', 'decade', 'century', 'millennium')
        :param field: The timestamp or interval field to truncate
        :return: A function metadata object preserving the input type

        ```python {{sticky: True}}
        # Truncate timestamp to month
        monthly = await conn.execute(select(func.date_trunc('month', User.created_at)))
        ```
        """
        metadata = self._column_to_metadata(field)
        metadata.literal = QueryLiteral(
            f"date_trunc('{precision}', {metadata.literal})"
        )
        return cast(T, metadata)

    def date_part(self, field: DATE_PART_FIELD, source: Any) -> float:
        """
        Extracts a subfield from a date/time value.

        :param field: The subfield to extract ('century', 'day', 'decade', 'dow', 'doy', 'epoch', 'hour', 'isodow', 'isoyear', 'microseconds', 'millennium', 'milliseconds', 'minute', 'month', 'quarter', 'second', 'timezone', 'timezone_hour', 'timezone_minute', 'week', 'year')
        :param source: The date/time field to extract from
        :return: A function metadata object that resolves to an integer

        ```python {{sticky: True}}
        # Get month from timestamp
        month = await conn.execute(select(func.date_part('month', User.created_at)))
        ```
        """
        metadata = self._column_to_metadata(source)
        metadata.literal = QueryLiteral(f"date_part('{field}', {metadata.literal})")
        return cast(float, metadata)

    def extract(self, field: DATE_PART_FIELD, source: Any) -> int:
        """
        Extracts a subfield from a date/time value using SQL standard syntax.

        :param field: The subfield to extract ('century', 'day', 'decade', 'dow', 'doy', 'epoch', 'hour', 'isodow', 'isoyear', 'microseconds', 'millennium', 'milliseconds', 'minute', 'month', 'quarter', 'second', 'timezone', 'timezone_hour', 'timezone_minute', 'week', 'year')
        :param source: The date/time field to extract from
        :return: A function metadata object that resolves to an integer

        ```python {{sticky: True}}
        # Get year from timestamp
        year = await conn.execute(select(func.extract('year', User.created_at)))
        ```
        """
        metadata = self._column_to_metadata(source)
        metadata.literal = QueryLiteral(f"extract({field} from {metadata.literal})")
        return cast(int, metadata)

    def age(self, timestamp: T, reference: T | None = None) -> T:
        """
        Calculates the difference between two timestamps.
        If reference is not provided, current_date is used.

        :param timestamp: The timestamp to calculate age from
        :param reference: Optional reference timestamp (defaults to current_date)
        :return: A function metadata object preserving the input type

        ```python {{sticky: True}}
        # Get age of a timestamp
        age = await conn.execute(select(func.age(User.birth_date)))

        # Get age between two timestamps
        age_diff = await conn.execute(select(func.age(Event.end_time, Event.start_time)))
        ```
        """
        metadata = self._column_to_metadata(timestamp)
        if reference is not None:
            ref_metadata = self._column_to_metadata(reference)
            metadata.literal = QueryLiteral(
                f"age({metadata.literal}, {ref_metadata.literal})"
            )
        else:
            metadata.literal = QueryLiteral(f"age({metadata.literal})")
        return cast(T, metadata)

    def date(self, field: T) -> T:
        """
        Converts a timestamp to a date by dropping the time component.

        :param field: The timestamp field to convert
        :return: A function metadata object that resolves to a date

        ```python {{sticky: True}}
        # Get just the date part
        event_date = await conn.execute(select(func.date(Event.timestamp)))
        ```
        """
        metadata = self._column_to_metadata(field)
        metadata.literal = QueryLiteral(f"date({metadata.literal})")
        return cast(T, metadata)

    # String Functions
    def lower(self, field: T) -> T:
        """
        Converts string to lowercase.

        :param field: The string field to convert
        :return: A function metadata object preserving the input type
        """
        metadata = self._column_to_metadata(field)
        metadata.literal = QueryLiteral(f"lower({metadata.literal})")
        return cast(T, metadata)

    def upper(self, field: T) -> T:
        """
        Converts string to uppercase.

        :param field: The string field to convert
        :return: A function metadata object preserving the input type
        """
        metadata = self._column_to_metadata(field)
        metadata.literal = QueryLiteral(f"upper({metadata.literal})")
        return cast(T, metadata)

    def length(self, field: Any) -> int:
        """
        Returns length of string.

        :param field: The string field to measure
        :return: A function metadata object that resolves to an integer
        """
        metadata = self._column_to_metadata(field)
        metadata.literal = QueryLiteral(f"length({metadata.literal})")
        return cast(int, metadata)

    def trim(self, field: T) -> T:
        """
        Removes whitespace from both ends of string.

        :param field: The string field to trim
        :return: A function metadata object preserving the input type
        """
        metadata = self._column_to_metadata(field)
        metadata.literal = QueryLiteral(f"trim({metadata.literal})")
        return cast(T, metadata)

    def substring(self, field: T, start: int, length: int) -> T:
        """
        Extracts substring.

        :param field: The string field to extract from
        :param start: Starting position (1-based)
        :param length: Number of characters to extract
        :return: A function metadata object preserving the input type
        """
        metadata = self._column_to_metadata(field)
        metadata.literal = QueryLiteral(
            f"substring({metadata.literal} from {start} for {length})"
        )
        return cast(T, metadata)

    # Mathematical Functions
    def round(self, field: T) -> T:
        """
        Rounds to nearest integer.

        :param field: The numeric field to round
        :return: A function metadata object preserving the input type
        """
        metadata = self._column_to_metadata(field)
        metadata.literal = QueryLiteral(f"round({metadata.literal})")
        return cast(T, metadata)

    def ceil(self, field: T) -> T:
        """
        Rounds up to nearest integer.

        :param field: The numeric field to round up
        :return: A function metadata object preserving the input type
        """
        metadata = self._column_to_metadata(field)
        metadata.literal = QueryLiteral(f"ceil({metadata.literal})")
        return cast(T, metadata)

    def floor(self, field: T) -> T:
        """
        Rounds down to nearest integer.

        :param field: The numeric field to round down
        :return: A function metadata object preserving the input type
        """
        metadata = self._column_to_metadata(field)
        metadata.literal = QueryLiteral(f"floor({metadata.literal})")
        return cast(T, metadata)

    def power(self, field: T, exponent: int | float) -> T:
        """
        Raises a number to the specified power.

        :param field: The numeric field to raise
        :param exponent: The power to raise to
        :return: A function metadata object preserving the input type
        """
        metadata = self._column_to_metadata(field)
        metadata.literal = QueryLiteral(f"power({metadata.literal}, {exponent})")
        return cast(T, metadata)

    def sqrt(self, field: T) -> T:
        """
        Calculates square root.

        :param field: The numeric field to calculate square root of
        :return: A function metadata object preserving the input type
        """
        metadata = self._column_to_metadata(field)
        metadata.literal = QueryLiteral(f"sqrt({metadata.literal})")
        return cast(T, metadata)

    # Aggregate Functions
    def array_agg(self, field: T) -> list[T]:
        """
        Collects values into an array.

        :param field: The field to aggregate
        :return: A function metadata object that resolves to a list
        """
        metadata = self._column_to_metadata(field)
        metadata.literal = QueryLiteral(f"array_agg({metadata.literal})")
        return cast(list[T], metadata)

    def string_agg(self, field: Any, delimiter: str) -> str:
        """
        Concatenates values with delimiter.

        :param field: The field to aggregate
        :param delimiter: The delimiter to use between values
        :return: A function metadata object that resolves to a string
        """
        metadata = self._column_to_metadata(field)
        metadata.literal = QueryLiteral(
            f"string_agg({metadata.literal}, '{delimiter}')"
        )
        return cast(str, metadata)

    # Type Conversion Functions
    def cast(self, field: Any, type_name: Type[T]) -> T:
        """
        Converts value to specified type.

        :param field: The field to convert
        :param type_name: The target Python type to cast to
        :return: A function metadata object with the new type

        ```python {{sticky: True}}
        # Cast a string to integer
        int_value = await conn.execute(select(func.cast(User.string_id, int)))

        # Cast a float to string
        str_value = await conn.execute(select(func.cast(Account.balance, str)))

        # Cast a string to enum
        status = await conn.execute(select(func.cast(User.status_str, UserStatus)))
        ```
        """

        metadata = self._column_to_metadata(field)

        # Special handling for enums
        if issubclass(type_name, Enum):
            metadata.literal = QueryLiteral(
                f"cast({metadata.literal} as {type_name.__name__.lower()})"
            )
        else:
            sql_type = get_python_to_sql_mapping().get(type_name)  # type: ignore
            if not sql_type:
                raise ValueError(f"Unsupported type for casting: {type_name}")
            metadata.literal = QueryLiteral(f"cast({metadata.literal} as {sql_type})")

        return cast(T, metadata)

    def to_char(self, field: Any, format: str) -> str:
        """
        Converts value to string with format.

        :param field: The field to convert
        :param format: The format string
        :return: A function metadata object that resolves to a string
        """
        metadata = self._column_to_metadata(field)
        metadata.literal = QueryLiteral(f"to_char({metadata.literal}, '{format}')")
        return cast(str, metadata)

    def to_number(self, field: Any, format: str) -> float:
        """
        Converts string to number with format.

        :param field: The string field to convert
        :param format: The format string
        :return: A function metadata object that resolves to a float
        """
        metadata = self._column_to_metadata(field)
        metadata.literal = QueryLiteral(f"to_number({metadata.literal}, '{format}')")
        return cast(float, metadata)

    def to_timestamp(self, field: Any, format: str) -> datetime:
        """
        Converts string to timestamp with format.

        :param field: The string field to convert
        :param format: The format string
        :return: A function metadata object that resolves to a timestamp
        """
        metadata = self._column_to_metadata(field)
        metadata.literal = QueryLiteral(f"to_timestamp({metadata.literal}, '{format}')")
        return cast(datetime, metadata)

    def _column_to_metadata(self, field: Any) -> FunctionMetadata:
        """
        Internal helper method to convert a field to FunctionMetadata.
        Handles both raw columns and nested function calls.

        :param field: The field to convert
        :return: A FunctionMetadata instance
        :raises ValueError: If the field cannot be converted to a column
        """
        if is_function_metadata(field):
            return field
        elif is_column(field):
            return FunctionMetadata(literal=field.to_query()[0], original_field=field)
        else:
            raise ValueError(
                f"Unable to cast this type to a column: {field} ({type(field)})"
            )


func = FunctionBuilder()
"""
A global instance of FunctionBuilder that provides SQL function operations for use in queries.
This instance offers a comprehensive set of SQL functions including aggregates, string operations,
mathematical functions, date/time manipulations, and type conversions.

Available function categories:
- Aggregate Functions: count, sum, avg, min, max, array_agg, string_agg
- String Functions: lower, upper, length, trim, substring
- Mathematical Functions: abs, round, ceil, floor, power, sqrt
- Date/Time Functions: date_trunc, date_part, extract, age, date
- Type Conversion: cast, to_char, to_number, to_timestamp

```python {{sticky: True}}
from iceaxe import func, select

# Aggregate functions
total_users = await conn.execute(select(func.count(User.id)))
avg_salary = await conn.execute(select(func.avg(Employee.salary)))
unique_statuses = await conn.execute(select(func.distinct(User.status)))

# String operations
users = await conn.execute(select((
    User.id,
    func.lower(User.name),
    func.upper(User.email),
    func.length(User.bio)
)))

# Date/time operations
monthly_stats = await conn.execute(select((
    func.date_trunc('month', Event.created_at),
    func.count(Event.id)
)).group_by(func.date_trunc('month', Event.created_at)))

# Mathematical operations
account_stats = await conn.execute(select((
    Account.id,
    func.abs(Account.balance),
    func.ceil(Account.interest_rate)
)))

# Type conversions
converted = await conn.execute(select((
    func.cast(User.string_id, int),
    func.to_char(User.created_at, 'YYYY-MM-DD'),
    func.cast(User.status_str, UserStatus)
)))

# Complex aggregations
department_stats = await conn.execute(
    select((
        Department.name,
        func.array_agg(Employee.name),
        func.string_agg(Employee.email, ','),
        func.sum(Employee.salary)
    )).group_by(Department.name)
)
```
"""
