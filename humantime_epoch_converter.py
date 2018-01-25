#!/usr/bin/env python3

import datetime
import itertools
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
        self.str_dt = self.str_dt_.strip().lower()  # strip-lowercasing

    def check_get(self):
        '''Method to call from instance.'''
        return self._check_format()
        
    def get_epoch_now(self):
        '''Returns the current time in Epoch.'''
        return int(time.mktime(time.localtime()))

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
            return self.add_sub()
        elif 'today' in self.str_dt:
            return self.get_epoch_now()
        
    def add_sub(self):
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
