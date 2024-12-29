import threading
from timer1101.timer import Timer


def singletondecorate(cls):
    _instance = None
    _lock = threading.Lock()

    def getinstance():
        nonlocal _instance
        if _instance is None:
            with _lock:
                if _instance is None:
                    _instance = cls()
        return _instance

    return getinstance


@singletondecorate
class TimerManager:
    _creat_timer_lock = threading.Lock()
    timerdict = {}

    def getTimer(self, name, *args, **kwargs) -> Timer:
        if name not in self.timerdict:
            with self._creat_timer_lock:
                if name not in self.timerdict:
                    self.timerdict[name] = Timer(name, *args, **kwargs)
        return self.timerdict[name]
