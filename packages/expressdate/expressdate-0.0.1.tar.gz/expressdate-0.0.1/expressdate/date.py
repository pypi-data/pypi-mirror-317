from __future__ import annotations
from datetime import date, timedelta
from typing import Iterator
from .parse import ExpressDateParser

__all__ = ["ExpressDate"]


class ExpressDate:
    """
    Represents one or more dates that can be created from a Python date object
    or a string expression. This class provides arithmetic operations such as
    adding or subtracting days, as well as set-like and logical operations
    (union, intersection, difference, and symmetric difference) for easy
    date manipulation and comparison.
    """

    def __init__(self, expr: date | str):
        """
        Initializes an ExpressDate instance.

        If the argument is a string, it is parsed to extract one or more dates.
        If the argument is a Python date object, it is stored as a single date.

        :param expr: A Python date object or a string 
                     that specifies one or more dates.
        :raises TypeError: If the provided argument is 
                           neither a date nor a string.
        """
        if isinstance(expr, str):
            self._expr = expr
            self._date = ExpressDateParser.parse(expr)
        elif isinstance(expr, date):
            self._expr = expr.strftime("%m-%d-%Y")
            self._date = (expr,)
        else:
            raise TypeError("Invalid type.")

    def __hash__(self) -> int:
        """
        Returns the hash of the internal dates.
        The hash is computed based on the tuple of 
        date objects stored in this instance.

        :return: An integer hash value.
        """
        return hash(self._date)

    def __str__(self) -> str:
        """
        Returns the original string expression 
        that was used to create this instance,
        or a string representation of the single date 
        if it was created from a Python date.

        :return: The date expression as a string.
        """
        return self._expr

    def __repr__(self) -> str:
        """
        Returns an official string representation of 
        the ExpressDate object for debugging.

        :return: A string in the form ExpressDate('MM-DD-YYYY') 
                 or an equivalent expression.
        """
        return f"ExpressDate('{self._expr}')"
    
    def __len__(self) -> int:
        """
        Provides the total number of date objects stored in this instance.

        :return: An integer representing how many distinct dates are stored.
        """
        return len(self._date)
    
    def __iter__(self) -> Iterator[date]:
        """
        Returns an iterator over the internal tuple of date objects.
    
        :return: An iterator over the date objects stored in this instance.
        """
        return iter(self._date)

    def __add__(self, other: timedelta | int) -> tuple[date, ...]:
        """
        Adds a timedelta or an integer number of 
        days to each date in this ExpressDate.

        :param other: A timedelta object or 
                      an integer representing the number of days.
        :return: A tuple of date objects resulting from the addition.
        """
        if isinstance(other, int):
            other = timedelta(days=other)
        return tuple(i + other for i in self._date)

    def __radd__(self, other: timedelta) -> tuple[date, ...]:
        """
        Reflects addition so that timedelta + ExpressDate is possible.

        :param other: A timedelta object.
        :return: A tuple of date objects resulting from the addition.
        """
        return self.__add__(other)

    def __sub__(self, other: ExpressDate | tuple[date, ...] | str) -> tuple[date, ...]:
        """
        Subtracts another ExpressDate object or 
        a tuple of dates from this instance.
        If a string is provided, it is parsed to create an ExpressDate first.

        :param other: Another ExpressDate, a tuple of date objects, or a string.
        :return: A tuple of date objects that remain after the subtraction.
        """
        if isinstance(other, ExpressDate):
            return tuple(sorted(set(self._date) - set(other.dates)))
        elif isinstance(other, tuple):
            return tuple(sorted(set(self._date) - set(other)))
        return tuple(sorted(set(self._date) - set(ExpressDate(other).dates)))

    def __rsub__(self, other: tuple[date, ...] | str) -> tuple[date, ...]:
        """
        Reflects subtraction so that another tuple of dates or 
        a string can subtract this ExpressDate object.

        :param other: A tuple of date objects or a string expression.
        :return: A tuple of date objects that remain after the subtraction.
        """
        if isinstance(other, tuple):
            return tuple(sorted(set(other) - set(self._date)))
        return tuple(sorted(set(ExpressDate(other).dates) - set(self._date)))

    def __eq__(self, other: object) -> bool:
        """
        Checks if this ExpressDate object is equal to another object.
        Equality is determined by comparing the sets of dates.

        :param other: Another ExpressDate, a Python date, or a string.
        :return: True if they represent the same set of dates, otherwise False.
        """
        if isinstance(other, ExpressDate):
            return hash(self) == hash(other)
        elif isinstance(other, date):
            return self._date == (other,)
        elif isinstance(other, str):
            return hash(self) == hash(ExpressDate(other))
        return False

    def __ne__(self, other: object) -> bool:
        """
        Checks if this ExpressDate object is not equal to another object.

        :param other: Another ExpressDate, a Python date, or a string.
        :return: True if they do not represent the same set of dates, 
                 otherwise False.
        """
        return not self.__eq__(other)

    def __or__(self, other: ExpressDate | tuple[date, ...] | str) -> tuple[date, ...]:
        """
        Performs a union (OR) operation.
        Merges all unique dates from both objects.

        :param other: Another ExpressDate, a tuple of dates, 
                      or a string expression.
        :return: A tuple containing all unique dates from both.
        """
        if isinstance(other, ExpressDate):
            return tuple(sorted(set(self._date) | set(other._date)))
        elif isinstance(other, tuple):
            return tuple(sorted(set(self._date) | set(other)))
        return tuple(sorted(set(self._date) | set(ExpressDate(other).dates)))

    def __ror__(self, other: tuple[date, ...] | str) -> tuple[date, ...]:
        """
        Reflects the union operation so that a tuple of dates or a string
        can be placed on the left side of the OR operator.

        :param other: A tuple of dates or a string expression.
        :return: A tuple containing all unique dates from both.
        """
        return self.__or__(other)

    def __and__(self, other: ExpressDate | tuple[date, ...] | str) -> tuple[date, ...]:
        """
        Performs an intersection (AND) operation.
        Finds dates common to both objects.

        :param other: Another ExpressDate, a tuple of dates,
                      or a string expression.
        :return: A tuple of dates that appear in both sets.
        """
        if isinstance(other, ExpressDate):
            return tuple(sorted(set(self._date) & set(other._date)))
        elif isinstance(other, tuple):
            return tuple(sorted(set(self._date) & set(other)))
        return tuple(sorted(set(self._date) & set(ExpressDate(other).dates)))

    def __rand__(self, other: tuple[date, ...] | str) -> tuple[date, ...]:
        """
        Reflects the intersection operation so that a tuple of dates or a string
        can be placed on the left side of the AND operator.

        :param other: A tuple of dates or a string expression.
        :return: A tuple of dates that appear in both sets.
        """
        return self.__and__(other)

    def __xor__(self, other: ExpressDate | tuple[date, ...] | str) -> tuple[date, ...]:
        """
        Performs a symmetric difference (XOR) operation.
        Returns dates that are in either object but not in both.

        :param other: Another ExpressDate, a tuple of dates, 
                      or a string expression.
        :return: A tuple containing the symmetric difference of 
                 the two sets of dates.
        """
        if isinstance(other, ExpressDate):
            return tuple(sorted(set(self._date) ^ set(other._date)))
        elif isinstance(other, tuple):
            return tuple(sorted(set(self._date) ^ set(other)))
        return tuple(sorted(set(self._date) ^ set(ExpressDate(other).dates)))

    def __rxor__(self, other: tuple[date, ...] | str) -> tuple[date, ...]:
        """
        Reflects the symmetric difference operation so that a tuple of dates
        or a string can be placed on the left side of the XOR operator.

        :param other: A tuple of dates or a string expression.
        :return: A tuple containing the symmetric difference of 
                 the two sets of dates.
        """
        return self.__xor__(other)

    def __contains__(self, other: ExpressDate | date | str) -> bool:
        """
        Checks whether a given single-day ExpressDate, Python date, or string
        is contained within this ExpressDate.

        :param other: A single-day ExpressDate, a Python date, or a string.
        :return: True if it is contained, False otherwise.
        :raises ValueError: If the other ExpressDate object 
                            represents more than one day.
        :raises TypeError: If the argument is not an ExpressDate, 
                           a date, or a string.
        """
        if isinstance(other, ExpressDate):
            if not other.is_single_day:
                raise ValueError("ExpressDate object must represent a single day.")
            return other.first in self._date
        elif isinstance(other, date):
            return other in self._date
        elif isinstance(other, str):
            return ExpressDateParser.parse_const_date(other) in self._date
        raise TypeError("Invalid type.")

    def __matmul__(self, other: ExpressDate | date | str) -> ExpressDate:
        """
        Uses the @ operator to combine two single-day ExpressDate objects 
        (or one ExpressDate and a single Python date) into a new ExpressDate 
        that represents a range in the form 'MM-DD-YYYY ~ MM-DD-YYYY'.

        :param other: Another single-day ExpressDate, 
                      a Python date, or a string.
        :return: A new ExpressDate object representing the resulting date range.
        :raises ValueError: If either ExpressDate represents more than one day.
        """
        if not self.is_single_day:
            raise ValueError("ExpressDate object must represent a single day.")
        if isinstance(other, ExpressDate):
            if not other.is_single_day:
                raise ValueError("ExpressDate object must represent a single day.")
            other = other.first
        elif isinstance(other, str):
            other = ExpressDateParser.parse_const_date(other)
        left = self.first.strftime("%m-%d-%Y")
        right = other.strftime("%m-%d-%Y")
        return ExpressDate(f"{left} ~ {right}")

    def __rmatmul__(self, other: date | str) -> ExpressDate:
        """
        Reflects the @ operation, allowing a Python date or string on 
        the left side to be combined with this ExpressDate for 
        forming a date range.

        :param other: A single Python date or string expression.
        :return: A new ExpressDate object representing the resulting date range.
        """
        return ExpressDate(other).__matmul__(self)

    @property
    def is_const(self) -> bool:
        """
        Indicates whether the underlying date expression 
        contains no wildcards or ranges.

        :return: True if there are no '*' or '~' characters in the expression, 
                 otherwise False.
        """
        return "*" not in self._expr and "~" not in self._expr

    @property
    def is_single_day(self) -> bool:
        """
        Indicates whether this ExpressDate object represents exactly one date.

        :return: True if the internal tuple contains a single date, 
                 otherwise False.
        """
        return len(self._date) == 1

    @property
    def is_continuous(self) -> bool:
        """
        Checks if all stored dates form a continuous sequence without any gaps.

        :return: True if the dates are consecutive days in ascending order, 
                 otherwise False.
        """
        for i in range(len(self._date) - 1):
            if self._date[i] + timedelta(days=1) != self._date[i + 1]:
                return False
        return True

    @property
    def length(self) -> int:
        """
        Provides the total number of date objects stored in this instance.

        :return: An integer representing how many distinct dates are stored.
        """
        return len(self)

    @property
    def dates(self) -> tuple[date, ...]:
        """
        Retrieves all the stored date objects as a tuple.

        :return: A tuple containing every date in this instance.
        """
        return self._date

    @property
    def first(self) -> date:
        """
        Returns the first (earliest) date in the stored tuple.

        :return: The earliest Python date object.
        """
        return self._date[0]

    @property
    def last(self) -> date:
        """
        Returns the last (latest) date in the stored tuple.

        :return: The latest Python date object.
        """
        return self._date[-1]
