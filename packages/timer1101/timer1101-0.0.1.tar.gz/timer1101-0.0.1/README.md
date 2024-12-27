```python
import timer1101 as timer

if __name__ == "__main__":
    timer.starte("test")
    # some codes
    timer.stope("test")

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