from influxdb import InfluxDBClient
from django.conf import settings
from metrics.utils import flatten_stats
import datetime

INFLUXDB_ARGS = settings.METRICS_INFLUXDB_CONFIG
INFLUXDB_TAGS = getattr(settings, "METRICS_INFLUXDB_TAGS", {})
client = InfluxDBClient(**INFLUXDB_ARGS)

client.create_database(client._database, True)


def combine_tags(new_tags, **kwargs):
    tags = kwargs
    tags.update(INFLUXDB_TAGS)
    tags.update(new_tags)
    return tags


def log(stats):
    flat_stats = flatten_stats(stats)
    now = datetime.datetime.now().isoformat()
    body = [
        {
            "measurement": "performance_metric",
            "tags": combine_tags(meta, name=name),
            "time": now,
            "fields": {
                "value": float(value)
            }
        }
        for (name, value, meta) in flat_stats
    ]

    client.write_points(body)
