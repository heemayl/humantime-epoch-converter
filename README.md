## `humantime-epoch-converter` is a Python library for converting the *human datetime specifications* into Epoch (seconds since 1st January, 1970).

Some examples of the supported input datetime specifications (**all specifications are case-insensitive**):

- `yesterday` (assumed `yesterday at 00:00:00`)

- `today at 7:30 PM`

- `now + 7 hours 30 minutes`

- `tomorrow 8`

- `today 14:45:04`

- `next sunday` (assumed `next sunday 00:00:00`)

- `next wed - 1 hr 30 mins 42 seconds`

- `today at 5:05 - 1 hour 40 seconds`


### I would suggest you to try and find out for any supported formats. Feel free to request missing one(s), which is(are) expected to be supported.

---

Here are some examples of running the `run_humantime_epoch_converter.py` wrapper script directly from shell:


```bash

$ ./run_humantime_epoch_converter.py

There must be exactly one argument -- a datetime string. See the `humantime_epoch_converter` library module's docstring for details.


$ ./run_humantime_epoch_converter.py yesterday

1517162400


$ ./run_humantime_epoch_converter.py 'today at 6:50'

1517273400


$ ./run_humantime_epoch_converter.py 'tomorrow 16:40 + 2 hr'

1517402400


$ ./run_humantime_epoch_converter.py 'next sunday 23'

1517763600


$ ./run_humantime_epoch_converter.py 'next sunday at 23'

1517763600


$ ./run_humantime_epoch_converter.py 'next wed at 2:30 + 48 minutes 21 secs'

1517347101


$ ./run_humantime_epoch_converter.py 'now'

1517311409


$ ./run_humantime_epoch_converter.py 'now + 1 hr 2 min 3 sec'

1517315150

```

