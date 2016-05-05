from metrics import measure


@measure()
def expensive_op():
    import time
    time.sleep(0.5)
