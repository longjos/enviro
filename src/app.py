import ConfigParser
from sensor.w1.d18b20 import Bus
from collector import CollectionBus
from collector.librato_collector import LibratoCollector
import time


config = ConfigParser.SafeConfigParser()
config.read('config.ini')

collection_bus = CollectionBus()
# collection_bus.register_collector(
#     LibratoCollector(
#         config.get('metrics', 'user_name'),
#         config.get('metrics', 'api_key')
#     )
# )


device_bus = Bus()
devices = device_bus.scan_devices()
while True:
    for device_id, device in devices.iteritems():
        last_value = device.last_value
        sensor_data = device.read()
        if sensor_data:
            print "Sensor %s says: %s" % (device_id, sensor_data)
            if sensor_data != last_value:
                collection_bus.record(device_id, sensor_data)
    time.sleep(.5)


