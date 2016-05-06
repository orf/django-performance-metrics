from django.shortcuts import render
import time
import metrics


@metrics.profile()
def expensive_sub_function():
    time.sleep(3)
    metrics.measure("user_count", 100)


@metrics.profile()
def do_something_expensive():
    time.sleep(1)
    expensive_sub_function()


# Create your views here.
def test(request):
    return render(request, "test.html")


def test_long(request):
    do_something_expensive()

    return render(request, "test.html")
