from datetime import datetime, timedelta
from typing import Optional
from dataclasses import dataclass


SECONDS_IN_A_DAY = 24 * 3600

DEFAULT_START_TIME = datetime(year=1990, month=1, day=1)
DEFAULT_END_TIME = datetime.utcnow()
DEFAULT_DATE_STR = '%Y%m%dT%H%M%SZ'
DEFAULT_CYCLE_INTERVALS = [0, 21600, 43200, 64800]

DEFAULT_DATE_RANGE_CONFIG = {
    'datestr': DEFAULT_DATE_STR,
    'start': DEFAULT_START_TIME,
    'end': DEFAULT_END_TIME
}

DEFAULT_OBS_CYCLE_INTERVALS = [0, 3600*6, 3600*12, 3600*18]


def default_datetime_converter(obj):
   if isinstance(obj, datetime):
      return obj.__str__()


def get_datetime_str(value, format_str):
    try:
        formatted_datetime = datetime.strftime(value, format_str)
    except Exception as e:
        msg = f'Invalid time: {value} or format_str: {format_str}' \
              f', error: {e}'
        raise ValueError(msg)

    return formatted_datetime

def is_valid_increment_type(value):
    if not isinstance(value, str) or value not in VALID_INCREMENT_TYPES:
        return False
    return True


def set_datetime(time_str, format_str):
    try:
        time = datetime.strptime(time_str, format_str)
        print(f'in set_datetime - time: {time}, time_str: {time_str}, format_str: {format_str}')
    except Exception as e:
        msg = f'Invalid time str: {time_str} or format string: {format_str}. {e}'
        raise ValueError(msg)

    return time


def get_date_range_from_dict(date_range):
    """
    This method is expecting a dictionary with fields 'start', 'end', and
    'datestr' where 'start' and 'end' are valid datetime strings and
    'datestr' is a format string used to translate 'start' and 'end'
    strings into valid datetime objects.
    If the 'datestr' format string must be valid.
    """
    if not isinstance(date_range, dict):
        msg = f'"date_range" must be a dict type, valid example: ' \
              f'{DEFAULT_DATE_RANGE_CONFIG}, using defaults.'
        raise ValueError(msg)

    datestr = date_range.get('datestr')
    try:
        test_formatted_date = datetime.utcnow().strftime(datestr)
    except Exception as e:
        msg = f'Invalid date format string: {date_range}, valid example: ' \
              f'{DEFAULT_DATE_STR}, error: {e}'
        raise ValueError(msg)

    raw_start = date_range.get('start')
    raw_end = date_range.get('end')
    start = set_datetime(raw_start, datestr)
    end = set_datetime(raw_end, datestr)

    if start is None:
        start = DEFAULT_START_TIME
        msg = f'Error: invalid start time: {raw_start}, using default: ' \
              f'{DEFAULT_START_TIME}'
        raise ValueError(msg)
    
    if end is None:
        end = DEFAULT_END_TIME 
        msg = f'Error: invalid end time: {raw_end}, using default: ' \
              f'{DEFAULT_END_TIME}'
        raise ValueError(msg)

    print(f'start: {start}, end: {end}')

    if start > end:
        msg = f'Invalid date range: {date_range}, "start" must be older than ' \
              f'"end", valid example: {DEFAULT_DATE_RANGE_CONFIG}'
        raise ValueError(msg)

    
    return DateRange(start, end)



@dataclass
class DateRange:
    start: Optional[datetime] = DEFAULT_START_TIME
    end: Optional[datetime] = DEFAULT_END_TIME
    current: datetime = None


    def __post_init__(self):
        if self.start > self.end:
            msg = f'Invalid date range: "start": {self.start} must older than ' \
                  f'"end": {self.end}.'
            raise ValueError(msg)
        self.current = self.start


    def set_start(self, value):
        if not isinstance(value, datetime):
            msg = f'Invalid time {value} must be a valid datetime object.'
            raise ValueError(msg)

        self.start = value


    def set_end(self, value):
        if not isinstance(value, datetime):
            msg = f'Invalid time {value} must be a valid datetime object.'
            raise ValueError(msg)

        if self.start > value:
            msg = f'Start: {self.start} must be older than end: {value}'
            raise ValueError(msg)

        self.end = value


    def set_current(self, value):
        if not isinstance(value, datetime):
            msg = f'Invalid time {value} must be a valid datetime object.'
            raise ValueError(msg)

        if (self.start > value or self.end < value):
            msg = f'"current": {value} must be older than "end": {self.end} and' \
                  f' newer than start: {self.start}'
            raise ValueError(msg)

        self.current = value


    def increment(
        self,
        days=0,
        seconds=0,
        microseconds=0,
        milliseconds=0,
        minutes=0,
        hours=0,
        weeks=0
    ):

        new_time = self.current

        try:
            new_time += timedelta(
                days,
                seconds,
                microseconds,
                milliseconds,
                minutes,
                hours,
                weeks
            )
        except Exception as e:
            raise ValueError(f'Invalid timedelta: {e}')

        if new_time < self.start:
            self.current = self.start
        elif new_time > self.end:
            self.current = self.end
        else:
            self.current = new_time


    def increment_day(self):    
        self.increment(days=1)


    def at_end(self):
        return self.current == self.end


    def at_start(self):
        return self.current == self.start
        
