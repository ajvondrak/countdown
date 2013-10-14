"""Uses Unix signals to time out blocks of code using the pattern

    start()
    try:
        [... your code here ...]
    except TimeIsUp:
        [... clean up response here ...]
    finally:
        reset()
"""

import signal
import time

__all__ = ['start', 'TimeIsUp', 'reset', 'profile']

class TimeIsUp(Exception):
    """This exception is raised if the alarm started by `start()` times out."""

def time_is_up(signum, frame):
    raise TimeIsUp()

def start():
    """Start a 30 second alarm that raises `TimeIsUp` at the end."""
    signal.signal(signal.SIGALRM, time_is_up)
    signal.alarm(30)

def reset():
    """Reset the alarm started by `start()`."""
    signal.alarm(0)

def profile(f, *args):
    """
    Call `f(*args)`, returning a tuple of `(t, r)` where `t` is the number of
    seconds the call took to complete and `r` is the function call's return
    value.
    """
    start = time.time()
    ret = f(*args)
    end = time.time()
    return end - start, ret
