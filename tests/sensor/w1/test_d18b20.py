import unittest
from mock import patch
from src.sensor.w1.d18b20 import D18B20

class TestSensor(unittest.TestCase):
    @patch('sensor.w1')
    def test_scan_devices(self, w1):
        w1.W1_BASE_DIR = '/Users/jlong/dev/enviro'
        sensor_bus = D18B20('123', '/somewhere')
        devices = sensor_bus.read()
        print devices
        self.assertTrue(False)



