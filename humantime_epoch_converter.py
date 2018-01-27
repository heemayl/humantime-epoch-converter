#!/usr/bin/env python3

import calendar
import datetime
import itertools
import re
import sys
import time


def print_msg(msg):
    print('\n{}\n'.format(msg))
    return


class DateTimeException(Exception):
    '''Custom exception.'''
    pass


class DateTime:
    '''Takes any human datetime specifier string, converts
    to Python datetime object and converts into Epoch.
    '''
    def __init__(self, str_dt):
        self.str_dt = str_dt.lower().strip().strip(':')

    def _has_next(self, _input_dt_str):
        _input_dt_list = _input_dt_str.split()
        if _input_dt_list[0] != 'next' or len(_input_dt_list) < 2:
            raise DateTimeException('Ambiguous input')
        day_ = _input_dt_list[1]
        # Only `day` at idx 2 means tomorrow
        if day_ == 'day':
            return self._yestr_today_tmrw('tomorrow {}'.format(
                ' '.join(_input_dt_list[2:]), 'tomorrow'))
        day_map = {
            frozenset(('sat', 'satur', 'saturday')): calendar.SATURDAY,
            frozenset(('sun', 'sunday')): calendar.SUNDAY,
            frozenset(('mon', 'monday')): calendar.MONDAY,
            frozenset(('tue', 'tues', 'tuesday')): calendar.TUESDAY,
            frozenset(('wed', 'wednes', 'wednesday')): calendar.WEDNESDAY,
            frozenset(('thu', 'thurs', 'thursday')): calendar.THURSDAY,
            frozenset(('fri', 'friday')): calendar.FRIDAY,
        }
        # Getting the day number
        for key, val in day_map.items():
            if day_ in key:
                day_num = val
                break
            
        def _get_days_to_go(day_num):
            '''Returns the day to go if the `day_num`
            is behind today's weekday.
            '''
            cycle_ = itertools.cycle((0, 1, 2, 3, 4, 5, 6))
            today_wday = time.localtime().tm_wday
            while True:
                if today_wday == next(cycle_):
                    break
            days = 1
            while True:
                if day_num != next(cycle_):
                    days += 1
                    continue
                break
            return days

        # Days to go
        after = _get_days_to_go(day_num) if time.localtime().tm_wday >= \
                day_num else day_num - time.localtime().tm_wday
        # Getting the YY, mm, dd
        target_ymd = (datetime.datetime.now() +
                      datetime.timedelta(days=after)).timetuple()[:3]
        target_hms = list(self._hour_min_sec(_input_dt_str))
        return self._mktime(
            tm_year=target_ymd[0],
            tm_mon=target_ymd[1],
            tm_mday=target_ymd[2],
            tm_hour=target_hms[0],
            tm_min=target_hms[1],
            tm_sec=target_hms[2]
        )
        
    def check_get(self):
        '''Method to call from instance.'''
        return self._check_format()
        
    def get_epoch_now(self):
        '''Returns the current time in Epoch.'''
        return int(time.mktime(time.localtime()))
    
    def _mktime(self, tm_year=None, tm_mon=None, tm_mday=None,
                tm_hour=None, tm_min=None, tm_sec=None, *_):
        '''Takes specifications, returns Epoch using `time.mktime`.'''
        today_ = time.localtime()
        return int(time.mktime(time.strptime('{}-{}-{}_{}:{}:{}'.format(
            tm_year or today_.tm_year,
            tm_mon or today_.tm_mon,
            tm_mday or today_.tm_mday,
            tm_hour or today_.tm_hour,
            tm_min or today_.tm_min,
            tm_sec or today_.tm_sec
            ),
            '%Y-%m-%d_%H:%M:%S'
        )))

    def _gen_iter(self, iter_, newlen, fillval='00'):
        '''Returns an iterator with the iter_ filled
        with fillval upto newlen.
        '''
        new_iter = itertools.chain(iter_, itertools.cycle((fillval,)))
        return itertools.islice(new_iter, newlen)
        
    def _check_format(self):
        '''Checks the formatting and calls the
        appropriate method.
        '''
        # fmt_method_map = {
        #     'add_sub': self.add_sub,
        #     'tomorrow': self.tomorrow,
        #     'today': self.today,
        # }
        if self.str_dt == 'now':
            return self._mktime(*time.localtime())
        elif 'next' in self.str_dt:
            return self._has_next(self.str_dt)
        elif '+' in self.str_dt or '-' in self.str_dt:
            return self._add_sub()
        elif 'yesterday' in self.str_dt:
            return self._yestr_today_tmrw(self.str_dt, day_='yesterday')
        elif 'today' in self.str_dt:
            return self._yestr_today_tmrw(self.str_dt, day_='today')
        elif 'tomorrow' in self.str_dt:
            return self._yestr_today_tmrw(self.str_dt, day_='tomorrow')

    def _hour_min_sec(self, in_str):
        '''Getting a string datetime and returning
        the desired HH, MM, SS as iterator.
        '''
        hms_str = re.sub(r'^[a-z]+(\s+[a-z]+)?(\s+at\s+)?', '', in_str)
        time_ = [i for i in re.split(r'[\s:]+', hms_str) if i]
        return self._gen_iter(time_, 3)
        
    def _yestr_today_tmrw(self, in_str_dt, day_='today'):
        time_ = list(self._hour_min_sec(in_str_dt))
        mday_ = time.localtime().tm_mday
        tm_mday = mday_ if day_ == 'today' else (mday_-1 if
                                                 day_ == 'yesterday'
                                                 else mday_+1)
        return self._mktime(
            tm_mday=tm_mday,
            tm_hour=str(time_[0]),
            tm_min=str(time_[1]),
            tm_sec=str(time_[2])
        )

    def _add_sub(self):
        '''`str_dt` contains `+/-`.'''
        before, after = self.str_dt.split('+') if '+' in self.str_dt else \
                        self.str_dt.split('-')
        self.to_add_sub = self._add_sub_time(after.split())
        return self.get_epoch_now() + self.to_add_sub

    def _add_sub_time(self, after_):
        '''Adds hr/min/sec to time.'''
        hrs = mins = secs = 0
        for val, name in itertools.zip_longest(after_[::2], after_[1::2]):
            if name in {'hrs', 'hr', 'hours', 'hour'}:
                hrs = int(val)
            elif name in {'minutes', 'minute', 'mins', 'min'}:
                mins = int(val)
            elif name in {'seconds', 'second', 'secs', 'sec', None}:
                secs = int(val)
            else:
                raise DateTimeException('Ambiguous input: {}'
                                        .format(self.str_dt_))
        return self._hour_to_sec(hrs) + self._min_to_sec(mins) + secs
                
    def _hour_to_sec(self, hr):
        return hr * 60 * 60

    def _min_to_sec(self, min):
        return min * 60
        

def main(arg):
    '''Base wrapper.'''
    if not isinstance(arg, str):
        print_msg('Argument must be a string')
        return False
    dt = DateTime(arg)
    return dt.check_get()


if __name__ == '__main__':
    if not len(sys.argv) == 2:
        print('There must be exactly one argument as string')
        exit(2)
    arg = sys.argv[1]
    out = main(arg)
    if not out:
        exit(1)
    print_msg(out)
    exit(0)
