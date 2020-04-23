from .ErrorHandler import *
from datetime import datetime
from sys import stderr
from os import path

# Determine if our target year is a leap year or not. Requires the function below for full accuracy.
isLeapYearCheckA = lambda year: (year % 4 == 0) and ((year % 100 == 0) and (year % 400 == 0))

# Determine if our target year is a leap year or not. Requires the function above for full accuracy.
isLeapYearCheckB = lambda year: (year % 4 == 0) and (year % 100 != 0) and (year % 400 != 0)

# Determine if our target year is a leap year or not. This combines the outputs of the above functions.
isLeapYearCheck = lambda year: isLeapYearCheckA(year) and isLeapYearCheckB(year)

# Determine if we're dealing with future dates or not.
futureCheck = lambda year, month, day: (DatetimeHandler.getToday() == year) and (DatetimeHandler.getToday().month == month) and (DatetimeHandler.getToday().day + 1 < day)

# The Discord epoch which is set to January 1, 2015.
discordEpoch = 1420070400000

# Set our filename for all of our exceptions to use.
fileName = path.basename(__file__)


class SnowflakeHandler(object):
    def __init__(self, snowflake):
        self.snowflake = int(snowflake)  # We need our value to be an integer in order to perform bitwise operations.

    def getTimestamp(self):
        """
        Convert a timestamp into a snowflake.

        :return:
        """

        try:

            # Shift the value of our snowflake to the right by 22 bits, this removes 22 bits of data from the snowflake.
            timestamp = self.snowflake >> 22

            # Return the shifted snowflake with the Discord epoch added onto it to create our timestamp.
            return timestamp + discordEpoch

        except Exception as ex:
            message = f'Unable to convert {self.snowflake} to a valid timestamp.\n'
            raise RuntimeException('getTimestamp', fileName, lineNumber(self.getTimestamp), message) from ex

        except RuntimeException as rex:
            stderr.write(rex.getMessage())


class TimestampHandler(object):
    def __init__(self, timestamp):
        self.timestamp = int(timestamp)  # We need our value to be an integer in order to perform bitwise operations.

    def getSnowflake(self):
        """
        Convert a snowflake into a timestamp.

        :return:
        """

        try:

            # Subtract the Discord epoch from our timestamp to create our unshifted snowflake.
            snowflake = self.timestamp - discordEpoch

            # Shift the value of our unshifted snowflake to the left by 22 bits, this creates our snowflake.
            return snowflake << 22

        except Exception as ex:
            message = f'Unable to convert {self.timestamp} to a valid snowflake.\n'
            raise RuntimeException('getSnowflake', fileName, lineNumber(self.getSnowflake), message) from ex

        except RuntimeException as rex:
            stderr.write(rex.getMessage())


class DatetimeHandler(object):
    @staticmethod
    def fromSnowflake(snowflake):
        """
        Gather a timestamp from a snowflake without importing a new class. Even though I could just combine everything.

        :param snowflake: The snowflake we're wanting to convert to a timestamp.
        :return:
        """

        # Call our getTimestamp function from the SnowflakeHandler class in a single line.
        return SnowflakeHandler(snowflake).getTimestamp()

    @staticmethod
    def fromTimestamp(timestamp):
        """
        Gather a snowflake from a timestamp in the same manner as seen above.

        :param timestamp: The timestamp we're wanting to convert to a snowflake.
        :return:
        """

        # Call our getSnowflake function from the TimestampHandler class in a single line.
        return TimestampHandler(timestamp).getSnowflake()

    @staticmethod
    def toDay(timestamp):
        """
        Get the year, month, and date from a timestamp.

        :param timestamp: The timestamp we're wanting to break down.
        :return:
        """

        try:

            # Since Discord deals in timestamps that include the milliseconds, we must divide it by 1000 to function.
            return datetime.fromtimestamp(timestamp / 1000)

        except Exception as ex:
            message = f'Unable to convert {timestamp} into a valid datetime object.\n'
            raise RuntimeException('toDay', fileName, lineNumber(DatetimeHandler.toDay), message) from ex

        except RuntimeException as rex:
            stderr.write(rex.getMessage())

    @staticmethod
    def fromDay(year, month, day):
        """
        Create a timestamp from a datetime object.

        :param year: The year in YYYY formatting.
        :param month: The month in M(M) formatting. (No trailing zeroes)
        :param day: The day in D(D) formatting. (No trailing zeroes)
        :return:
        """

        try:

            # Convert our datetime object into a timestamp and then incorporate the milliseconds (0) to the timestamp.
            return datetime(year, month, day).timestamp() * 1000

        except Exception as ex:
            message = f'Unable to convert {year}-{month}-{day} to a valid timestamp.\n'
            raise RuntimeException('fromDay', fileName, lineNumber(DatetimeHandler.fromDay), message) from ex

        except RuntimeException as rex:
            stderr.write(rex.getMessage())

    @staticmethod
    def getRange(startYear, endYear, endMonth=12):
        """
        Get all of the months and their appropriate number of days based on the given years.

        :param startYear: The earliest year that we want to grab calendar dates from.
        :param endYear: The latest year that we want to grab calendar dates from.
        :param endMonth: The lastest month of the latest year to minimize the amount of data we have to work with.
        :return:
        """

        try:

            # Create an empty dictionary to store the year alongside the calendar dates associated with it.
            yearRange = {}

            # Iterate through all of the years that were given.
            for year in range(endYear, startYear - 1, -1):

                # Determine if the current year is a leap year. If so then February will have 29 days instead of 28.
                February = 29 if isLeapYearCheck(year) else 28

                # Generate an array to store our calendar dates.
                calendarDates = [31, February, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

                # Determine if this is the latest year and if the latest month is earlier than December.
                if year == endYear and endMonth < 12:

                    # Update our year range dictionary to store the calendar dates for this year up to this month.
                    yearRange.update({year: calendarDates[:endMonth]})

                else:

                    # Update our year range dictionary to store the calendar dates for the given year.
                    yearRange.update({year: calendarDates})

            # Return our updated year range dictionary with all of our years and calendar dates.
            return yearRange

        except Exception as ex:
            message = f'Unable to generate the calendar dates between {endYear}-{endMonth} and {startYear}-1'
            raise RuntimeException('getRange', fileName, lineNumber(DatetimeHandler.getRange), message) from ex

        except RuntimeException as rex:
            stderr.write(rex.getMessage())

    @staticmethod
    def getToday():
        """
        Return the datetime struct from the current date.

        :return:
        """

        return datetime.today()
