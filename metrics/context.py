from threading import local
from django.core.signals import request_finished
from collections import namedtuple
from metrics.signals import metrics_received

Metric = namedtuple("Metric", "name value metadata")


class MetricsContextManager(local):
    def __init__(self):
        self.stack = []
        request_finished.connect(self._request_finished)

    def _request_finished(self, **kwargs):
        pass

    def start(self):
        frame = MetricsFrame()
        self.stack.append(frame)
        return frame

    def end(self):
        frame = self.stack.pop()
        if self.is_active:
            self.current_frame.join(frame)
        else:
            metrics_received.send(sender=self.__class__, metrics=frame.to_dict())

    @property
    def is_active(self):
        return bool(self.stack)

    @property
    def current_frame(self):
        return self.stack[-1]

    def __enter__(self):
        return self.start()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end()


class MetricsFrame(object):
    def __init__(self):
        self._children = []
        self._stats = []

    def record(self, name, value, metadata=None):
        self._stats.append(Metric(name, value, metadata or {}))

    def join(self, other_frame):
        self._children.append(other_frame)

    def to_dict(self):
        return {
            "stats": [
                {"name": name, "value": value, "meta": meta}
                for (name, value, meta) in self._stats
            ],
            "children": [child.to_dict() for child in self._children]
        }


manager = MetricsContextManager()
