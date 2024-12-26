import datetime
import warnings
from typing import Any, Self, overload

from dateutil.parser import parse
from dateutil.relativedelta import relativedelta
from pydantic import GetCoreSchemaHandler, GetJsonSchemaHandler
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import core_schema


class Date(datetime.datetime):
    """
    A subclass of `datetime.datetime` that provides additional functionality for working with dates.

    This class extends the `datetime.datetime` class and adds methods for formatting dates, adding or subtracting time intervals,
    and getting the first or last day of the year.

    Additionally, this class provides support for pydantic serialization and deserialization.

    """

    _spanish_months = {
        1: "Enero",
        2: "Febrero",
        3: "Marzo",
        4: "Abril",
        5: "Mayo",
        6: "Junio",
        7: "Julio",
        8: "Agosto",
        9: "Septiembre",
        10: "Octubre",
        11: "Noviembre",
        12: "Diciembre",
    }

    @overload
    def __new__(
        cls,
    ) -> Self:
        """
        Create and return a new instance of the class.

        This method is a static method that is responsible for creating a new instance
        of the class. It is called before the __init__ method and is used to create the
        object itself.

        Returns:
            Self: A new instance of the class.

        """

    @overload
    def __new__(
        cls,
        year: int,
        month: int,
        day: int,
        hour: int = 0,
        minute: int = 0,
        second: int = 0,
        *,
        fold: int = 0,
    ) -> Self:
        """
        Create a new instance of the class.

        Args:
            year (int): The year value.
            month (int): The month value.
            day (int): The day value.
            hour (int, optional): The hour value. Defaults to 0.
            minute (int, optional): The minute value. Defaults to 0.
            second (int, optional): The second value. Defaults to 0.

        Returns:
            Self: The newly created instance.
        """

    @overload
    def __new__(
        cls,
        date: datetime.datetime,
    ) -> Self:
        """
        Create a new instance of the class.

        Args:
            date (datetime.datetime): The date to be used for creating the instance.

        Returns:
            Self: The newly created instance.

        """

    @overload
    def __new__(
        cls,
        str_date: str,
    ) -> Self:
        """
        Create a new instance of the class.

        Args:
            str_date (str): The string representation of the date.

        Returns:
            Self: The newly created instance of the class.
        """

    def __new__(  # type: ignore
        cls,
        *args,
    ):
        if not args:
            date = datetime.datetime.now()
        else:
            arg1 = args[0]

            if isinstance(arg1, datetime.datetime):
                date = arg1
            elif isinstance(arg1, str):
                try:
                    try:
                        date = datetime.datetime.strptime(arg1, "%Y-%m")
                    except ValueError:
                        date = parse(arg1)
                except ValueError as e:
                    raise ValueError("Date format not recognized") from e

            elif isinstance(arg1, bytes):
                warnings.warn(
                    "Giving default value to a Date in a model will use the current date and time of the model definition. If you want to use the current date and time when the model is created, use a default factory function instead.",
                    category=EarlyInstanceWarning,
                    stacklevel=10,
                )
                return super().__new__(cls, *args)

            else:
                date = datetime.datetime(*args)

        return super().__new__(
            cls,
            date.year,
            date.month,
            date.day,
            date.hour,
            date.minute,
            date.second,
        )

    def __str__(self):
        return self.rfc3339_string

    @property
    def date_string(self):
        """
        Converts the date object to a string representation in the format 'YYYY-MM-DD'.

        Returns:
            str: The date as a string in the format 'YYYY-MM-DD'.
        """
        return self.strftime("%Y-%m-%d")

    @property
    def iso_string(self):
        """
        Returns the ISO 8601 formatted string representation of the date.

        :return: The ISO 8601 formatted string representation of the date.
        :rtype: str
        """
        return self.isoformat()

    @property
    def europe_string(self):
        """
        Returns the date and time in European format (dd/mm/yyyy HH:MM:SS).

        Returns:
            str: The date and time in European format.
        """
        return self.strftime("%d/%m/%Y %H:%M:%S")

    @property
    def latam_string(self):
        """
        Returns the date and time in Latam format (dd/mm/yyyy).

        Returns:
            str: The date and time in Latam format.
        """
        return self.strftime("%d/%m/%Y")

    @property
    def rfc2822_string(self):
        """
        Returns the date and time formatted as a string in RFC 2822 format.

        The format of the returned string is: "Day, DD Month YYYY HH:MM:SS",
        where Day is the abbreviated day of the week (e.g., Mon, Tue, etc.),
        DD is the day of the month (e.g., 01, 02, etc.), Month is the abbreviated
        month name (e.g., Jan, Feb, etc.), YYYY is the four-digit year, HH is
        the hour in 24-hour format (e.g., 00, 01, etc.), MM is the minute, and
        SS is the second.

        Returns:
            str: The date and time formatted as a string in RFC 2822 format.
        """
        return self.strftime("%a, %d %b %Y %H:%M:%S")

    @property
    def rfc3339_string(self):
        """
        Returns the RFC 3339 formatted string representation of the date.

        The RFC 3339 format is a profile of the ISO 8601 standard for representing dates and times.
        This method appends the letter 'Z' to the end of the string to indicate that the time is in UTC.

        Returns:
            str: The RFC 3339 formatted string representation of the date.
        """
        return self.isoformat() + "Z"

    @property
    def local_string(self):
        """
        Returns a string representation of the date and time in the local timezone.

        Returns:
            str: A string representation of the date and time in the local timezone.
        """
        return self.strftime("%c")

    @property
    def human_readable(self):
        """
        Returns a human-readable representation of the date and time.

        Returns:
            str: A string representing the date and time in the format:
                 "{day} de {month} de {year} a las {hour}:{minute}"
        """
        return f"{self.day} de {self._spanish_months[self.month]} de {self.year} a las {str(self.hour).zfill(2)}:{str(self.minute).zfill(2)}"

    def human_readable_date(self):
        """
        Returns a human-readable date string in the format: "{day} de {month} de {year}".
        """
        return f"{self.day} de {self._spanish_months[self.month]} de {self.year}"

    def human_readable_time(self):
        """
        Return a pretty string representation of the time
        in the format HH:MM.

        Returns:
            str: A formatted string representing the time.
        """
        return f"{str(self.hour).zfill(2)}:{str(self.minute).zfill(2)}"

    def add_days(self, days: int):
        """
        Adds the specified number of days to the current date.

        Args:
            days (int): The number of days to add.

        Returns:
            datetime: The resulting date after adding the specified number of days.
        """
        return self + relativedelta(days=days)

    def add_months(self, months: int):
        """
        Adds the specified number of months to the current date.

        Args:
            months (int): The number of months to add.

        Returns:
            datetime: The resulting date after adding the specified number of months.
        """
        return self + relativedelta(months=months)

    def add_years(self, years: int):
        """
        Adds the specified number of years to the current date.

        Args:
            years (int): The number of years to add.

        Returns:
            datetime: The resulting date after adding the specified number of years.
        """
        return self + relativedelta(years=years)

    def add_hours(self, hours: int):
        """
        Adds the specified number of hours to the current date and time.

        Args:
            hours (int): The number of hours to add.

        Returns:
            datetime: The updated date and time after adding the specified hours.
        """
        return self + relativedelta(hours=hours)

    def add_minutes(self, minutes: int):
        """
        Adds the specified number of minutes to the current date and time.

        Args:
            minutes (int): The number of minutes to add.

        Returns:
            datetime: The updated date and time.

        """
        return self + relativedelta(minutes=minutes)

    def add_seconds(self, seconds: int):
        """
        Adds the specified number of seconds to the current date and time.

        Args:
            seconds (int): The number of seconds to add.

        Returns:
            datetime: The updated date and time.

        """
        return self + relativedelta(seconds=seconds)

    @property
    def first_day_of_year(self):
        """
        Returns a new datetime object representing the first day of the year.

        Returns:
            datetime: A new datetime object with the month, day, hour, minute, second, and microsecond set to 0.
        """
        return self.replace(
            month=1,
            day=1,
            hour=0,
            minute=0,
            second=0,
            microsecond=0,
        )

    @property
    def last_day_of_year(self):
        """
        Returns a datetime object representing the last day of the year.

        Returns:
            datetime: A datetime object representing the last day of the year.
        """
        return self.replace(
            month=12,
            day=31,
            hour=23,
            minute=59,
            second=59,
            microsecond=999999,
        )

    @property
    def first_day_of_month(self):
        """
        Returns a new datetime object with the first day of the month,
        overriding the day, hour, minute, second, and microsecond attributes to 0.

        Returns:
            datetime: A new datetime object with the first day of the month.
        """
        return self.replace(
            day=1,
            hour=0,
            minute=0,
            second=0,
            microsecond=0,
        )

    @property
    def last_day_of_month(self):
        """
        Returns the last day of the month for the given date.

        This method replaces the day, hour, minute, second, and microsecond
        components of the date with the last day, 23:59:59.999999 of the month.

        Returns:
            datetime: The last day of the month.
        """
        return self.replace(
            day=1,
            hour=23,
            minute=59,
            second=59,
            microsecond=999999,
        ) + relativedelta(months=1, days=-1)

    @classmethod
    def overlaps(cls, start1, end1, start2, end2) -> bool:
        """
        Check if two time intervals overlap.

        Args:
            start1 (datetime): The start time of the first interval.
            end1 (datetime): The end time of the first interval.
            start2 (datetime): The start time of the second interval.
            end2 (datetime): The end time of the second interval.

        Returns:
            bool: True if the intervals overlap, False otherwise.
        """
        if not end1:
            end1 = cls.max
        if not end2:
            end2 = cls.max
        return start1 <= end2 and start2 <= end1

    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        _source_type: Any,
        _handler: GetCoreSchemaHandler,
    ) -> core_schema.CoreSchema:
        """
        Returns a pydantic_core.CoreSchema that behaves in the following ways:

        * strings will be parsed as `Date`
        * `Date` instances will be parsed as `Date` instances without any changes
        * Nothing else will pass validation
        * Serialization will always return just a string
        """

        def validate_from_str(value: str):
            date = None
            if isinstance(value, datetime.datetime):
                date = Date(
                    value.year,
                    value.month,
                    value.day,
                    value.hour,
                    value.minute,
                    value.second,
                )
            if isinstance(value, str):
                date = Date(value)
            return date

        def serialize(value: Date) -> str:
            return str(value)

        from_str_schema = core_schema.no_info_plain_validator_function(
            validate_from_str
        )

        schema_date = core_schema.json_or_python_schema(
            json_schema=from_str_schema,
            python_schema=from_str_schema,
            serialization=core_schema.plain_serializer_function_ser_schema(
                serialize, when_used="json"
            ),
        )

        return schema_date

    @classmethod
    def __get_pydantic_json_schema__(
        cls,
        _core_schema: core_schema.CoreSchema,
        handler: GetJsonSchemaHandler,
    ) -> JsonSchemaValue:
        schema_date = handler(core_schema.str_schema())
        schema_date.update(
            {
                "description": "A subclass of datetime.datetime that provides additional functionality for working with dates."
            }
        )
        return schema_date


class EarlyInstanceWarning(Warning):
    pass
