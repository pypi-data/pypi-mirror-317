#  """
#    Copyright (c) 2016- 2024, Wiliot Ltd. All rights reserved.
#
#    Redistribution and use of the Software in source and binary forms, with or without modification,
#     are permitted provided that the following conditions are met:
#
#       1. Redistributions of source code must retain the above copyright notice,
#       this list of conditions and the following disclaimer.
#
#       2. Redistributions in binary form, except as used in conjunction with
#       Wiliot's Pixel in a product or a Software update for such product, must reproduce
#       the above copyright notice, this list of conditions and the following disclaimer in
#       the documentation and/or other materials provided with the distribution.
#
#       3. Neither the name nor logo of Wiliot, nor the names of the Software's contributors,
#       may be used to endorse or promote products or services derived from this Software,
#       without specific prior written permission.
#
#       4. This Software, with or without modification, must only be used in conjunction
#       with Wiliot's Pixel or with Wiliot's cloud service.
#
#       5. If any Software is provided in binary form under this license, you must not
#       do any of the following:
#       (a) modify, adapt, translate, or create a derivative work of the Software; or
#       (b) reverse engineer, decompile, disassemble, decrypt, or otherwise attempt to
#       discover the source code or non-literal aspects (such as the underlying structure,
#       sequence, organization, ideas, or algorithms) of the Software.
#
#       6. If you create a derivative work and/or improvement of any Software, you hereby
#       irrevocably grant each of Wiliot and its corporate affiliates a worldwide, non-exclusive,
#       royalty-free, fully paid-up, perpetual, irrevocable, assignable, sublicensable
#       right and license to reproduce, use, make, have made, import, distribute, sell,
#       offer for sale, create derivative works of, modify, translate, publicly perform
#       and display, and otherwise commercially exploit such derivative works and improvements
#       (as applicable) in conjunction with Wiliot's products and services.
#
#       7. You represent and warrant that you are not a resident of (and will not use the
#       Software in) a country that the U.S. government has embargoed for use of the Software,
#       nor are you named on the U.S. Treasury Department’s list of Specially Designated
#       Nationals or any other applicable trade sanctioning regulations of any jurisdiction.
#       You must not transfer, export, re-export, import, re-import or divert the Software
#       in violation of any export or re-export control laws and regulations (such as the
#       United States' ITAR, EAR, and OFAC regulations), as well as any applicable import
#       and use restrictions, all as then in effect
#
#     THIS SOFTWARE IS PROVIDED BY WILIOT "AS IS" AND "AS AVAILABLE", AND ANY EXPRESS
#     OR IMPLIED WARRANTIES OR CONDITIONS, INCLUDING, BUT NOT LIMITED TO, ANY IMPLIED
#     WARRANTIES OR CONDITIONS OF MERCHANTABILITY, SATISFACTORY QUALITY, NONINFRINGEMENT,
#     QUIET POSSESSION, FITNESS FOR A PARTICULAR PURPOSE, AND TITLE, ARE DISCLAIMED.
#     IN NO EVENT SHALL WILIOT, ANY OF ITS CORPORATE AFFILIATES OR LICENSORS, AND/OR
#     ANY CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY,
#     OR CONSEQUENTIAL DAMAGES, FOR THE COST OF PROCURING SUBSTITUTE GOODS OR SERVICES,
#     FOR ANY LOSS OF USE OR DATA OR BUSINESS INTERRUPTION, AND/OR FOR ANY ECONOMIC LOSS
#     (SUCH AS LOST PROFITS, REVENUE, ANTICIPATED SAVINGS). THE FOREGOING SHALL APPLY:
#     (A) HOWEVER CAUSED AND REGARDLESS OF THE THEORY OR BASIS LIABILITY, WHETHER IN
#     CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE);
#     (B) EVEN IF ANYONE IS ADVISED OF THE POSSIBILITY OF ANY DAMAGES, LOSSES, OR COSTS; AND
#     (C) EVEN IF ANY REMEDY FAILS OF ITS ESSENTIAL PURPOSE.
#  """
import importlib
import sys

from wiliot_testers.yield_tester.configs.inlay_data import all_inlays
from wiliot_testers.yield_tester.simulation.yield_simulation_utils import get_simulated_gw_port, AUTO_PACKET, \
    AUTO_TRIGGERS, TIME_BETWEEN_AUTO_TRIGGERS
from wiliot_core import *

script_dir = os.path.dirname(__file__)
json_file_path = os.path.join(script_dir, '../configs', 'user_inputs.json')
default_user_inputs = {
    "min_cumulative": "60",
    "min_cumulative_line": "yes",
    "min_current": "20",
    "min_current_line": "yes",
    "max_temperature": "40",
    "min_temperature": "10",
    "temperature_type": "C",
    "min_humidity": "20",
    "max_humidity": "90",
    "min_light_intensity": "0",
    "max_light_intensity": "1500",
    "red_line_cumulative": "85",
    "red_line_current": "50",
    "pin_number": "004",
    "Arduino": "Yes",
    "rssi_threshold": ""
}
try:
    with open(json_file_path) as f:
        user_inputs = json.load(f)
    for key, value in default_user_inputs.items():
        if key not in user_inputs:
            user_inputs[key] = value
    with open(json_file_path, 'w') as f:
        json.dump(user_inputs, f, indent=4)
except Exception as e:
    user_inputs = default_user_inputs
    os.makedirs(os.path.dirname(json_file_path), exist_ok=True)
    with open(json_file_path, 'w') as f:
        json.dump(user_inputs, f, indent=4)

SECONDS_WITHOUT_PACKETS = 60
SECONDS_FOR_GW_ERROR_AFTER_NO_PACKETS = 120
MAX_SUB1G_POWER = 29
MAX_BLE_POWER = 22
ARDUINO_EXISTS = (user_inputs.get('Arduino', '').strip().lower() == 'yes')

inlay_data_eng_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'configs', 'inlay_data_eng.py')
if os.path.exists(inlay_data_eng_path):
    inlay_data = getattr(importlib.import_module('wiliot_testers.yield_tester.configs.inlay_data_eng'), 'all_inlays', {})
    inlays = inlay_data if inlay_data else all_inlays
else:
    inlays = all_inlays


class AdvaProcess(object):
    """
    Counting the number of unique advas
    """

    def __init__(self, stop_event, inlay_type, logging_file, listener_path, time_between_matrices, rssi_th):
        self.stopped_by_user = False
        self.take_care_of_pausing = False
        self.gw_error_connection = False
        self.second_without_packets = False
        self.gw_instance = None
        self.rssi_th = rssi_th
        self.logger_file = logging_file
        self.listener_path = listener_path
        self.all_tags = Queue()
        self.stop = stop_event
        self.gw_start_time = datetime.datetime.now()
        self.init_gw(listener_path)
        self.trigger_time_queue = deque(maxlen=10)
        self.last_change_time = 0
        self.number_of_sensor_triggers = 0
        self.needed_time_between_matrices = TIME_BETWEEN_AUTO_TRIGGERS if AUTO_TRIGGERS else time_between_matrices
        self.inlay_type = inlay_type
        self.gw_reset_config()
        time.sleep(1)

    def init_gw(self, listener_path=None):

        try:
            if self.gw_instance is None:
                gw_port = get_simulated_gw_port() if AUTO_PACKET else None
                self.gw_instance = WiliotGateway(auto_connect=True,
                                                 logger_name='yield',
                                                 log_dir_for_multi_processes=listener_path,
                                                 port=gw_port,
                                                 np_max_packet_in_buffer_before_error=10)

            else:
                # reconnect
                is_connected = self.gw_instance.is_connected()
                if is_connected:
                    self.gw_instance.close_port()
                self.gw_instance.open_port(self.gw_instance.port, self.gw_instance.baud)

            is_connected = self.gw_instance.is_connected()
            if is_connected:
                self.gw_instance.start_continuous_listener()
            else:
                self.logger_file.warning("Couldn't connect to GW in main thread")
                raise Exception(f"Couldn't connect to GW in main thread")

        except Exception as ee:
            raise Exception(f"Couldn't connect to GW in main thread, error: {ee}")

    def set_stopped_by_user(self, stopped):
        self.stopped_by_user = stopped
        self.take_care_of_pausing = True

    def get_gw_start_time(self):
        return self.gw_start_time

    def get_last_change_time(self):
        return self.last_change_time

    def get_gw_error_connection(self):
        return self.gw_error_connection

    def pop_from_triggers_queue(self):
        self.trigger_time_queue.popleft()

    def get_trigger_time_queue(self):
        return self.trigger_time_queue

    def get_sensors_triggers(self):
        return self.number_of_sensor_triggers

    def gw_reset_config(self, start_gw_app=False):
        """
        Configs the gateway
        """
        if self.gw_instance.connected:
            self.gw_instance.reset_gw()
            self.gw_instance.reset_listener()
            time.sleep(2)
            if not self.gw_instance.is_gw_alive():
                self.logger_file.warning('gw_reset_and_config: gw did not respond')
                raise Exception('gw_reset_and_config: gw did not respond after rest')

            gw_config = inlays.get(self.inlay_type)

            cmds = {CommandDetails.scan_ch: gw_config['received_channel'],
                    CommandDetails.time_profile: gw_config['time_profile_val'],
                    CommandDetails.set_energizing_pattern: gw_config['energy_pattern_val'],
                    CommandDetails.set_sub_1_ghz_power: [MAX_SUB1G_POWER],
                    CommandDetails.set_scan_radio: self.gw_instance.get_cmd_symbol_params(
                        freq_str=gw_config['symbol_val']),
                    CommandDetails.set_rssi_th: self.rssi_th,
                    }
            output_power_cmds = self.gw_instance.get_cmds_for_abs_output_power(abs_output_power=MAX_BLE_POWER)
            cmds = {**cmds, **output_power_cmds}
            self.gw_instance.set_configuration(cmds=cmds, start_gw_app=start_gw_app, read_max_time=1)
            if not ARDUINO_EXISTS and not AUTO_TRIGGERS:
                pin_num = user_inputs.get('pin_number')
                cmd = '!cmd_gpio CONTROL_IN P%s 0' % pin_num.zfill(3)
                self.gw_instance.write(cmd, must_get_ack=True)
        else:
            raise Exception('Could NOT connect to GW')

    def raising_trigger_number(self):
        self.number_of_sensor_triggers += 1
        self.logger_file.info(f'Got a Trigger.  Number of Triggers {self.number_of_sensor_triggers}')

    def run(self):
        """
        Receives available data then counts and returns the number of unique advas.
        """
        self.gw_instance.set_configuration(start_gw_app=True)
        self.gw_instance.reset_start_time()
        self.gw_start_time = datetime.datetime.now()
        got_new_adva = False
        no_data_start_time = None  # Time when we first detect no data available

        while not self.stop.is_set():
            time.sleep(0)
            current_time_of_data = (datetime.datetime.now() - self.gw_start_time).total_seconds()
            time_condition_met = current_time_of_data - self.last_change_time >= self.needed_time_between_matrices

            gw_rsp = self.gw_instance.get_gw_rsp()

            if not self.stopped_by_user and self.take_care_of_pausing:
                self.gw_reset_config(start_gw_app=True)
                self.take_care_of_pausing = False
            elif self.stopped_by_user and self.take_care_of_pausing:
                self.gw_instance.reset_gw()
                self.take_care_of_pausing = False

            if time_condition_met:
                if AUTO_TRIGGERS:
                    self.last_change_time = (datetime.datetime.now() - self.gw_start_time).total_seconds()  # a float
                    self.raising_trigger_number()
                    self.trigger_time_queue.append([self.last_change_time, self.number_of_sensor_triggers])
                else:
                    if gw_rsp is not None and 'Detected High-to-Low peak' in gw_rsp['raw'] and not self.stopped_by_user:
                        self.last_change_time = gw_rsp['time']  # a float
                        self.raising_trigger_number()
                        self.trigger_time_queue.append([self.last_change_time, self.number_of_sensor_triggers])

            if self.gw_instance.is_data_available() and not self.stopped_by_user:
                raw_packets_in = self.gw_instance.get_packets(action_type=ActionType.ALL_SAMPLE,
                                                              data_type=DataType.RAW, tag_inlay=self.inlay_type)
                if not self.all_tags.full():
                    self.all_tags.put(raw_packets_in)
                else:
                    self.logger_file.warning(f"Queue is full.. Packet: {raw_packets_in}")
                got_new_adva = True
                no_data_start_time = None
            else:
                if not self.stopped_by_user:
                    if no_data_start_time is None:
                        no_data_start_time = time.time()
                    if time.time() - no_data_start_time >= SECONDS_WITHOUT_PACKETS:
                        got_new_adva = False
                        if not self.second_without_packets:
                            self.logger_file.warning("One minute without packets..")
                            self.second_without_packets = True
                        time.sleep(5)
                        if not self.gw_instance.is_connected():
                            self.reconnect()
                    if time.time() - no_data_start_time >= SECONDS_FOR_GW_ERROR_AFTER_NO_PACKETS:
                        self.gw_error_connection = True
                        break
                    if self.gw_instance.get_read_error_status():
                        self.logger_file.warning("Reading error.. Listener did recovery flow.")
                    time.sleep(0.050 if not got_new_adva else 0)
                else:
                    no_data_start_time = None
        self.gw_instance.reset_gw()
        self.gw_instance.exit_gw_api()

    def reconnect(self):
        self.logger_file.info('Trying to reconnect to GW')
        try:
            self.init_gw()
            self.gw_reset_config(start_gw_app=True)
        except Exception as e:
            self.logger_file.warning(f"Couldn't reconnect GW, due to: {e}")

    def get_raw_packets_queue(self):
        """
        Returns the packet queue that is created above
        """
        return self.all_tags
