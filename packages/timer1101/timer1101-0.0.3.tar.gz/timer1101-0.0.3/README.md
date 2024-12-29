```python
import timer1101 as timer

if __name__ == "__main__":
    timer.starte("test0")
    # some codes
    timer.starte("test1")
    # some codes
    timer.stope("test0")
    # some codes
    timer.stope("test1")

```

```python
import timer1101 as timer
import logging
import coloredlogs
import verboselogs


verboselogs.install()
coloredlogs.install(level=logging.INFO)
logger = logging.getLogger("timeLogger")
timer.rootTimer.outputfunc = logger.info

if __name__ == "__main__":
    timer.starte("test")
    # some codes
    timer.stope("test")

```

```python
from timer1101 import timefunc


@timefunc()
def func(l):
    for i in range(l):
        print(i)
    return l


if __name__ == "__main__":
    ret = func(10)
    print(ret)

```
