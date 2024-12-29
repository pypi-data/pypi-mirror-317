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

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from wiliot_tools.utils.wiliot_gui.wiliot_gui import WiliotGui, popup_message
from wiliot_tools.test_equipment.test_equipment import YoctoSensor
from wiliot_tools.resolver_tool.resolve_packets import ResolvePackets

from wiliot_testers.tester_utils import dict_to_csv
import matplotlib
import matplotlib.pyplot as plt
from functools import partial
from wiliot_testers.utils.get_version import get_version
from wiliot_testers.utils.upload_to_cloud_api import upload_to_cloud_api
from wiliot_testers.yield_tester.modules.adva_process import *
from wiliot_testers.yield_tester.modules.count_thread import *
from wiliot_testers.yield_tester.utils.resolve_utils import *

import time

CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'configs', 'gui_input_do_not_delete.json')
DEFAULT_USER_INPUT = {
    'inlay_dict_inlay': '', 'number': '', 'received_channel': '',
    'energy_pattern_val': '', 'tester_station_name': '',
    'comments': '', 'operator': '', 'wafer_lot': '', 'wafer_num': '',
    'conversion_type': '', 'surface': '', 'matrix_tags': '',
    'thermodes_col': 1, 'gw_energy_pattern': '', 'gw_time_profile': '',
    'window_size': 1, 'assembled_reel': '', 'do_resolve': False, 'owner_id': '',
}
RED_COLOR = 'red'
BLACK_COLOR = 'black'
SET_VALUE_MORE_THAN_100 = 110
VALUE_WHEN_NO_SENSOR = -10000
MIN_Y_FOR_PLOTS = 0
MAX_Y_FOR_PLOTS = 112
FIRST_STEP_SIZE = 10
TIME_BETWEEN_MATRICES = 0.5
RSSI_THRESHOLD = int(user_inputs.get('rssi_threshold', '0') or '0')

MAND_FIELDS = ['wafer_lot', 'wafer_num', 'window_size', 'thermodes_col', 'lanes',
               'q_size']  # mandatory fields in GUI before the run

matplotlib.use('TkAgg')
today = datetime.date.today()
formatted_today = today.strftime("%Y%m%d")  # without -
formatted_date = today.strftime("%Y-%m-%d")
current_time = datetime.datetime.now()
cur_time_formatted = current_time.strftime("%H%M%S")  # without :
time_formatted = current_time.strftime("%H:%M:%S")
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %H:%M:%S %p')
root_logger = logging.getLogger()

for handler in root_logger.handlers:
    if isinstance(handler, logging.StreamHandler):
        handler.setLevel(logging.INFO)


class MainWindow:
    """
    The main class the runs the GUI and supervise the multi-threading process of fraction's calculation and GUI viewing
    """

    def __init__(self):
        self.curr_ex_id_for_log = None
        self.user_input = {}
        self.resolve_path = ''
        self.external_ids = []
        self.resolver = None
        self.resolve_q = None
        self.previous_input = {}
        self.current_values = None
        self.current_status_text = None
        self.cumulative_status_text = None
        self.assembled_reel = None
        self.lane_ids = ''
        self.light_intensity = None
        self.humidity = None
        self.temperature = None
        self.main_sensor = None
        self.main_gui = None
        self.test_started = True
        self.user_response_after_arduino_connection_error = False
        self.advanced_window = None
        self.user_response_after_gw_connection_error = False
        self.env_choice = 'prod'
        self.matrix_size = None
        self.filling_missed_field = None
        self.start_run = None
        self.logger = None
        self.ttfp = None
        self.curr_adva_for_log = None
        self.conversion_type = None
        self.surface = None
        self.adva_process = None
        self.adva_process_thread = None
        self.count_process = None
        self.count_process_thread = None
        self.resolver_thread = None
        self.folder_path = None
        self.py_wiliot_version = None
        self.final_path_run_data = None
        self.run_data_dict = None
        self.stop = threading.Event()
        self.thermodes_col = None
        self.print_neg_advas = True
        self.selected = ''
        self.wafer_lot = ''
        self.wafer_number = ''
        self.window_size = 1
        self.operator = ''
        self.tester_type = 'yield'
        self.tester_station_name = ''
        self.comments = ''
        self.gw_energy_pattern = None
        self.gw_time_profile = None
        self.rows_number = 1
        self.upload_flag = True
        self.cmn = ''
        self.final_path_packets_data = None
        self.seen_advas = set()
        self.not_neg_advas = 0  # used only to be shown in the small window
        self.update_packet_data_flag = False
        self.advas_before_tags = set()
        self.stop_run = False
        self.fig_canvas_agg1 = None
        self.trigger_count = 0
        self.yield_type = None

    def setup_logger(self, yield_tester_type):
        # Logger setup
        self.init_file_path(yield_tester_type)
        self.logger = logging.getLogger('yield')
        if self.logger.hasHandlers():
            self.logger.handlers.clear()
        self.logger.setLevel(logging.INFO)
        final_path_log_file = os.path.join(self.folder_path, self.cmn + '@yield_log.log')
        file_handler = logging.FileHandler(final_path_log_file)
        file_handler.setFormatter(
            logging.Formatter('%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p'))
        file_handler.setLevel(logging.INFO)
        self.logger.addHandler(file_handler)

    def get_adva_yield_result(self):
        """
        Calculates the yield fraction
        """
        result = 0
        tags_num = self.get_number_of_tested()
        if tags_num > 0:
            result = (self.not_neg_advas / tags_num) * 100
        return result

    def get_ex_yield_result(self):
        """
        Calculates the yield fraction
        """
        result = 0
        tags_num = self.get_number_of_tested()
        if tags_num > 0:
            result = (len(self.external_ids) / tags_num) * 100
        return result

    def run(self):
        """
        Viewing the window and checking if the process stops
        """
        self.open_session()
        if self.start_run:
            self.init_processes(self.selected)
            time.sleep(0.5)
            self.init_run_data()
            self.init_resolver_data()
            self.start_processes()
            self.overlay_window()
        else:
            self.logger.warning('Error Loading Program')

    def init_file_path(self, yield_tester_type):
        self.py_wiliot_version = get_version()
        d = WiliotDir()
        d.create_tester_dir(tester_name=yield_tester_type)
        yield_test_app_data = d.get_tester_dir(yield_tester_type)
        run_path = os.path.join(yield_test_app_data, self.get_log_folder_name())
        if not os.path.exists(run_path):
            os.makedirs(run_path)
        self.cmn = self.get_cmn(formatted_today, cur_time_formatted)
        self.folder_path = os.path.join(run_path, self.cmn)
        if not os.path.exists(self.folder_path):
            os.makedirs(self.folder_path)

    def get_log_folder_name(self):
        return self.wafer_lot + '.' + self.wafer_number

    def get_cmn(self, day_str, time_str):
        return f'{self.wafer_lot}.{self.wafer_number}_{day_str}_{time_str}'

    def init_resolver_data(self):
        if not self.user_input['do_resolve']:
            return

        self.resolve_path = os.path.join(self.folder_path, self.cmn + '@resolve_data.csv')
        dict_to_csv({'adv_address': [], 'resolve_status': [], 'external_id': []},
                    self.resolve_path, only_titles=True)

    def init_run_data(self):
        self.final_path_run_data = os.path.join(self.folder_path, self.cmn + '@run_data.csv')
        gw_version = self.adva_process.gw_instance.get_gw_version()[0]
        start_time = datetime.datetime.now()
        run_start_time = start_time.strftime("%H:%M:%S")
        value = inlays[self.selected]
        self.run_data_dict = {'common_run_name': self.cmn, 'tester_station_name': self.tester_station_name,
                              'operator': self.operator, 'received_channel': value['received_channel'],
                              'run_start_time': formatted_date + ' ' + run_start_time, 'run_end_time': '',
                              'wafer_lot': self.wafer_lot, 'wafer_number': self.wafer_number,
                              'assembled reel': self.assembled_reel, 'lane_ids': self.lane_ids,
                              'window_size': self.window_size, 'upload_date': '',
                              'tester_type': self.tester_type, 'gw_energy_pattern': self.gw_energy_pattern,
                              'comments': self.comments, 'inlay': self.selected, 'total_run_tested': 0,
                              'total_run_responding_tags': 0, 'conversion_type': self.conversion_type,
                              'gw_version': gw_version, 'surface': self.surface, 'matrix_tags': str(self.matrix_size),
                              'py_wiliot_version': self.py_wiliot_version, 'number_of_columns': self.thermodes_col,
                              'number_of_lanes': self.rows_number, 'gw_time_profile': self.gw_time_profile}

    def update_run_data_file(self, run_end_time, tags_num, advas, result, upload_date=''):

        """
        Updates the run_data CSV file while running the program
        """
        self.run_data_dict['run_end_time'] = run_end_time
        self.run_data_dict['upload_date'] = upload_date
        self.run_data_dict['total_run_tested'] = tags_num
        self.run_data_dict['total_run_responding_tags'] = advas
        self.run_data_dict['yield'] = result
        self.run_data_dict['conversion_type'] = self.conversion_type
        self.run_data_dict['surface'] = self.surface
        if self.user_input['do_resolve']:
            self.run_data_dict['total_run_external_ids'] = len(self.external_ids)
            self.run_data_dict['yield_external_ids'] = 100 * (len(self.external_ids) / tags_num) if tags_num else 0
        dict_to_csv(dict_in=self.run_data_dict, path=self.final_path_run_data)

    def calculate_ttfp_with_queue(self, packet_time, trigger_time_queue):
        while trigger_time_queue:
            try:
                trigger_time, matrix_cnt = trigger_time_queue[0]
                if len(trigger_time_queue) > 1:
                    trigger_time_next, _ = trigger_time_queue[1]
                else:
                    trigger_time_next = float('inf')
                # [matrix_x, time_x] <= p_time <= [matrix_y, time_y] --> p from matrix x
                if trigger_time <= packet_time <= trigger_time_next:
                    return trigger_time, matrix_cnt, packet_time - trigger_time
                elif packet_time < trigger_time:  # got packet before trigger
                    return float('nan'), matrix_cnt - 1, float('nan')
                else:  # packet_time > trigger_time_next
                    # Remove the processed trigger time
                    if ARDUINO_EXISTS:
                        self.count_process.pop_from_triggers_queue()
                    else:
                        self.adva_process.pop_from_triggers_queue()

            except Exception as e:
                self.logger.warning(f'Could not calculate tag matrix TTFP due to {e}')
                break
        return float('nan'), None, float('nan')

    def add_to_resolve_queue(self, packet_in):
        adva = packet_in.get_adva()
        if self.resolve_q.full():
            self.logger.warning(f'resolve queue is full discard the following adva: {adva}')
            return
        self.resolve_q.put({'tag': adva, 'payload': packet_in.get_payload()})

    def update_packet_data(self):
        """
        Updates the run_data CSV file while running the program
        """
        raw_packet_queue = self.adva_process.get_raw_packets_queue()
        triggers_queue = self.adva_process.get_trigger_time_queue() if not ARDUINO_EXISTS else \
            self.count_process.get_trigger_times()

        if not raw_packet_queue.empty():
            cur_df = pd.DataFrame()
            n_elements = raw_packet_queue.qsize()
            # Collecting Packets from the queue and putting them into a TagCollection
            for _ in range(n_elements):
                for p in raw_packet_queue.get():
                    trigger_time, matrix_cnt, tag_matrix_ttfp = self.calculate_ttfp_with_queue(p['time'],
                                                                                               triggers_queue)
                    cur_p = Packet(p['raw'], time_from_start=p['time'], inlay_type=self.selected,
                                   custom_data={
                                       'common_run_name': self.cmn,
                                       'matrix_tags_location': matrix_cnt,
                                       'matrix_timestamp': trigger_time,
                                       'tag_matrix_ttfp': tag_matrix_ttfp,
                                       'environment_light_intensity': self.light_intensity,
                                       'environment_humidity': self.humidity,
                                       'environment_temperature': self.temperature})

                    tag_id = cur_p.get_adva()

                    if self.get_number_of_tested() == 0:
                        self.advas_before_tags.add(tag_id)
                    else:
                        if self.print_neg_advas:
                            self.logger.info('neglected advas:  %05d', len(self.advas_before_tags))
                            self.print_neg_advas = False

                    if tag_id not in self.seen_advas and tag_id not in self.advas_before_tags:
                        cur_p_df = cur_p.as_dataframe(sprinkler_index=0)
                        cur_df = pd.concat([cur_df, cur_p_df], ignore_index=True)
                        self.seen_advas.add(tag_id)
                        self.logger.info(f"New adva {tag_id}")
                        if self.user_input['do_resolve']:
                            self.add_to_resolve_queue(cur_p)

            # writing to DataFrame and then to CSV
            if not cur_df.empty:
                self.final_path_packets_data = os.path.join(self.folder_path, f"{self.cmn}@packets_data.csv")
                try:
                    if not self.update_packet_data_flag:
                        cur_df.to_csv(self.final_path_packets_data, mode='w', header=True, index=False)
                        self.update_packet_data_flag = True
                    else:
                        cur_df.to_csv(self.final_path_packets_data, mode='a', header=False, index=False)
                except Exception as ee:
                    self.logger.error(f"Exception occurred: {ee}")

    def stop_button(self, run_end_time, tags_num, advas, result, upload_date):
        """
        Finishing the program and saves the last changes after pressing Stop in the second window
        """
        self.logger.info(f"User quit from application")
        self.adva_process_thread.join()
        self.update_run_data_file(formatted_date + ' ' + run_end_time, tags_num, advas, result, upload_date)
        self.update_packet_data()
        if ARDUINO_EXISTS:
            self.count_process_thread.join()
        if self.resolver_thread is not None:
            self.resolver_thread.join()

    def init_processes(self, inlay_select, time_between_matrices=TIME_BETWEEN_MATRICES, rssi_th=RSSI_THRESHOLD):
        """
        Initializing the two main instances and threads in order to start working
        """
        try:
            self.adva_process = AdvaProcess(stop_event=self.stop,
                                            inlay_type=inlay_select,
                                            logging_file=self.logger,
                                            listener_path=self.folder_path,
                                            time_between_matrices=time_between_matrices, rssi_th=rssi_th)
            self.adva_process_thread = threading.Thread(target=self.adva_process.run, args=())
        except Exception as e:
            self.logger.warning(f"{e}")
            popup_message(msg='GW is not connected. Please connect it.', logger=self.logger)
            raise Exception('GW is not connected')

        if ARDUINO_EXISTS:
            try:
                self.count_process = CountThread(self.stop, self.logger, self.matrix_size, self.thermodes_col)
                self.count_process_thread = threading.Thread(target=self.count_process.run, args=())
            except Exception as e:
                self.logger.warning(f"{e}")
                popup_message(msg='Arduino is not connected. Please connect it.', logger=self.logger)
                raise Exception('Arduino is not connected')

        if self.user_input['do_resolve']:
            self.yield_type = 'External Ids'
            resolve_q = Queue(maxsize=10000)
            self.resolver = ResolvePackets(tags_in_test=[],
                                           owner_id=self.user_input['owner_id'],
                                           env=ENV_RESOLVE,
                                           resolve_q=resolve_q,
                                           set_tags_status_df=self.updated_resolved_tags,
                                           stop_event_trig=self.stop,
                                           logger_name=self.logger.name,
                                           gui_type='ttk',
                                           tag_status=YieldTagStatus
                                           )
            self.resolver_thread = threading.Thread(target=self.resolver.run, args=())
            self.resolve_q = resolve_q
        else:
            self.yield_type = 'Advas'

    def updated_resolved_tags(self, tag_status):
        """
        tag_status = {'adv_address': [tag],
                      'resolve_status': [status],
                      'external_id': [ex_id]}
        @return:
        @rtype:
        """
        tag_status = {k: v[0] for k, v in tag_status.items()}
        new_ex_id = tag_status['external_id']
        self.logger.info(f'update resolved tags: {new_ex_id}')
        if new_ex_id not in self.external_ids:
            self.external_ids.append(new_ex_id)
        dict_to_csv(dict_in=tag_status, path=self.resolve_path, append=True)

    def start_processes(self):
        """
        Starting the work of the both threads
        """
        self.adva_process_thread.start()
        if ARDUINO_EXISTS:
            self.count_process_thread.start()
        if self.resolver_thread is not None:
            self.resolver_thread.start()

    @staticmethod
    def draw_figure(canvas, figure):
        """
        Embeds a Matplotlib figure in a PySimpleGUI Canvas Element
        """
        figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
        figure_canvas_agg.draw()
        figure_canvas_agg.get_tk_widget().grid(row=3, column=0, sticky="nsew", columnspan=120)
        figure_canvas_agg.get_tk_widget().configure(width=520, height=500)
        return figure_canvas_agg

    def upload_to_cloud(self):
        yes_or_no = ['Yes', 'No']
        upload_layout_dic = {'ask_to_upload': {'widget_type': 'label', 'value': 'Do you want to stop or upload?'},
                             'upload': {'text': 'Upload:', 'value': yes_or_no[0], 'widget_type': 'combobox',
                                        'options': yes_or_no},
                             'env_choice': {'text': 'Select Environment:', 'value': 'prod', 'widget_type': 'combobox',
                                            'options': ['prod', 'test']}}
        upload_layout_dic_gui = WiliotGui(params_dict=upload_layout_dic, parent=self.main_gui.layout)
        upload_layout_dic_values_out = upload_layout_dic_gui.run()

        if upload_layout_dic_values_out:
            self.upload_flag = upload_layout_dic_values_out['upload'] == 'Yes'
            self.env_choice = upload_layout_dic_values_out['env_choice']

        if self.upload_flag:
            try:
                is_uploaded = upload_to_cloud_api(self.cmn, self.tester_type + '-test',
                                                  run_data_csv_name=self.final_path_run_data,
                                                  packets_data_csv_name=self.final_path_packets_data,
                                                  env=self.env_choice, is_path=True)

            except Exception as ee:
                is_uploaded = False
                self.upload_flag = is_uploaded
                self.logger.error(f"Exception occurred: {ee}")
                exit()

            if is_uploaded:
                self.logger.info("Successful upload")
            else:
                self.logger.info('Failed to upload the file')
                popup_message(msg="Run upload failed. Check exception error at the console"
                                  " and check Internet connection is available"
                                  " and upload logs manually", tk_frame=self.main_gui.layout, logger=self.logger)
            self.main_gui.on_close()
            self.upload_flag = is_uploaded
        else:
            self.logger.info('File was not uploaded')

    def error_popup(self, error_type):
        self.logger.warning(f'{error_type} connection error occurred')
        popup_message(msg=f'{error_type} Connection error occurred.\n' f'Yield test was stopped',
                      tk_frame=self.main_gui.layout, logger=self.logger)
        self.logger.info(f'User reacted to {error_type} connection error')

    def get_current_plot_title(self):
        yield_type = 'Advas Yield' if self.yield_type == 'Advas' else 'External Ids Yield'

        return f'{yield_type} of last {self.window_size} matrices'

    def init_graphs(self, gui, min_current, min_cumulative):
        # create the main figure and two subplots
        fig, (ax, axy) = plt.subplots(1, 2, figsize=(12, 7))
        fig.subplots_adjust(left=0.05, right=0.95, top=0.85, bottom=0.15, wspace=0.2)
        # initialize the first graph
        prev_tests = None
        prev_val = None
        ax.set_xlabel('Number of tags')
        ax.set_ylabel('Yield %')
        ax.set_ylim([-MIN_Y_FOR_PLOTS, MAX_Y_FOR_PLOTS])
        ax_y_ticks = np.arange(MIN_Y_FOR_PLOTS, MAX_Y_FOR_PLOTS + 10, FIRST_STEP_SIZE)
        ax.set_yticks(ax_y_ticks)
        plt.ion()
        ax.yaxis.grid(True)
        text_box = ax.text(0.18, 1.05,
                           f"{self.get_current_plot_title()}: 0.00 %",
                           transform=ax.transAxes, fontweight='bold')
        if user_inputs.get('min_current_line') == 'yes':
            ax.axhline(y=min_current, color='black', linestyle='--')
        # initialize the second graph
        prev_tests1 = None
        prev_val1 = None
        axy.set_xlabel('Number of tags')
        axy.set_ylabel('Yield %')
        axy.set_ylim([MIN_Y_FOR_PLOTS, MAX_Y_FOR_PLOTS])
        axy_y_ticks = np.arange(MIN_Y_FOR_PLOTS, MAX_Y_FOR_PLOTS + 10, FIRST_STEP_SIZE)
        axy.set_yticks(axy_y_ticks)
        plt.ion()
        axy.yaxis.grid(True)
        text_box1 = axy.text(0.18, 1.05, f"Cumulative Yield: 0.0 %", transform=axy.transAxes,
                             fontweight='bold')
        if prev_val:
            text_box1 = axy.text(0.18, 1.05, f"Cumulative Yield: {prev_val:.2f} %", transform=axy.transAxes,
                                 fontweight='bold')
        if user_inputs.get('min_cumulative_line') == 'yes':
            axy.axhline(y=min_cumulative, color='black', linestyle='--')

        canvas_elem1 = gui.layout
        self.fig_canvas_agg1 = self.draw_figure(canvas_elem1, fig)
        return ax, axy, prev_tests, prev_val, prev_tests1, prev_val1, text_box, text_box1

    def calc_current_value(self):
        if self.yield_type == 'Advas':
            return 100 * ((len(self.seen_advas) - self.curr_adva_for_log) / self.matrix_size)
        else:
            return 100 * ((len(self.external_ids) - self.curr_ex_id_for_log) / self.matrix_size)

    def update_params_for_current_graph(self):
        self.new_trigger_log_line(latest_adva=len(self.seen_advas) - self.curr_adva_for_log,
                                  size=self.matrix_size)
        self.curr_adva_for_log = len(self.seen_advas)
        self.curr_ex_id_for_log = len(self.external_ids)

    def update_current_graph(self, new_trigger_graph_update):
        curr_tests = new_trigger_graph_update.get('new_num_rows')
        curr_val = self.calc_current_value()
        if curr_val > 100:
            curr_val = SET_VALUE_MORE_THAN_100

        if not hasattr(self, 'current_status_text') or self.current_status_text is None:
            self.current_status_text = None
        if curr_val < new_trigger_graph_update.get('min_current'):
            status_message_current = f'Current yield is lower than {new_trigger_graph_update.get("min_current")}%'
            if self.current_status_text is None:
                self.current_status_text = \
                    new_trigger_graph_update.get('ax').text(0.5, -0.19, status_message_current,
                                                            transform=new_trigger_graph_update.get('ax').transAxes,
                                                            fontsize=12, color='red', fontweight='bold', ha='center')
            else:
                self.current_status_text.set_text(status_message_current)
        else:
            if self.current_status_text is not None:
                self.current_status_text.remove()
                self.current_status_text = None

        figure_color_current = 'red' if curr_val < new_trigger_graph_update.get('red_line_current') else 'blue'
        # Plot the first point only if it's the first update
        new_trigger_graph_update.get('ax').plot([new_trigger_graph_update.get('prev_tests'), curr_tests],
                                                [new_trigger_graph_update.get('prev_val'), curr_val],
                                                color=figure_color_current)
        prev_tests = curr_tests
        prev_val = curr_val
        new_trigger_graph_update.get('text_box').set_text(f"{self.get_current_plot_title()}: {curr_val} %")

        self.update_params_for_current_graph()

        return prev_tests, prev_val

    def update_cumulative_graph(self, cumulative_graph_update_args):
        curr_tests1 = cumulative_graph_update_args.get('new_num_rows')
        curr_val1 = self.get_adva_yield_result() if self.yield_type == 'Advas' else self.get_ex_yield_result()

        if curr_val1 > 100:
            curr_val1 = SET_VALUE_MORE_THAN_100

        if not hasattr(self, 'cumulative_status_text') or self.cumulative_status_text is None:
            self.cumulative_status_text = None
        if curr_val1 < cumulative_graph_update_args.get('min_cumulative') and self.get_number_of_tested() != 0:
            status_message_cumulative = \
                f'Cumulative yield is lower than {cumulative_graph_update_args.get("min_cumulative")}%'
            if self.cumulative_status_text is None:
                self.cumulative_status_text = cumulative_graph_update_args.get('axy').text(
                    0.5, -0.19, status_message_cumulative,
                    transform=cumulative_graph_update_args.get('axy').transAxes,
                    fontsize=12, color='red', fontweight='bold', ha='center')
            else:
                self.cumulative_status_text.set_text(status_message_cumulative)
        else:
            if self.cumulative_status_text is not None:
                self.cumulative_status_text.remove()
                self.cumulative_status_text = None
        figure_color_cumulative = 'red' if curr_val1 < cumulative_graph_update_args.get(
            'red_line_cumulative') else 'blue'
        cumulative_graph_update_args.get('axy').plot([cumulative_graph_update_args.get('prev_tests1'), curr_tests1],
                                                     [cumulative_graph_update_args.get('prev_val1'), curr_val1],
                                                     color=figure_color_cumulative)
        prev_tests1 = curr_tests1
        prev_val1 = curr_val1
        yield_type_str = 'Advas' if self.yield_type == 'Advas' else 'External Ids'
        cumulative_graph_update_args.get('text_box1').set_text(f"{yield_type_str} Cumulative Yield: {curr_val1:.2f}%")
        self.fig_canvas_agg1.draw()

        return prev_tests1, prev_val1

    def handling_advanced_settings_window(self, advanced_settings_inputs):
        self.logger.info('Advanced settings was pressed')
        advanced_layout_dict = {
            'current_min_y_value': {'text': 'Current" min y:', 'value': '', 'widget_type': 'entry'},
            'current_max_y_value': {'text': '"Current" max y:', 'value': '', 'widget_type': 'entry'},
            'current_size_value': {'text': '"Current" step:', 'value': '', 'widget_type': 'entry'},
            'cumulative_min_y_value': {'text': '"Cumulative" min y:', 'value': '', 'widget_type': 'entry'},
            'cumulative_max_y_value': {'text': '"Cumulative" max y', 'value': '', 'widget_type': 'entry'},
            'cumulative_size_value': {'text': '"Cumulative" step:', 'value': '', 'widget_type': 'entry'},
            'window_size': {'text': 'Window size:', 'value': '', 'widget_type': 'entry'},
            'yield_type': {'text': 'Yield type', 'value': self.yield_type, 'widget_type': 'combobox',
                           'options': ['Advas', 'External Ids']},
            'reset_button': {'text': 'Reset', 'value': '', 'widget_type': 'button'},
        }

        default_values = {
            'current_min_y_value': 0,
            'current_max_y_value': 120,
            'current_size_value': 10,
            'cumulative_min_y_value': 0,
            'cumulative_max_y_value': 120,
            'cumulative_size_value': 10,
            'window_size': 1,
            'yield_type': 'Advas',

        }

        def reset_button():
            self.logger.info("Reset values from advanced settings")
            for key in default_values:
                advanced_gui.update_widget(key, default_values[key])
                globals()[key] = default_values[key]

            advanced_settings_inputs.get('ax').set_ylim([advanced_settings_inputs.get('current_min_y_value'),
                                                         advanced_settings_inputs.get('current_max_y_value')])
            advanced_settings_inputs.get('ax').set_yticks(
                np.arange(advanced_settings_inputs.get('current_min_y_value'),
                          advanced_settings_inputs.get('current_max_y_value') + advanced_settings_inputs.get(
                              'current_size_value'),
                          advanced_settings_inputs.get('current_size_value')))

            advanced_settings_inputs.get('axy').set_ylim([advanced_settings_inputs.get('cumulative_min_y_value'),
                                                          advanced_settings_inputs.get('cumulative_max_y_value')])
            advanced_settings_inputs.get('axy').set_yticks(
                np.arange(advanced_settings_inputs.get('cumulative_min_y_value'),
                          advanced_settings_inputs.get('cumulative_max_y_value') + advanced_settings_inputs.get(
                              'cumulative_size_value'),
                          advanced_settings_inputs.get('cumulative_size_value')))
            self.main_gui.window_size = 1
            self.yield_type = 'Advas'

        advanced_gui = WiliotGui(params_dict=advanced_layout_dict, exit_sys_upon_cancel=False,
                                 parent=self.main_gui.layout)
        advanced_gui.set_button_command('reset_button', reset_button)
        user_out = advanced_gui.run()

        if not self.current_values:
            self.current_values = {
                'current_min_y_value': advanced_settings_inputs.get('current_min_y_value'),
                'current_max_y_value': advanced_settings_inputs.get('current_max_y_value'),
                'current_size_value': advanced_settings_inputs.get('current_size_value'),
                'cumulative_min_y_value': advanced_settings_inputs.get('cumulative_min_y_value'),
                'cumulative_max_y_value': advanced_settings_inputs.get('cumulative_max_y_value'),
                'cumulative_size_value': advanced_settings_inputs.get('cumulative_size_value'),
                'window_size': advanced_settings_inputs.get('window_size', 1),
                'yield_type': 'Advas',
            }

        def get_adv_value():
            if not adv_value.isdigit() and adv_value != '':
                popup_message(msg=f"A not-number character in {adv_key}", tk_frame=advanced_gui.layout,
                              logger=self.logger)
                return
            if adv_value != '':
                new_value = int(adv_value)  # if user wrote a value
            elif self.current_values[adv_key]:
                new_value = self.current_values[
                    adv_key]  # if the user did not write a value and not the first submit
            else:
                new_value = int(default_values[adv_key])  # if the user did not write a value and first submit
            return new_value

        if user_out:
            self.main_gui.layout.attributes('-alpha', 1.0)
            for adv_key, adv_value in user_out.items():
                if adv_value and adv_key != 'window_size' and adv_key != 'yield_type':
                    new_value = get_adv_value()
                else:
                    if adv_key == 'yield_type':
                        new_value = adv_value
                        self.current_values[adv_key] = new_value
                        if self.yield_type != new_value:
                            for line in advanced_settings_inputs.get('ax').get_lines():
                                line.remove()
                            for line in advanced_settings_inputs.get('axy').get_lines():
                                line.remove()
                            self.yield_type = new_value
                    else:
                        new_value = int(get_adv_value())
                        self.window_size = new_value
                        self.main_gui.window_size = new_value
                self.current_values[adv_key] = new_value
                self.logger.info(f"{adv_key} changed to {new_value}")
            advanced_settings_inputs.get('ax').set_ylim(
                [self.current_values['current_min_y_value'], self.current_values['current_max_y_value']])
            advanced_settings_inputs.get('ax').set_yticks(np.arange(self.current_values['current_min_y_value'],
                                                                    self.current_values['current_max_y_value'] +
                                                                    self.current_values[
                                                                        'current_size_value'],
                                                                    self.current_values['current_size_value']))

            advanced_settings_inputs.get('axy').set_ylim(
                [self.current_values['cumulative_min_y_value'], self.current_values['cumulative_max_y_value']])
            advanced_settings_inputs.get('axy').set_yticks(np.arange(self.current_values['cumulative_min_y_value'],
                                                                     self.current_values['cumulative_max_y_value'] +
                                                                     self.current_values[
                                                                         'cumulative_size_value'],
                                                                     self.current_values['cumulative_size_value']))
            advanced_settings_inputs.get('text_box').set_text(
                f"{self.get_current_plot_title()}: {self.calc_current_value()} %")
            self.fig_canvas_agg1.draw()

    def get_number_of_tested(self):
        if ARDUINO_EXISTS:
            tags_num = self.count_process.get_tested()
        else:
            tags_num = self.adva_process.get_sensors_triggers() * int(self.thermodes_col) * int(self.rows_number)
        return tags_num

    def stop_or_error_process(self):
        end_time = datetime.datetime.now()
        run_end_time = end_time.strftime("%H:%M:%S")
        if self.upload_flag:
            upload_date = run_end_time
        else:
            upload_date = ''
        advas = len(self.seen_advas)
        tags_num = self.get_number_of_tested()
        result = float(100 * (advas / tags_num)) if tags_num != 0 else float('inf')
        self.stop_button(run_end_time, tags_num, advas, result, upload_date)
        return True

    def new_trigger_log_line(self, latest_adva, size):
        yield_result = "%.5f" % self.get_adva_yield_result()

        if '.' in yield_result and len(yield_result.split('.')[0]) < 2:
            yield_result = "0" + yield_result
        latest_yield_formatted = "{:.5f}".format(float(latest_adva / size) * 100).zfill(9)
        if ARDUINO_EXISTS:
            matrix_num = self.count_process.get_tested() / size
            all_tested = self.count_process.get_tested()
        else:
            matrix_num = self.adva_process.get_sensors_triggers()
            all_tested = self.adva_process.get_sensors_triggers() * size
        self.logger.info(
            'Matrix Number: %05d, Cumulative Yield: %s, Cumulative Tags: %05d, Cumulative Advas: %05d,'
            'Latest Yield: %s, Latest Tags: %05d, Latest Advas: %05d, Light Intensity: '
            '%05.1f, Humidity: %05.1f, Temperature: %05.1f',
            matrix_num, yield_result, all_tested, len(self.seen_advas), latest_yield_formatted,
            size, latest_adva, self.light_intensity, self.humidity, self.temperature)

    def new_trigger_sensors(self, new_trigger_user_configs):

        temperature_display = f"{self.temperature:.2f} °C"
        if self.main_sensor:
            self.light_intensity = self.main_sensor.get_light()
            self.humidity = self.main_sensor.get_humidity()
            self.temperature = self.main_sensor.get_temperature()
        if new_trigger_user_configs.get('temperature_type') == "F":
            temperature_display = f"{self.temperature * 9 / 5 + 32:.2f} °F"
        temperature_color = BLACK_COLOR if (new_trigger_user_configs.get('min_temperature') <= self.temperature <=
                                            new_trigger_user_configs.get('max_temperature')) else RED_COLOR
        light_intensity_color = BLACK_COLOR if (
                new_trigger_user_configs.get('min_light_intensity') <= self.light_intensity <=
                new_trigger_user_configs.get('max_light_intensity')) else RED_COLOR
        humidity_color = BLACK_COLOR if (new_trigger_user_configs.get('min_humidity') <= self.humidity <=
                                         new_trigger_user_configs.get('max_humidity')) else RED_COLOR
        self.main_gui.update_widget('sensor_row_temperature_value', f'Temperature: {temperature_display}',
                                    color=temperature_color)
        self.main_gui.update_widget('sensor_row_light_intensity_value',
                                    f'Light Intensity: {self.light_intensity} lux',
                                    color=light_intensity_color)
        self.main_gui.update_widget('sensor_row_humidity_value', f'Humidity: {self.humidity} %',
                                    color=humidity_color)

    def overlay_window(self):
        """
        The small window open session
        """
        # taking values from user_input json file
        temperature_type = user_inputs.get('temperature_type', default_user_inputs['temperature_type'])
        min_current = float(user_inputs.get('min_current', default_user_inputs['min_current']))
        min_cumulative = float(user_inputs.get('min_cumulative', default_user_inputs['min_cumulative']))
        min_humidity = float(user_inputs.get('min_humidity', default_user_inputs['min_humidity']))
        max_humidity = float(user_inputs.get('max_humidity', default_user_inputs['max_humidity']))
        max_light_intensity = float(user_inputs.get('max_light_intensity', default_user_inputs['max_light_intensity']))
        min_light_intensity = float(user_inputs.get('min_light_intensity', default_user_inputs['min_light_intensity']))
        min_temperature = float(user_inputs.get('min_temperature', default_user_inputs['min_temperature']))
        max_temperature = float(user_inputs.get('max_temperature', default_user_inputs['max_temperature']))
        red_line_current = float(user_inputs.get('red_line_current', default_user_inputs['red_line_current']))
        red_line_cumulative = float(user_inputs.get('red_line_cumulative', default_user_inputs['red_line_cumulative']))

        # creating the main window
        temp_val = self.temperature if temperature_type == "C" else self.temperature * 9 / 5 + 32
        overlay_layout_dict = {
            'counting_row': [{'num_rows': {'text': '', 'widget_type': 'label', 'value': 'Number of tags:',
                                           'options': {'font': ('Arial', 26, 'bold')}}},
                             {'num_advas': {'text': '', 'widget_type': 'label', 'value': 'Number of advas:',
                                            'options': {'font': ('Arial', 26, 'bold')}}},
                             ],

            'sensor_row': [{'light_intensity_value': {'text': '', 'widget_type': 'label',
                                                      'options': {'font': ('Arial', 14, 'bold')},
                                                      'value': f'Light Intensity: {self.light_intensity}'}},
                           {'temperature_value': {'widget_type': 'label', 'options': {'font': ('Arial', 14, 'bold')},
                                                  'value': f'Temperature: {temp_val} {temperature_type}'}},
                           {'humidity_value': {'widget_type': 'label', 'value': f'Humidity: {self.humidity}',
                                               'options': {'font': ('Arial', 14, 'bold')}, }
                            }, ],

            'space': {'value': '', 'widget_type': 'label'},
            'buttons_row': [
                {'advanced_settings_button': {'text': 'Advanced Settings', 'value': '', 'widget_type': 'button'}},
                {'stop_button': {'text': 'Stop', 'value': '', 'widget_type': 'button'}},
                {'pause_button': {'text': 'Pause Test', 'value': '', 'widget_type': 'button'}}]

        }
        if self.user_input['do_resolve']:
            overlay_layout_dict['counting_row'].append(
                {'num_ex_ids': {'text': '', 'widget_type': 'label', 'value': 'Number of external ids:',
                                'options': {'font': ('Arial', 26, 'bold')}}}
            )

        def stop_button_callback():
            self.stop.set()
            final_tags = self.get_number_of_tested()
            self.logger.info('Final Yield: %s, Final Tags: %05d, Final Advas: %05d,',
                             self.get_adva_yield_result(), final_tags, len(self.seen_advas), )
            self.upload_to_cloud()
            self.stop_run = self.stop_or_error_process()

        def toggle_test_callback():
            self.test_started = not self.test_started
            if ARDUINO_EXISTS:
                self.count_process.set_pause_triggers(not self.test_started)
            self.adva_process.set_stopped_by_user(not self.test_started)
            if self.test_started:
                self.logger.info('Test was started by user')
                self.main_gui.update_widget('buttons_row_pause_button', 'Pause Test')

            else:
                self.logger.info('Test was paused by user')
                self.main_gui.update_widget('buttons_row_pause_button', 'Start Test')

        # values before running
        self.curr_adva_for_log = len(self.seen_advas)
        self.curr_ex_id_for_log = len(self.external_ids)
        sub = False
        current_min_y_value = MIN_Y_FOR_PLOTS
        current_max_y_value = MAX_Y_FOR_PLOTS
        current_size_value = FIRST_STEP_SIZE
        cumulative_min_y_value = MIN_Y_FOR_PLOTS
        cumulative_max_y_value = MAX_Y_FOR_PLOTS
        cumulative_size_value = FIRST_STEP_SIZE
        result = float('inf')

        self.main_gui = WiliotGui(params_dict=overlay_layout_dict, full_screen=True, do_button_config=False)
        # initializing graphs
        ax, axy, prev_tests, prev_val, prev_tests1, prev_val1, text_box, text_box1 = \
            self.init_graphs(self.main_gui, min_current, min_cumulative)
        advanced_settings_inputs = {
            'ax': ax,
            'current_min_y_value': current_min_y_value,
            'current_max_y_value': current_max_y_value,
            'current_size_value': current_size_value,
            'axy': axy,
            'cumulative_min_y_value': cumulative_min_y_value,
            'cumulative_max_y_value': cumulative_max_y_value,
            'cumulative_size_value': cumulative_size_value,
            'window_size': self.window_size,
            'text_box': text_box,
        }
        advanced_settings_callback = partial(
            self.handling_advanced_settings_window, advanced_settings_inputs)

        self.main_gui.set_button_command('buttons_row_advanced_settings_button', advanced_settings_callback)
        self.main_gui.set_button_command('buttons_row_stop_button', stop_button_callback)
        self.main_gui.set_button_command('buttons_row_pause_button', toggle_test_callback)

        # initialize num_advas and num_rows
        num_rows = 0
        num_advas = 0
        self.main_gui.update_widget('counting_row_num_rows', f"Number of tags: {num_rows}")
        self.main_gui.update_widget('counting_row_num_advas', f"Number of advas: {num_advas}")
        if self.user_input['do_resolve']:
            self.main_gui.update_widget('counting_row_num_ex_ids', f"Number of external ids: {len(self.external_ids)}")

        def update_gui():
            nonlocal num_rows, num_advas, prev_tests, prev_val, prev_tests1, prev_val1, result, sub

            new_num_rows = self.get_number_of_tested()
            new_num_advas = len(self.seen_advas)
            self.not_neg_advas = new_num_advas

            # update packet data
            self.update_packet_data()

            if self.user_input['do_resolve']:
                self.main_gui.update_widget('counting_row_num_ex_ids',
                                            f"Number of external ids: {len(self.external_ids)}")

            # updating number of rows in GUI
            if new_num_rows != num_rows:
                num_rows = new_num_rows
                self.main_gui.update_widget('counting_row_num_rows', f"Number of tags: {num_rows}")

            # updating number of advas in GUI
            if new_num_advas != num_advas and new_num_advas > 0:
                num_advas = new_num_advas
                self.main_gui.update_widget('counting_row_num_advas', f"Number of advas: {num_advas}")

            # all processes when getting a new matrix
            curr_triggers_count = self.adva_process.get_sensors_triggers() if not ARDUINO_EXISTS \
                else self.count_process.get_matrix_cnt()
            triggers_diff = curr_triggers_count - self.trigger_count
            if triggers_diff > int(self.window_size) - 1:  # not using == or >=
                self.trigger_count = curr_triggers_count
                new_trigger_graph_update = {
                    'text_box': text_box,
                    'ax': ax,
                    'new_num_rows': new_num_rows,
                    'min_current': min_current,
                    'red_line_current': red_line_current,
                    'prev_tests': prev_tests,
                    'prev_val': prev_val,
                }
                new_trigger_user_configs = {
                    'temperature_type': temperature_type,
                    'min_temperature': min_temperature,
                    'max_temperature': max_temperature,
                    'min_light_intensity': min_light_intensity,
                    'max_light_intensity': max_light_intensity,
                    'min_humidity': min_humidity,
                    'max_humidity': max_humidity,

                }
                self.new_trigger_sensors(new_trigger_user_configs=new_trigger_user_configs)
                # updating the first graph
                prev_tests, prev_val = self.update_current_graph(new_trigger_graph_update)

            # updating the second graph
            cumulative_graph_args = {
                'axy': axy,
                'new_num_rows': new_num_rows,
                'min_cumulative': min_cumulative,
                'red_line_cumulative': red_line_cumulative,
                'prev_tests1': prev_tests1,
                'prev_val1': prev_val1,
                'text_box1': text_box1
            }
            prev_tests1, prev_val1 = self.update_cumulative_graph(cumulative_graph_update_args=cumulative_graph_args)

            end_time = datetime.datetime.now()
            run_end_time = end_time.strftime("%H:%M:%S")
            advas = len(self.seen_advas)
            tags_num = self.get_number_of_tested()
            result = float(100 * (advas / tags_num)) if tags_num != 0 else float('inf')
            self.update_run_data_file(formatted_date + ' ' + run_end_time, tags_num, advas, result)
            if self.adva_process.get_gw_error_connection() or \
                    (ARDUINO_EXISTS and self.count_process.get_arduino_connection_error()):
                if ARDUINO_EXISTS:
                    if self.count_process.get_arduino_connection_error():
                        self.user_response_after_arduino_connection_error = True
                        self.logger.warning('User responded to Arduino error')
                self.user_response_after_gw_connection_error = True
                self.logger.warning('User responded to GW error')
                self.stop_or_error_process()
            if self.user_response_after_gw_connection_error:
                connection_error = 'GW'
                self.error_popup(connection_error)
                self.upload_to_cloud()
                end_time = datetime.datetime.now()
                run_end_time = end_time.strftime("%H:%M:%S")
                if self.upload_flag:
                    upload_date = run_end_time
                else:
                    upload_date = ''
                self.update_run_data_file(formatted_date + ' ' + run_end_time, self.get_number_of_tested(),
                                          len(self.seen_advas), result, upload_date)
                self.main_gui.on_close()

            if sub or self.stop_run:
                self.stop_or_error_process()
                time.sleep(1)
                self.adva_process_thread.join()
                sys.exit()

        self.main_gui.add_recurrent_function(100, update_gui)
        self.main_gui.run()

    @staticmethod
    def open_session_layout(previous_input, inlay_info):

        open_session_layout = {
            'wafer_lot': {'text': 'Wafer Lot:', 'value': previous_input['wafer_lot'], 'widget_type': 'entry'},
            'wafer_num': {'text': 'Wafer Number:', 'value': previous_input['wafer_num'], 'widget_type': 'entry'},
            'thermodes_col': {'text': 'Number of Columns:', 'value': previous_input['thermodes_col'],
                              'widget_type': 'entry'},
            'matrix_tags': {'text': '', 'widget_type': 'label',
                            'value': f'Matrix tags: {str(inlay_info["default_matrix_tags"])}'},
            'inlay_dict': [
                {'inlay': {'text': 'Inlay:', 'value': previous_input['inlay_dict_inlay'], 'widget_type': 'combobox',
                           'options': list(inlays.keys())}},
                {'inlay_info': {'widget_type': 'label', 'value': inlay_info['inlay_info']}},
            ],
            'tester_station_name': {'text': 'Tester Station:', 'value': previous_input['tester_station_name'],
                                    'widget_type': 'entry'},
            'comments': {'text': 'Comments:', 'value': previous_input['comments'], 'widget_type': 'entry'},
            'operator': {'text': 'Operator:', 'value': previous_input['operator'], 'widget_type': 'entry'},
            'conversion_type': {'text': 'Conversion:', 'value': previous_input['conversion_type'],
                                'widget_type': 'combobox', 'options': inlay_info["conv_opts"]},
            'surface': {'text': 'Surface:', 'value': previous_input['surface'], 'widget_type': 'combobox',
                        'options': inlay_info["surfaces"]},
            'window_size': {'text': 'Window Size for Analysis:', 'value': previous_input['window_size'],
                            'widget_type': 'entry'},
            'do_resolve': {'text': 'Get External Id from Cloud', 'value': previous_input['do_resolve']},
            'owner_id': {'text': 'Owner Id for Cloud Connection', 'value': previous_input['owner_id']},

        }

        return open_session_layout

    def setup_inlay_parameters(self, values_out, energy_pat, time_pro, thermodes_col=None, rows_num=None,
                               yield_tester_type='assembly_yield_tester'):
        selected_inlay = inlays.get(self.selected)
        self.user_input = values_out
        self.rows_number = int(selected_inlay['number_of_rows']) if rows_num is None else rows_num
        self.wafer_lot = values_out.get('wafer_lot', '')
        self.wafer_number = values_out.get('wafer_num', '')
        self.window_size = values_out.get('window_size', 1)
        self.comments = values_out['comments']
        self.gw_energy_pattern = energy_pat
        self.gw_time_profile = time_pro
        self.thermodes_col = values_out.get('thermodes_col', 1) if thermodes_col is None else thermodes_col
        self.conversion_type = values_out['conversion_type']
        self.surface = values_out['surface']
        self.tester_station_name = values_out['tester_station_name']
        self.operator = values_out['operator']
        self.matrix_size = int(self.thermodes_col) * int(self.rows_number)
        self.setup_logger(yield_tester_type)

        try:
            self.main_sensor = YoctoSensor(self.logger)
        except Exception as ee:
            self.main_sensor = None
            print(f'No sensor is connected ({ee})')
        if self.main_sensor:
            self.light_intensity = self.main_sensor.get_light()
            self.humidity = self.main_sensor.get_humidity()
            self.temperature = self.main_sensor.get_temperature()
        else:
            self.temperature = VALUE_WHEN_NO_SENSOR
            self.humidity = VALUE_WHEN_NO_SENSOR
            self.light_intensity = VALUE_WHEN_NO_SENSOR

        self.start_run = True

    def open_session(self, cols_or_rows='thermodes_col'):
        """
        Opening a session for the process
        """
        # Load previous input from the config file
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r") as f:
                self.previous_input = json.load(f)

        for k, v in DEFAULT_USER_INPUT.items():
            if k not in self.previous_input.keys():
                self.previous_input[k] = v

        self.start_run = False
        self.selected = self.previous_input['inlay_dict_inlay']
        selected_inlay = inlays.get(self.selected, {})
        energy_pat = selected_inlay.get('energy_pattern_val', 'Invalid Selection')
        time_pro = selected_inlay.get('time_profile_val', 'Invalid Selection')
        default_matrix_tags = int(self.previous_input.get('thermodes_col', 1))

        inlay_info_dict = {
            'inlay_info': ',   '.join(f"{key}: {value}" for key, value in selected_inlay.items() if
                                      key != 'inlay' and key != 'number' and key != 'number_of_rows'),
            'default_matrix_tags': default_matrix_tags,
            'conv_opts': ['Not converted', 'Standard', 'Durable'],
            'surfaces': ['Air', 'Cardboard', 'RPC', 'General Er3', 'General Er3.5']
        }

        open_session_layout = self.open_session_layout(previous_input=self.previous_input, inlay_info=inlay_info_dict)

        open_session_gui = WiliotGui(params_dict=open_session_layout, do_button_config=False)

        def on_inlay_change(*args):
            inlay_var = open_session_gui.widgets_vals['inlay_dict_inlay']
            inlay_select = inlay_var.get()
            self.selected = inlay_select
            if inlay_select in inlays:
                selected_inlay = inlays[inlay_select]
                inlay_info = inlays[self.selected]
                info_string = ',   '.join(
                    f"{key}: {value}" for key, value in inlay_info.items() if
                    key != 'inlay' and key != 'number' and key != 'number_of_rows')
                thermodes_col_value = open_session_gui.widgets_vals.get('thermodes_col')
                if thermodes_col_value is not None:
                    default_matrix_tags = int(thermodes_col_value.get()) * selected_inlay.get('number_of_rows', 1)
                else:
                    default_matrix_tags = selected_inlay.get('number_of_rows', 1)
            else:
                info_string = 'Invalid Selection'
                default_matrix_tags = 0

            open_session_gui.update_widget('inlay_dict_inlay_info', info_string)
            if 'matrix_tags' in open_session_gui.widgets.keys():
                open_session_gui.update_widget('matrix_tags', f'Matrix tags: {str(default_matrix_tags)}')

        def on_cols_change(*args):
            nonlocal default_matrix_tags
            inlay_var = open_session_gui.widgets_vals['inlay_dict_inlay']
            inlay = inlay_var.get() if inlay_var.get() != '' and inlay_var.get() in inlays.keys() else list(inlays)[0]
            selected_inlay = inlays[inlay]
            cols_str = open_session_gui.widgets_vals.get('thermodes_col')
            rows_str = open_session_gui.widgets_vals.get('rows_num')
            cols_num = cols_str.get() if cols_str is not None else 1
            rows_num = int(rows_str.get()) if rows_str is not None else selected_inlay.get('number_of_rows')
            default_matrix_tags = cols_num * rows_num
            if 'matrix_tags' in open_session_gui.widgets.keys():
                open_session_gui.update_widget('matrix_tags', f'Matrix tags: {str(default_matrix_tags)}')
            if 'parts_row_part_1' in open_session_gui.widgets.keys():
                for i in range(1, 4):
                    open_session_gui.update_widget(f'parts_row_part_{i}', disabled=(i > rows_num))

        def submit_open_session(*args):
            wafer_number = ''
            wafer_lot = ''
            wafer_number_widget = open_session_gui.widgets.get('wafer_num')
            if wafer_number_widget is not None:
                wafer_number = wafer_number_widget.get()
            wafer_lot_widget = open_session_gui.widgets.get('wafer_lot')
            if wafer_lot_widget is not None:
                wafer_lot = wafer_lot_widget.get()
            missing_fields = []
            self.filling_missed_field = []
            for field in MAND_FIELDS:
                if open_session_gui.widgets.get(field) is not None:
                    session_value = open_session_gui.widgets.get(field).get().strip()
                    if not session_value:
                        missing_fields.append(field)
                        self.filling_missed_field.append(field)
            if missing_fields:
                error_msg = f"Please fill all the " \
                            f"mandatory fields {', '.join([f'[{field}]' for field in missing_fields])}"
                popup_message(msg=error_msg, tk_frame=open_session_gui.layout, logger=self.logger)
                return  # Skip the rest and prompt for missing fields again
            for missed_field in self.filling_missed_field:
                setattr(self, missed_field, open_session_gui.widgets.get(missed_field).get().strip())

            for value, value_name in [(wafer_lot, "Wafer lot"), (wafer_number, "Wafer number")]:
                for character in value:
                    if not character.isalpha() and not character.isdigit():
                        popup_message(msg=f"{value_name} can't include '{character}' not letter/digit",
                                      tk_frame=open_session_gui.layout, logger=self.logger)
                        return
            open_session_gui.on_submit()

        open_session_gui.button_configs(submit_command=submit_open_session)
        open_session_gui.add_event(widget_key='inlay_dict_inlay', command=on_inlay_change)
        open_session_gui.add_event(widget_key=cols_or_rows, command=on_cols_change)

        on_cols_change()
        values_out = open_session_gui.run(save_path=CONFIG_FILE)

        if values_out:
            self.setup_inlay_parameters(values_out, energy_pat, time_pro)
            # Save the correct values to previous_input
            # self.saving_prev_input(values_out)


if __name__ == '__main__':
    m = MainWindow()
    m.run()
