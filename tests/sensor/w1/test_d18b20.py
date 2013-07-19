import unittest
from mock import patch
from sensor.w1.d18b20 import D18B20, Bus


class TestSensor(unittest.TestCase):
    @patch(__name__ + '.D18B20._read_sensor')
    @patch('sensor.w1')
    def test_sensor_read_freezing(self, w1, _read_sensor):
        _read_sensor.return_value = 0
        w1.W1_BASE_DIR = '/Users/jlong/dev/enviro'
        dut = D18B20('123', '/somewhere')
        read_value = dut.read()
        self.assertEqual(32, read_value)

    @patch(__name__ + '.D18B20._read_sensor')
    @patch('sensor.w1')
    def test_sensor_read_not_ready(self, w1, _read_sensor):
        _read_sensor.return_value = None
        w1.W1_BASE_DIR = '/Users/jlong/dev/enviro'
        dut = D18B20('123', '/somewhere')
        read_value = dut.read()
        self.assertIsNone(read_value)


class TestSensorBus(unittest.TestCase):
    @patch('glob.glob')
    def test_scan_devices_none_found(self, glob):
        glob.return_value = []
        bus = Bus()
        found_devices = bus.scan_devices()
        self.assertDictEqual({}, found_devices)

    @patch('sensor.w1.d18b20.D18B20')
    @patch('glob.glob')
    def test_scan_devices_one_found(self, glob, D18B20):
        glob.return_value = ['/somewhere/w1/28-123456']
        bus = Bus()
        found_devices = bus.scan_devices()
        self.assertIn('123456', found_devices)

