#!/usr/bin/python3

import time
import datetime
import csv
import copy
import os
from metamotion import MetaMotion, Mode, Color, MetaMotionDeviceNotFound, Method
from enum import Enum

class Status(Enum):
    IN_CONNECTION = 0
    DISCONNECTING = 1


class Gather:
    def __init__(self, freq = 25, address = None, save_file = "data", method=Method.STREAMING):
        if address is None:
            devices_detected = MetaMotion.scan_metamotion_sensor()
            if len(devices_detected) == 0:
                raise(MetaMotionDeviceNotFound("A MetaMotionR sensor can't be found"))
            else:
                address = devices_detected[0]

        self.freq = freq
        self.sensor = MetaMotion(address, method)
        self.sensor.connect()
        self.status = Status.IN_CONNECTION
        self.sensor.setup_accelerometer(freq = freq)
        self.sensor.setup_gyroscope(freq = freq)
        self.sensor.turn_on_led(Mode.SOLID, Color.GREEN)
        self.acc_data = []
        self.gyro_data = []
        self.save_file = save_file
        self.root_dir = os.path.expanduser("~/metamotion_files")

    def init_loggers(self):
        self.sensor.gyroscope.setup_logger()
        self.sensor.accelerometer.setup_logger()

        self.sensor.start_logging()

    def get_data_from_loggers(self):
        self.sensor.stop_logging()
        self.sensor.sync_host_with_device()
        time.sleep(3)
        self.sensor.subscribe_anonymous_datasignals()

        self.sensor.download_logs()
        self.sensor.wait_until_download_complete()

        print("The logged data by gyroscope ", self.sensor.gyroscope.rotation_log)
        print("The logged data by accelerometer", self.sensor.accelerometer.acc_log)

        self.acc_data = self.sensor.accelerometer.acc_log
        self.gyro_data = self.sensor.gyroscope.rotation_log
        self.clean_sensor()

    def write_data_to_csv(self):
        if not os.path.exists(self.root_dir):
            os.makedirs(self.root_dir)

        timestamp = datetime.datetime.fromtimestamp(
            time.time()).strftime('%Y-%m-%d_%H:%M:%S')
        filename = self.root_dir + "/" + self.save_file + "_" + timestamp + ".csv"
        
        print("Writing all data to a csv")
        with open(filename, mode='a+') as csv_file:
            fieldnames = ['acc_x', 'acc_y', 'acc_z',\
                'gyro_x', 'gyro_y', 'gyro_z']
            
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            writer.writeheader()    
            for i in range(min(len(self.acc_data), len(self.gyro_data))):
                writer.writerow({
                    'acc_x': self.acc_data[i][0].x, 'acc_y': self.acc_data[i][0].y, 'acc_z': self.acc_data[i][0].z,
                    'gyro_x': self.gyro_data[i][0].x, 'gyro_y': self.gyro_data[i][0].y, 'gyro_z': self.gyro_data[i][0].z
                    })
                    
    def get_data_with_stream(self):
        acc_data = self.acc_data
        gyro_data = self.gyro_data

        def acceleration_handler(acceleration, timestamp):
            print("The acceleration is: {} {} {}".format(acceleration.x, acceleration.y, acceleration.z))
            acc_data.append([copy.deepcopy(acceleration), timestamp])
    
        def rotation_handler(rotation, timestamp):
            print("The rotation is: {} {} {}".format(rotation.x, rotation.y, rotation.z))
            gyro_data.append([copy.deepcopy(rotation), timestamp])

        self.acceleration_handler = acceleration_handler
        self.rotation_handler = rotation_handler
        self.sensor.gyroscope.on_rotation(rotation_handler)
        self.sensor.accelerometer.on_acceleration(acceleration_handler)
        self.sensor.on_disconnect(self.on_disconnect)

    def disconnect(self):
        self.sensor.disconnect()
        self.status = Status.DISCONNECTING

    def on_disconnect(self):
        if self.status == Status.DISCONNECTING:
            return

        while 1:
            try:
                self.sensor.connect()
                break
            except ConnectionError:
                print("None device found")
        self.sensor.setup_accelerometer(freq = self.freq)
        self.sensor.setup_gyroscope(freq = self.freq)
        self.sensor.turn_on_led(Mode.SOLID, Color.GREEN)
        self.sensor.gyroscope.on_rotation(self.rotation_handler)
        self.sensor.accelerometer.on_acceleration(self.acceleration_handler)
        self.sensor.on_disconnect(self.on_disconnect)

    def clean_sensor(self):
        self.sensor.clean()

    def wait_keyboard_interrupt(self):
        print("Press Ctrl-C when the exercise finished")
        self.sensor.wait_until_break()

    def sensor_is_connected(self):
        return self.sensor.is_connected()


if __name__ == '__main__':
    gather = Gather(freq=20)
    # gather.get_data_with_log()
    # gather.write_data_to_csv()
    # gather.get_data_with_stream()
    # gather.wait_keyboard_interrupt()
    # gather.write_data_to_csv()
    # gather.init_loggers()
    gather.get_data_from_loggers()
    gather.write_data_to_csv()
    gather.disconnect()
