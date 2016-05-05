from metrics.context import manager
import time
import inspect


class MetricsMiddleware(object):
    def process_view(self, request, view_func, view_args, view_kwargs):
        self.frame = manager.start()
        self.start_time = time.time()
        view_module_path = inspect.getmodule(view_func).__name__
        self.metadata = {
            "module": view_module_path,
            "view": "{0}.{1}".format(view_module_path, view_func.__name__)
        }

    def extract_request_info(self, request):
        is_ajax = request.is_ajax()
        is_authenticated = request.user.is_authenticated()
        is_staff = request.user.is_staff
        is_superuser = request.user.is_superuser
        username = request.user.username if is_authenticated else None
        referrer = request.META.get('HTTP_REFERER')  # dat spelling
        url = request.get_full_path()

        return {
            "is_ajax": is_ajax,
            "is_authenticated": is_authenticated,
            "is_staff": is_staff,
            "is_superuser": is_superuser,
            "username": username,
            "referrer": referrer,
            "url": url,
            "method": request.method
        }

    def process_response(self, request, response):
        if hasattr(self, "frame"):
            time_taken = (time.time() - self.start_time) * 1000
            self.metadata.update(self.extract_request_info(request))
            self.frame.record("response.time", time_taken, self.metadata)
            manager.end()

        return response
