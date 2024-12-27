from datetime import date, datetime, timedelta, tzinfo

__all__ = ["ExpressDateParser"]


class ExpressDateParser:
    """
    A parser class for date expressions that supports 
    single dates, date ranges, and wildcard expressions.
    It can parse both American (MM-DD-YYYY) and CJK (YYYY-MM-DD) style formats,
    handle wildcard characters (*), and optionally filter by weekday.
    """

    @classmethod
    def parse(cls, expr: str, tz: tzinfo | None = None) -> tuple[date, ...]:
        """
        Parse a date or date range expression.

        If no tilde (~) is present, the expression is treated as a single date.
        If a tilde (~) is found, the expression is considered a range, 
        for example:
            "2023-01-01 ~ 2023-01-10"
        In this case, the method will parse both sides and 
        generate all dates within the range.

        :param expr: A string representing a date (with optional wildcards) 
                     or a date range.
        :param tz: An optional timezone, used for determining 'today' 
                   if one side of the range is missing.
        :return: A tuple of date objects parsed from the expression.
        :raises ValueError: If the expression is invalid or 
                            the date range is incorrect.
        """
        # If the expression does not contain a tilde (~), 
        # treat it as a single date.
        if "~" not in expr:
            return cls.parse_date(expr)

        # Handle date range expressions like "2023-01-01 ~ 2023-01-10".
        tilde_pos = expr.find("~")
        left = expr[:tilde_pos].strip()
        right = expr[tilde_pos + 1:].strip()
        today = datetime.now(tz=tz).date()  # Use today's date if needed.

        # If the right side is empty, assume the range ends at 'today'.
        if right == "" and left:
            return cls.parse_date_range(cls.parse_const_date(left), today)

        # If both sides are specified, 
        # parse them and generate the full date range.
        elif left and right:
            return cls.parse_date_range(
                cls.parse_const_date(left),
                cls.parse_const_date(right)
            )

        # Raise an error if the expression is invalid 
        # (e.g., "~something" or "something~" with no data).
        raise ValueError("Invalid date expression.")

    @classmethod
    def parse_date_range(cls, left: date, right: date) -> tuple[date, ...]:
        """
        Generate a list of date objects from the left date 
        to the right date (inclusive).

        :param left: The starting date of the range.
        :param right: The ending date of the range.
        :return: A tuple of date objects covering 
                 the entire range from 'left' to 'right'.
        :raises ValueError: If the left date is greater than the right date.
        """
        if left > right:
            raise ValueError("Invalid date range.")

        dates = []
        current = left
        # Iterate day by day from 'left' up to 'right'.
        while current <= right:
            dates.append(current)
            current += timedelta(days=1)

        return tuple(dates)

    @classmethod
    def parse_date(cls, expr: str) -> tuple[date, ...]:
        """
        Parse a single date expression, 
        which may contain wildcard characters (*).

        :param expr: A string representing a single date or 
                     a wildcard expression (e.g., "2023-*1-01").
        :return: A tuple of date objects.
                 In most cases, this will contain one date,
                 but wildcard expressions can expand 
                into multiple possible dates.
        """
        # If the expression contains a wildcard (*), 
        # treat it as an expression date that needs expansion.
        if "*" in expr:
            return cls.parse_expr_date(expr)

        # Otherwise, parse it as a constant (exact) date.
        return (cls.parse_const_date(expr),)

    @classmethod
    def parse_expr_date(cls, expr: str) -> tuple[date, ...]:
        """
        Parse a date expression containing wildcard characters (*). 
        The wildcard can appear in different parts of the date 
        (year, month, day), and this method will attempt to generate 
        all valid possibilities.

        :param expr: A string representing a date expression 
                     with one or more '*' characters.
        :return: A tuple of date objects that match the wildcard expression.
        :raises ValueError: If the expression leads to 
                            an invalid date (e.g., out of range).
        """
        # Convert American format (MM-DD-YYYY) to 
        # CJK format (YYYY-MM-DD) if needed.
        expr = cls.convert_to_cjk_style(expr)

        # Initialize 'week' to None; it may be updated 
        # if a weekday is specified (e.g., "mon", "tue").
        week = None

        # Check if there's a comma indicating 
        # a weekday filter (e.g., "2023-01-01, mon").
        if (comma_pos := expr.find(",")) != -1:
            expr, week = expr[:comma_pos], expr[comma_pos + 1:].strip().lower()

        dates = []

        # Search for asterisks (*) in the expression and handle them one by one.
        i = -1
        while (i := expr.find("*", i + 1)) != -1:
            # Handle wildcard in the year portion (positions 0~3).
            if 0 <= i < 3:
                # Replace '*' with digits 0~9 to 
                # generate all possible year values.
                for digit in range(0, 10):
                    dates.extend(cls.parse_date(expr.replace("*", str(digit), 1)))
                break
            if i == 3:
                # If the wildcard is the last digit of the year (e.g., "202*"),
                # replace it with digits 0~9. Skip "0000" year if it appears.
                for digit in range(0 + (expr[:3] == "000"), 10):
                    dates.extend(cls.parse_date(expr.replace("*", str(digit), 1)))
                break

            # By this point, the year is fully specified.
            year = int(expr[:4])
            # Check if it is a leap year.
            is_leap = (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)

            # Handle wildcard in the month portion (positions 5~6).
            if i == 5:
                # If the wildcard is the tens digit of the month, 
                # it can be '0' or '1' in most cases.
                is_zero = (expr[6] == "0")
                for digit in range(0 + is_zero, 2):
                    dates.extend(cls.parse_date(expr.replace("*", str(digit), 1)))
                break
            if i == 6:
                # If the wildcard is the ones digit of the month 
                # (e.g., "2023-0*-DD"),
                # handle potential 10, 11, 12 if the tens digit is '1'.
                is_over_ten = (expr[5] == "1")
                for digit in range(1 - is_over_ten, 3 if is_over_ten else 10):
                    dates.extend(cls.parse_date(expr.replace("*", str(digit), 1)))
                break

            # At this point, the month is fully specified.
            month = int(expr[5:7])
            is_feb = (month == 2)

            # Handle wildcard in the day portion (positions 8~9).
            if i == 8:
                # If the wildcard is the tens digit of 
                # the day (e.g., "2023-01-*1"),
                # consider the possible range for the tens digit 
                # (0~3 depending on month and leap year).
                is_zero = (expr[9] == "0")
                is_over_eight = (expr[9] not in "*0" and expr[9] > "8")
                start = 0 + is_zero
                # If the ones digit is over '8' and 
                # it's a leap year in Feb, adjust the range.
                end = 3 - (is_over_eight and is_leap) if is_feb else 4 - is_zero
                for digit in range(start, end):
                    dates.extend(cls.parse_date(expr.replace("*", str(digit), 1)))
                break
            if i == 9:
                # If the wildcard is the ones digit of the day 
                # (e.g., "2023-01-1*"),
                # handle the maximum valid day based on the month.
                days_in_month = [2, 9 + is_leap, 2, 1, 2, 1, 2, 2, 1, 2, 1, 2]
                tens_digit = int(expr[8])
                start = 0 + (tens_digit == 0)

                if is_feb:
                    # If it's February, check for 29 in 
                    # leap years if tens_digit=2.
                    end = 10 if tens_digit != 2 else days_in_month[1]
                else:
                    # For other months, if tens_digit=3, 
                    # we handle 30 or 31 accordingly.
                    end = 10 if tens_digit != 3 else days_in_month[month - 1]

                for digit in range(start, end):
                    dates.append(cls.parse_const_date(expr.replace("*", str(digit), 1)))
                break

        # If a weekday was specified, filter the generated dates accordingly.
        if week:
            weekday_map = {
                "mon": 0,
                "tue": 1,
                "wed": 2,
                "thu": 3,
                "fri": 4,
                "sat": 5,
                "sun": 6,
            }
            weekday_val = weekday_map[week]
            return tuple(d for d in dates if d.weekday() == weekday_val)

        # Return the expanded dates if no weekday filtering is required.
        return tuple(dates)

    @classmethod
    def parse_const_date(cls, expr: str) -> date:
        """
        Parse a constant (exact) date expression in CJK format (YYYY-MM-DD).

        If the expression is in American format (MM-DD-YYYY), 
        it will be converted to CJK format before parsing. 
        This method does not handle wildcard characters.

        :param expr: A string representing a date 
                     in either MM-DD-YYYY or YYYY-MM-DD format.
        :return: A date object corresponding to the expression.
        :raises ValueError: If the expression does not represent a valid date.
        """
        return datetime.strptime(cls.convert_to_cjk_style(expr), "%Y-%m-%d").date()

    @staticmethod
    def convert_to_cjk_style(expr: str) -> str:
        """
        Convert a date expression from American (MM-DD-YYYY) 
        to CJK (YYYY-MM-DD) style if needed.

        :param expr: A string representing a date 
                     in either MM-DD-YYYY or YYYY-MM-DD format.
        :return: A string representing the date in CJK (YYYY-MM-DD) format.
        """
        # Check if the expression is already in CJK style 
        # (detect if the first dash is after the fourth character).
        is_cjk_style = (expr.find("-") == 4)
        if not is_cjk_style:
            # Convert if in American format, 
            # assuming positions for month/day/year.
            return f"{expr[6:]}-{expr[:2]}-{expr[3:5]}"
        return expr
