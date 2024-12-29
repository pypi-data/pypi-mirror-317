import functools
import rs1101.random_string as rs
from timer1101.timer import Timer
from timer1101.timerManager import TimerManager



tm = TimerManager()
rootTimer = tm.getTimer("root")


def timefunc(timer: Timer = None, id_length=20):
    if timer is None:
        timer = rootTimer

    def decorate(func):
        @functools.wraps(func)
        def newfunc(*args, **kwargs):
            randomid = rs.random_string(id_length)
            event = f"{func.__name__=}:{randomid=}"
            timer.starte(event)
            ret = func(*args, **kwargs)
            timer.stope(event)
            return ret

        return newfunc

    return decorate
