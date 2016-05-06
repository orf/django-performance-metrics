def flatten_stats(stats):
    for metric in stats["stats"]:
        yield metric["name"], metric["value"], metric["meta"]

    for child in stats["children"]:
        yield from flatten_stats(child)
