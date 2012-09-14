# git-timeclock

A integrated timeclock for git. Based on git tags. By default prints out current time accrued, along with the individual times.

Example output:

    Start: 2012-06-18 01:03:06
    End: 2012-06-18 01:07:25
    Work session: 0 hours, 4 minutes, and 19 seconds
    Start: 2012-06-18 01:17:02
    End: 2012-06-18 02:05:21
    Work session: 0 hours, 48 minutes, and 19 seconds
    ---------
    Totals: 52 minutes and 38 seconds

Gracefully handles multiple starts and stops:

    Start: 2012-06-17 23:35:37
    Start: 2012-06-17 23:35:38
    End: 2012-06-17 23:35:46
    End: 2012-06-17 23:35:47
    End: 2012-06-17 23:36:18
    Work session: 0 hours, 0 minutes, and 40 seconds


Usage:

    git-timeclock [-h] [-s | -e] [-d] [-t TIME] [dir]

    positional arguments:
      dir                   The directory of the git repo

    optional arguments:
      -h, --help            show this help message and exit
      -s, --start           Record a new start tag on top of the current HEAD.
      -e, --end             Record a new end tag.
      -d, --debug           various debug stuffs
      -t TIME, --time TIME  Start counting tags from this date Formatted like:
                            [YYYY-][MM-]DD. The year and the month are optional,
                            but you need to use dashes if you do specify them

