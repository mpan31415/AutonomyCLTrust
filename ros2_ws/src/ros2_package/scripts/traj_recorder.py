#!/usr/bin/env python3

######################################################
######################################################
## FILE SUMMARY:
##
## - Python class definition of the TrajRecorder Node
##
## - The TrajRecorder subscribes to the positions of
##   human input, robot input, and the tcp pose
##   
## - Once the trial finishes, this node then creates
##   a DataLogger instance and passes all the recorded
##   trial information to it for logging to csv files
##
######################################################
######################################################

import rclpy
from rclpy.node import Node

from math import pi, sin

from tutorial_interfaces.msg import Falconpos
from tutorial_interfaces.msg import PosInfo
from std_msgs.msg import Bool

from ros2_package.data_logger import DataLogger
from ros2_package.traj_utils import get_sine_ref_points

from datetime import datetime
from time import time


ORIGIN = [0.5059, 0.0, 0.4346]   # this is in [meters]

ALL_CSV_DIR = "{CSV_DIRECTORY}"

LOG_DATA = True


# sin curve parameters 
TRAJ_DICT_LIST = [
    {'a': 1, 'b': 1, 'c': 4, 's': pi,     'h': 0.25},
    {'a': 2, 'b': 3, 'c': 4, 's': 4*pi/3, 'h': 0.25},
    {'a': 1, 'b': 3, 'c': 4, 's': pi,     'h': 0.25},
    {'a': 2, 'b': 2, 'c': 5, 's': pi,     'h': 0.2},
    {'a': 2, 'b': 3, 'c': 5, 's': 8*pi/5, 'h': 0.2},
    {'a': 2, 'b': 4, 'c': 5, 's': pi,     'h': 0.2}
]

TRAJ_HEIGHT = 0.1
TRAJ_WIDTH = 0.3
TRAJ_DEPTH = 0.1


class TrajRecorder(Node):

    ##############################################################################
    def __init__(self):

        super().__init__('traj_recorder')

        # parameter stuff
        self.param_names = ['free_drive', 'mapping_ratio', 'use_depth', 'part_id', 'alpha_id', 'traj_id']
        self.declare_parameters(
            namespace='',
            parameters=[
                (self.param_names[0], 0),
                (self.param_names[1], 3.0),
                (self.param_names[2], 0),
                (self.param_names[3], 0),
                (self.param_names[4], 0),
                (self.param_names[5], 0)
            ]
        )
        (free_drive_param, mapping_ratio_param, use_depth_param, part_param, alpha_param, traj_param) = self.get_parameters(self.param_names)
        self.free_drive = free_drive_param.value
        self.mapping_ratio = mapping_ratio_param.value
        self.use_depth = use_depth_param.value
        self.part_id = part_param.value
        self.alpha_id = alpha_param.value
        self.traj_id = traj_param.value

        self.print_params()

        # get the reference trajectory points
        self.traj_params = TRAJ_DICT_LIST[self.traj_id]
        self.refx, self.refy, self.refz = get_sine_ref_points(200, self.traj_params['a'], self.traj_params['b'], self.traj_params['c'], 
                                                              self.traj_params['s'], self.traj_params['h'], TRAJ_HEIGHT, TRAJ_WIDTH, TRAJ_DEPTH, 
                                                              ORIGIN, self.use_depth)

        # tcp position subscriber
        self.tcp_pos_sub = self.create_subscription(PosInfo, 'tcp_position', self.tcp_pos_callback, 10)
        self.tcp_pos_sub  # prevent unused variable warning

        # record flag subscriber
        self.record_flag_sub = self.create_subscription(Bool, 'record', self.record_flag_callback, 10)
        self.record_flag_sub  # prevent unused variable warning

        # second last point subscriber
        self.slp_sub_ = self.create_subscription(Bool, 'last_point', self.lp_flag_callback, 10)
        self.slp_sub_  # prevent unused variable warning

        # flags to control data recording & plotting, and writing to csv file
        self.write_data = LOG_DATA
        self.record = False
        self.data_written = False

        self.last_point = False

        # do not log data if in free-drive mode
        if self.free_drive:
            self.write_data = False
        
        # do not log data if in full autonomy mode
        if self.alpha_id == 0:
            self.write_data = False
        
        # data points of the trajectory {reference, human, robot, total}
        self.refxs = []
        self.refys = []
        self.refzs = []

        self.hxs = []
        self.hys = []
        self.hzs = []

        self.rxs = []
        self.rys = []
        self.rzs = []

        self.txs = []
        self.tys = []
        self.tzs = []

        self.times_from_start = []
        self.times = []
        self.datetimes = []

        # file name of the csv sheet
        self.csv_dir = ALL_CSV_DIR + "part" + str(self.part_id) + "/"


    ##############################################################################
    def tcp_pos_callback(self, msg):
        
        if self.record:
            # self.get_logger().info('Recording the tcp position: x = %.3f, y = %.3f, z = %.3f ' % (msg.x, msg.y, msg.z))
            self.refxs.append(msg.ref_position[0])
            self.refys.append(msg.ref_position[1])
            self.refzs.append(msg.ref_position[2])

            self.hxs.append(msg.human_position[0])
            self.hys.append(msg.human_position[1])
            self.hzs.append(msg.human_position[2])

            self.rxs.append(msg.robot_position[0])
            self.rys.append(msg.robot_position[1])
            self.rzs.append(msg.robot_position[2])

            self.txs.append(msg.tcp_position[0])
            self.tys.append(msg.tcp_position[1])
            self.tzs.append(msg.tcp_position[2])

            self.times_from_start.append(msg.time_from_start)
            self.times.append(time())
            self.datetimes.append(datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))

            if self.last_point and not self.data_written:
                if self.write_data:
                    self.write_to_csv()
                    self.data_written = True


    ##############################################################################
    def record_flag_callback(self, msg):
        self.record = msg.data


    ##############################################################################
    def lp_flag_callback(self, msg):
        self.last_point = msg.data


    ##############################################################################
    def write_to_csv(self):

        dl = DataLogger(self.csv_dir, self.part_id, self.alpha_id, self.traj_id, self.refxs, self.refys, self.refzs, self.hxs, self.hys, self.hzs,
                        self.rxs, self.rys, self.rzs, self.txs, self.tys, self.tzs, self.times_from_start, self.times, self.datetimes)

        dl.calc_error(self.use_depth)

        dl.write_header()
        
        dl.log_data()

    
    ##############################################################################
    def print_params(self):
        print("\n" * 10)
        print("=" * 100)

        print("\n\nThe current parameters [traj_recorder] are as follows:\n")
        print("The free_drive flag = %d\n\n" % self.free_drive)
        print("The mapping_ratio = %d\n\n" % self.mapping_ratio)
        print("The use_depth = %d\n\n" % self.use_depth)
        print("The participant_id = %d\n\n" % self.part_id)
        print("The alpha_id = %d\n\n" % self.alpha_id)
        print("The trajectory_id = %d\n\n" % self.traj_id)

        print("=" * 100)
        print("\n" * 10)
        



##############################################################################
def main(args=None):

    rclpy.init(args=args)

    michael = TrajRecorder()

    rclpy.spin(michael)

    michael.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()