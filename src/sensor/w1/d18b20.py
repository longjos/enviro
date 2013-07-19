import sensor.w1
import os
import glob


DEVICE_FAMILY = '28'
DEVICE_FILE = 'w1_slave'


class Bus(object):
    def __init__(self):
        self._devices = {}

    def scan_devices(self):
        """
            Scan the 1-Wire bus for all devices for this family and return a list of device objects

            :return: Dict of device objects. Key = device_id, Value = :class:`D18B20`
            :rtype: :class:`List`
        """
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
        """
            1-Wire D18B20 temperature sensor

            :param device_id: Unique device ID assigned by manufacture
            :type device_id: :class:`String`

            :param device_file: devfs file location for this device
            :type device_id: :class:`String`
        """
        self.device_id = device_id
        self.device_file = device_file
        self.last_value = 0

    def read(self):
        """
            Read the value of this sensor

            Returns the temperature measured in Degrees F or None if the device does not have a solution
            :rtype: :class:`Int`
        """
        raw_data = self._read_sensor()
        if raw_data is not None:
            self.last_value = self._c_to_f(self._raw_to_c(raw_data))
            return self.last_value
        else:
            return None

    def _raw_to_c(self, raw_data):
        return float(raw_data) / 1000.0

    def _c_to_f(self, c):
        return c * 9.0 / 5.0 + 32.0

    def _read_sensor(self):
        with open(self.device_file, 'r') as fp:
            data_rows = fp.readlines()
            if data_rows[0].strip()[-3:] != 'YES':
                return None
            temperature_position = data_rows[1].find('t=')
            if temperature_position != -1:
                temperature_data = data_rows[1][temperature_position+2:]
                return temperature_data
