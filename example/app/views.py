from django.shortcuts import render
import time
import metrics


@metrics.measure()
def expensive_sub_function():
    time.sleep(3)


@metrics.measure()
def do_something_expensive():
    time.sleep(1)
    expensive_sub_function()


# Create your views here.
def test(request):
    return render(request, "test.html")


def test_long(request):
    do_something_expensive()

    return render(request, "test.html")
