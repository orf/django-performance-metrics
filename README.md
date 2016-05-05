# django-performance-metrics

This library helps you measure and record the performance of functions 
within your complex Django applications. It looks a bit like this:

```python
from django.shortcuts import render
from metrics import measure
import time

@measure()
def expensive_sub_function():
    time.sleep(3)

@measure()
def do_something_expensive():
    time.sleep(1)
    expensive_sub_function()

def my_view(request):
    do_something_expensive()
    return render(request, "template.html")

```


After adding `metrics` to your `INSTALLED_APPS`, 
`metrics.middleware.MetricsMiddleware` to your `MIDDLEWARE_CLASSES`
and setting `METRICS_CONSOLE_LOG` to `True` you get the following output
in the console:

```
 - response.time: 4019.8562145233154
   * Meta: is_authenticated=False username=None is_staff=False referrer=None is_superuser=False view=app.views.test_long is_ajax=False method=GET url=/ module=app.views
	 - app.views.do_something_expensive: 4.002618789672852
		 - app.views.expensive_sub_function: 3.002188205718994
```

You can wrap any number of functions with the `measure` decorator, or 
use it as a context manager:
```
with measure("something_expensive"):
    SomeModel.objects.all().delete()
```

All measurements taken within a request/response cycle are fed to a 
signal called `metrics_received`. Currently the library only prints 
these metrics to the console, but in the future it will be expanded to
log them to external services like InfluxDB.