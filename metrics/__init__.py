from contextlib import ContextDecorator
from metrics.context import manager
import time
import inspect


class measure(ContextDecorator):
    def __init__(self, name=None):
        self.name = name

    def __enter__(self):
        self.frame = manager.start()
        self.start = time.time()

    def __call__(self, func):
        if self.name is None:
            module = inspect.getmodule(func)
            self.name = "{0}.{1}".format(module.__name__, func.__name__)

        return super().__call__(func)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.frame.record(self.name, time.time() - self.start)
        manager.end()


default_app_config = 'metrics.apps.MetricsConfig'
