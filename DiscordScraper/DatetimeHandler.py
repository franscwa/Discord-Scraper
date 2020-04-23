from .ErrorHandler import CustomError
from inspect import findsource
from datetime import datetime
from sys import stderr


isLeapYearCheckA = lambda year: (year % 4 == 0) and ((year % 100 == 0) and (year % 400 == 0))
isLeapYearCheckB = lambda year: (year % 4 == 0) and (year % 100 != 0) and (year % 400 != 0)
discordEpoch = 1420070400000


class SnowflakeHandler(object):
    def __init__(self, snowflake):
        self.snowflake = int(snowflake)

    def getTimestamp(self):
        try:
            return (self.snowflake >> 22) + discordEpoch

        except ( TypeError, ValueError ) as e:
            raise CustomError(e, 'DatetimeHandler', findsource(self.getTimestamp)[1], 'getTimestamp', [])

        except CustomError as ce:
            stderr.write(ce.getMessage())


class TimestampHandler(object):
    def __init__(self, timestamp):
        self.timestamp = int(timestamp)

    def getSnowflake(self):
        try:
            return self.timestamp - discordEpoch << 22

        except ( TypeError, ValueError ) as e:
            raise CustomError(e, 'DatetimeHandler', findsource(self.getSnowflake)[1], 'getSnowflake', [])

        except CustomError as ce:
            stderr.write(ce.getMessage())


class DatetimeHandler(object):
    @staticmethod
    def fromSnowflake(snowflake):
        try:
            snowflakeHandler = SnowflakeHandler(snowflake)
            return snowflakeHandler.getTimestamp()

        except ( TypeError, ValueError ) as e:
            raise CustomError(e, 'DatetimeHandler', findsource(DatetimeHandler.fromSnowflake)[1], 'fromSnowflake', [snowflake])

        except CustomError as ce:
            stderr.write(ce.getMessage())

    @staticmethod
    def fromTimestamp(timestamp):
        try:
            timestampHandler = TimestampHandler(timestamp)
            return timestampHandler.getSnowflake()

        except ( TypeError, ValueError ) as e:
            raise CustomError(e, 'DatetimeHandler', findsource(DatetimeHandler.fromTimestamp)[1], 'fromTimestamp', [timestamp])

        except CustomError as ce:
            stderr.write(ce.getMessage())

    @staticmethod
    def toDay(timestamp):
        try:
            return datetime.fromtimestamp(timestamp / 1000)

        except ( TypeError, ValueError ) as e:
            raise CustomError(e, 'DatetimeHandler', findsource(DatetimeHandler.toDay)[1], 'toDay', [timestamp])

        except CustomError as ce:
            stderr.write(ce.getMessage())

    @staticmethod
    def fromDay(year, month, day):
        try:
            timeStruct = datetime(year, month, day)
            return timeStruct.timestamp() * 1000

        except ( TypeError, ValueError ) as e:
            raise CustomError(e, 'DatetimeHandler', findsource(DatetimeHandler.fromDay)[1], 'fromDay', [year, month, day])

        except CustomError as ce:
            stderr.write(ce.getMessage())

    @staticmethod
    def getRange(startYear, endYear, endMonth=12):
        try:
            yearRange = {}

            for year in range(endYear, startYear - 1, -1):
                isLeapYear = isLeapYearCheckA(year) or isLeapYearCheckB(year)

                if year == endYear and endMonth < 12:
                    yearRange.update({year: [31, 29 if isLeapYear else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][:endMonth]})
                else:
                    yearRange.update({year: [31, 29 if isLeapYear else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]})

            return yearRange

        except ( TypeError, ValueError ) as e:
            raise CustomError(e, 'DatetimeHandler', findsource(DatetimeHandler.getRange)[1], 'getRange', [startYear, endYear])

        except CustomError as ce:
            stderr.write(ce.getMessage())

    @staticmethod
    def getToday():
        try:
            return datetime.today()

        except ( TypeError, ValueError ) as e:
            raise CustomError(e, 'DatetimeHandler', findsource(DatetimeHandler.getToday)[1], 'getToday', [])

        except CustomError as ce:
            stderr.write(ce.getMessage())
