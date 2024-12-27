from datetime import UTC, timedelta
from datetime import datetime, tzinfo


class ExpiryTime:
    def __init__(self, expiryTime: int = None, date: datetime = None, tz: tzinfo = None):
        """
        Use one of these expiryTime, date to initialize

        :param expiryTime: number of milliseconds from epoch
        :param tz: timezone
        """
        self.__tz = tz
        if expiryTime is not None and date is not None:
            raise ValueError("Cannot initialize with two parameters")

        if expiryTime is not None:
            self.__expiry_time = expiryTime
            self.__date = self.convert_expiryTime(expiryTime, tz if tz else UTC)
        if date is not None:
            self.__date = date
            if date.tzinfo != tz:
                raise ValueError("Timezone does not match with date timezone")
            self.__expiry_time = self.convert_datetime(date, tz if tz else date.tzinfo)

        if expiryTime is None and date is None:
            raise ValueError("Cannot initialize with no parameters")



    @staticmethod
    def convert_datetime(date: datetime, tz: tzinfo) -> int:
        """

        :param date: datetime
        :param tz: timezone
        :return: number of milliseconds from epoch
        """
        epoch = datetime.fromtimestamp(0, tz=tz)
        return round((date - epoch).total_seconds() * 1000)
    @staticmethod
    def convert_expiryTime(expiryTime: int, tz: tzinfo) -> datetime:
        """

        :param expiryTime: number of milliseconds from epoch
        :param tz: timezone
        :return: datetime
        """
        timestamp = expiryTime / 1000
        return datetime.fromtimestamp(timestamp, tz=tz)

    def __str__(self):
        return self.date.__str__()

    def strftime(self, format: str) -> str:
        """
        Format using strftime().

        Example: "%d/%m/%Y, %H:%M:%S"
        """
        return self.__date.strftime(format)

    @property
    def expiryTime(self):
        return self.__expiry_time

    @expiryTime.setter
    def expiryTime(self, expiryTime: int):
        self.__expiry_time = expiryTime
        self.__date = self.convert_expiryTime(expiryTime, self.__tz)

    @property
    def date(self):
        return self.__date

    @date.setter
    def date(self, date: datetime):
        self.__date = date
        self.__expiry_time = self.convert_datetime(date, self.__tz)

    @property
    def tz(self):
        return self.__tz

    @tz.setter
    def tz(self, tz: tzinfo):
        self.__tz = tz
        self.__date = self.convert_expiryTime(self.__expiry_time, tz)

    def __add__(self, other):
        if isinstance(other, timedelta):
            self.date += other
        if isinstance(other, int):
            self.expiryTime += other
        return self

    def __sub__(self, other):
        if isinstance(other, timedelta):
            self.date -= other
        if isinstance(other, int):
            self.expiryTime -= other
        return self