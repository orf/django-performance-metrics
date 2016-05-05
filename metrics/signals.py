from django import dispatch


metrics_received = dispatch.Signal(providing_args=["metrics"])
