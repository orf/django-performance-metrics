def _log_stat(metrics, indent=0):
    for metric in metrics["stats"]:
        prefix = "\t" * indent
        metadata_info = " ".join("{0}={1}".format(key, value) for key, value in metric["meta"].items())

        print("{prefix} - {metric[name]}: {metric[value]}".format(prefix=prefix, metric=metric))
        if metadata_info:
            print("{prefix}   * Meta: {meta}".format(prefix=prefix, meta=metadata_info))

    for child in metrics["children"]:
        _log_stat(child, indent=indent + 1)


def log_statistics(metrics, **kwargs):
    print("-" * 20)
    _log_stat(metrics)
    print("-" * 20)
