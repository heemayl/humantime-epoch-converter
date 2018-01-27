#!/usr/bin/env python3

# Wrapper script to call to leverage the `humantime_epoch_converter`
# library directly from command line. Takes one argument -- the datetime
# string, and returns the Epoch using the library.
# See the `humantime_epoch_converter` module's docstring for details.

import sys

from lib.humantime_epoch_converter import main, print_msg


if not len(sys.argv) == 2:
    print_msg(("There must be exactly one argument -- a datetime string. "
               "See the `humantime_epoch_converter` library module's "
               "docstring for details."
    ))
    exit(2)
arg = sys.argv[1]
out = main(arg)
if not out:
    exit(1)
print_msg(out)
exit(0)
