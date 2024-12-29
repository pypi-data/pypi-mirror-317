import datetime
import time
from collections import deque

import serial
from wiliot_testers.yield_tester.simulation.yield_simulation_utils import AUTO_TRIGGERS, TIME_BETWEEN_AUTO_TRIGGERS
from wiliot_testers.yield_tester.utils.get_arduino_ports import get_arduino_ports

BAUD_ARDUINO = 1000000


class CountThread(object):
    """
    Counting the number of tags
    """

    def __init__(self, stop_event, logger_file, matrix_size=1, ther_cols=1):
        self.arduino_connection_error = False
        self.pause_triggers = False
        self.logger_file = logger_file
        self.start_time = datetime.datetime.now()
        self.last_arduino_trigger_time = datetime.datetime.now()
        self.comPortObj = None
        self.trigger_port = None
        if not AUTO_TRIGGERS:
            self.connect()
        self.matrix_size = matrix_size
        self.ther_cols = ther_cols
        self.stop = stop_event
        self.matrix_cnt = 0
        self.trigger_times = deque(maxlen=10)

    def connect(self):
        optional_ports = get_arduino_ports()
        if len(optional_ports) == 0:
            raise Exception("NO ARDUINO")
        for port in optional_ports:
            try:
                self.comPortObj = serial.Serial(port, BAUD_ARDUINO, timeout=0.1)
                time.sleep(2)
                initial_message = self.comPortObj.readline().decode().strip()
                if "Wiliot Yield Counter" in initial_message:
                    self.trigger_port = port
            except Exception as e:
                raise Exception(f'could not connect to port {port} due to {e}')

    def raising_trigger(self):
        self.last_arduino_trigger_time = datetime.datetime.now()
        self.matrix_cnt += 1
        self.update_trigger_times((self.last_arduino_trigger_time - self.start_time).total_seconds())  # a float
        self.logger_file.info(f'Got a Trigger.  Number of Triggers {self.matrix_cnt}')

    def reconnect(self):
        """
        Attempts to reconnect to the Arduino.
        """
        connected = False
        start_time = time.time()
        while not connected and not self.stop.is_set() and time.time() - start_time < 60:
            try:
                self.comPortObj = serial.Serial(self.trigger_port, BAUD_ARDUINO, timeout=0.1)
                connected = True
                self.logger_file.info("Reconnected to Arduino")
            except serial.SerialException:
                self.logger_file.error("Reconnection failed. Trying again...")
                time.sleep(5)
        if not connected:
            self.arduino_connection_error = True

    def run(self):
        """
        Tries to read data and then counts the number of tags
        """
        while not self.stop.is_set():
            time.sleep(0.100)
            if not AUTO_TRIGGERS:
                try:
                    data = self.comPortObj.readline()
                    if data.__len__() > 0:
                        try:
                            tmp = data.decode().strip(' \t\n\r')
                            if "pulses detected" in tmp and not self.pause_triggers:
                                self.raising_trigger()
                        except Exception as ee:
                            self.logger_file.error(f'Warning: Could not decode counter data or Warning: {ee}')
                except serial.SerialException as e:
                    self.logger_file.error("Arduino is disconnected   ", e)
                    self.reconnect()
                except Exception as ee:
                    self.logger_file.error(f"NO READLINE: {ee}")
            else:
                self.raising_trigger()
                time.sleep(TIME_BETWEEN_AUTO_TRIGGERS)
        if not AUTO_TRIGGERS:
            self.comPortObj.close()

    def update_trigger_times(self, trigger_time):
        self.trigger_times.append([trigger_time, self.matrix_cnt])

    def get_trigger_times(self):
        return self.trigger_times

    def pop_from_triggers_queue(self):
        self.trigger_times.popleft()

    def set_pause_triggers(self, paused):
        self.pause_triggers = paused

    def get_tested(self):
        """
        returns the number of tags
        """
        return self.matrix_cnt * int(self.matrix_size)

    def get_arduino_connection_error(self):
        return self.arduino_connection_error

    def get_matrix_cnt(self):
        return self.matrix_cnt
