from django.apps import AppConfig
from django.conf import settings
from metrics.signals import metrics_received
from metrics.utils import log_statistics


class MetricsConfig(AppConfig):
    name = "metrics"
    verbose_name = "django-performance-metrics"

    def ready(self):
        if getattr(settings, "METRICS_CONSOLE_LOG", False) and settings.DEBUG:
            metrics_received.connect(log_statistics)
