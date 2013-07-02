import librato


class LibratoCollector(object):
    def __init__(self, user_name, api_key):
        self._connect(user_name, api_key)

    def _connect(self, user_name, api_key):
        self._connection = librato.connect(user_name, api_key)

    def record(self, sensor_id, sensor_value):
        try:
            self._connection.submit(sensor_id, sensor_value)
        except Exception:
            pass
