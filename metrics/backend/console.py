

def log(metrics, indent=0):
    for metric in metrics["stats"]:
        prefix = "\t" * indent
        metadata_info = " ".join("{0}={1}".format(key, value) for key, value in metric["meta"].items())

        print("{prefix} - {metric[name]}: {metric[value]}".format(prefix=prefix, metric=metric))
        if metadata_info:
            print("{prefix}   * Meta: {meta}".format(prefix=prefix, meta=metadata_info))

    for child in metrics["children"]:
        log(child, indent=indent + 1)
