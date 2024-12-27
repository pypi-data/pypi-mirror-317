import functools
from timer1101.timer import Timer
import rs1101.random_string as rs


timerdict = {}


def getTimer(name, **kwargs) -> Timer:
    if name not in timerdict:
        timerdict[name] = Timer(name, **kwargs)
    return timerdict[name]


rootTimer = getTimer("root")
starte = rootTimer.starte
stope = rootTimer.stope


def timefunc(timer: Timer = None, id_length=20):
    if timer is None:
        timer = rootTimer

    def decorate(func):
        @functools.wraps(func)
        def newfunc(*args, **kwargs):
            randomid = rs.random_string(id_length)
            event = f"{func.__name__=},  {randomid=}"
            timer.starte(event)
            ret = func(*args, **kwargs)
            timer.stope(event)
            return ret

        return newfunc

    return decorate
