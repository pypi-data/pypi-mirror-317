from .date import ExpressDate
from .parse import ExpressDateParser
from datetime import date

__all__ = ["express", "expr", "ExpressDate", "ExpressDateParser"]


def express(e: date | str) -> ExpressDate:
    """
    Creates and returns a new ExpressDate object 
    from the provided date or string.

    :param e: A Python date object or a string specifying one or more dates.
    :return: An ExpressDate instance representing the parsed date(s).
    """
    return ExpressDate(e)


def expr(e: date | str) -> ExpressDate:
    """
    Creates and returns a new ExpressDate object 
    from the provided date or string.

    :param e: A Python date object or a string specifying one or more dates.
    :return: An ExpressDate instance representing the parsed date(s).
    """
    return express(e)
