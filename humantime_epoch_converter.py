#!/usr/bin/env python3

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
        self.str_dt_ = str_dt
        self.str_dt = self.str_dt_.strip().strip(':').lower()

    def check_get(self):
        '''Method to call from instance.'''
        return self._check_format()
        
    def get_epoch_now(self):
        '''Returns the current time in Epoch.'''
        return int(time.mktime(time.localtime()))
    
    def _mktime(self, tm_year=None, tm_mon=None, tm_mday=None,
                tm_hour=None, tm_min=None, tm_sec=None):
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
        if '+' in self.str_dt or '-' in self.str_dt:
            return self._add_sub()
        elif 'yesterday' in self.str_dt:
            return self._yestr_today_tmrw(self.str_dt, day_='yesterday')
        elif 'today' in self.str_dt:
            return self._yestr_today_tmrw(self.str_dt, day_='today')
        elif 'tomorrow' in self.str_dt:
            return self._yestr_today_tmrw(self.str_dt, day_='tomorrow')
        
    def _yestr_today_tmrw(self, in_str_dt, day_='today'):
        time_ = re.split(r'[\s:]+', in_str_dt)
        try:
            time_.remove('at')
        except ValueError:
            pass
        time_ = list(self._gen_iter(time_, 4))
        mday_ = time.localtime().tm_mday
        tm_mday = mday_ if day_ == 'today' else (mday_-1 if
                                                 day_ == 'yesterday'
                                                 else mday_+1)
        return self._mktime(
            tm_mday=tm_mday,
            tm_hour=str(time_[1]),
            tm_min=str(time_[2]),
            tm_sec=str(time_[3])
        )

    def _tomorrow(self):
        pass
        
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
