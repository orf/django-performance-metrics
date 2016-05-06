from django.apps import AppConfig
from django.conf import settings
from metrics.signals import metrics_received
from django.utils.module_loading import import_string


class MetricsConfig(AppConfig):
    name = "metrics"
    verbose_name = "django-performance-metrics"

    def ready(self):
        backend = getattr(settings, "METRICS_BACKEND", "metrics.backend.console")
        backend_log_funcs = [import_string("{0}.log".format(backend))]

        if settings.DEBUG:
            backend_log_funcs.append(
                import_string("metrics.backend.console.log")
            )

        def receiver(metrics, **kwargs):
            for func in backend_log_funcs:
                func(metrics)

        metrics_received.connect(receiver, weak=False)

