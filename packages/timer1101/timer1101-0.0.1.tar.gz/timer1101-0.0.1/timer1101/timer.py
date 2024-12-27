import time


class Timer:
    def __init__(
        self,
        name,
        timefunc=time.perf_counter_ns,
        outputfunc=print,
        durationfunc=lambda a: a / 10**6,
    ):
        self.name = name
        self.timefunc = timefunc
        self.outputfunc = outputfunc
        self.durationfunc = durationfunc

        self.adict = {}
        self.format_string_start = r"{event} start at {t}."
        self.format_string_stop = r"{event} stop at {t}, duration {duration}ms."

    def starte(self, event: str):
        """start an event"""
        t = self.timefunc()
        self.adict[event] = t
        s = self.format_string_start.format(event=event, t=t)
        if self.outputfunc is not None:
            self.outputfunc(s)
        return t

    def stope(self, event: str):
        """stop an event"""
        t = self.timefunc()
        start_time = self.adict.pop(event)
        duration = t - start_time
        s = self.format_string_stop.format(
            event=event,
            t=t,
            duration=self.durationfunc(duration),
            start_time=start_time,
        )
        if self.outputfunc is not None:
            self.outputfunc(s)
        return t, duration
