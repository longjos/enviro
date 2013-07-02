class CollectionBus(object):

    def __init__(self):
        self._collectors = []

    def register_collector(self, collector):
        self._collectors.append(collector)

    def record(self, sensor_id, sensor_value):
        for collector in self._collectors:
            collector.record(sensor_id, sensor_value)
