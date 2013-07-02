import sensor.w1
import os
import glob


DEVICE_FAMILY = '28'
DEVICE_FILE = 'w1_slave'


class Bus(object):
    def __init__(self):
        self._devices = {}

    def scan_devices(self):
        base_dir = sensor.w1.W1_BASE_DIR
        device_folders = glob.glob(base_dir + DEVICE_FAMILY + '*')
        for device_folder in device_folders:
            device_id = os.path.split(device_folder)[1].split('-', 1)[1]
            device = D18B20(device_id, '%s/%s' % (device_folder, DEVICE_FILE))
            self._devices[device_id] = device
        return self._devices


class D18B20(object):
    def __init__(
            self,
            device_id,
            device_file
    ):
        self.device_id = device_id
        self.device_file = device_file
        self.last_value = 0

    def _read_sensor(self):
        fp = open(self.device_file, 'r')
        data_rows = fp.readlines()
        if data_rows[0].strip()[-3:] != 'YES':
            return None
        temperature_position = data_rows[1].find('t=')
        if temperature_position != -1:
            temperature_data = data_rows[1][temperature_position+2:]

            return temperature_data

    def read(self):
        raw_data = self._read_sensor()
        if raw_data:
            self.last_value = self.c_to_f(self.raw_to_c(raw_data))
            return self.last_value
        else:
            return None

    def raw_to_c(self, raw_data):
        return float(raw_data) / 1000.0

    def c_to_f(self, c):
        return c * 9.0 / 5.0 + 32.0
