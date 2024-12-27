from timer1101.timer import Timer


timerdict = {}


def getTimer(name, **kwarg) -> Timer:
    if name not in timerdict:
        timerdict[name] = Timer(name, **kwarg)
    return timerdict[name]


rootTimer = getTimer("root")
starte = rootTimer.starte
stope = rootTimer.stope
