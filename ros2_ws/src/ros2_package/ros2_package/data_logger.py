######################################################
######################################################
## FILE SUMMARY:
##
## - Python class definition of DataLogger
##
## - The DataLogger instantiates with experimental conditions
##   used for any particular trial and the recorded trajectory
##   waypoints, and write them to two files:
##   
##   1. A new .csv file containing the raw trajectory waypoints
##      of that particular trial
##
##   2. Append a row of calculated error information to
##      the header file of the corresponding participant
##
######################################################
######################################################


from csv import writer, DictReader, DictWriter
from os.path import isfile
from math import sqrt


#####################################################################################################
class DataLogger:

    def __init__(self, csv_dir, part_id, alpha_id, traj_id, 
                 refxs, refys, refzs, hxs, hys, hzs, rxs, rys, rzs, txs, tys, tzs, 
                 times_from_start, times, datetimes):
        
        # trial info
        self.csv_dir = csv_dir
        self.part_id = part_id
        self.alpha_id = alpha_id
        self.traj_id = traj_id

        # reference
        self.refxs = refxs
        self.refys = refys
        self.refzs = refzs
        
        # human
        self.hxs = hxs
        self.hys = hys
        self.hzs = hzs
        self.num_points = len(self.hxs)

        # robot
        self.rxs = rxs
        self.rys = rys
        self.rzs = rzs

        # total (human + robot)
        self.txs = txs
        self.tys = tys
        self.tzs = tzs

        # other info
        self.times_from_start = times_from_start
        self.times = times
        self.datetimes = datetimes

        self.header_file_name = self.csv_dir + "part" + str(self.part_id) + "_header.csv"
        self.header_field_names = ['trial_number', 'alpha_id', 'traj_id', 'human_ave', 'robot_ave', 'overall_ave',
                                   'human_total', 'robot_total', 'overall_total', 'human_dim_ave', 'robot_dim_ave', 'overall_dim_ave', 
                                   'human_dim_total', 'robot_dim_total', 'overall_dim_total']


    ##############################################################################
    def calc_error(self, use_depth):
        
        ########################################### THESE GO INTO THE 400-LINE FILE ###########################################
        # human error lists in each dim
        self.hx_err_list = [abs(self.hxs[i] - self.refxs[i]) for i in range(self.num_points)]
        self.hy_err_list = [abs(self.hys[i] - self.refys[i]) for i in range(self.num_points)]
        self.hz_err_list = [abs(self.hzs[i] - self.refzs[i]) for i in range(self.num_points)]

        # robot error lists in each dim
        self.rx_err_list = [abs(self.rxs[i] - self.refxs[i]) for i in range(self.num_points)]
        self.ry_err_list = [abs(self.rys[i] - self.refys[i]) for i in range(self.num_points)]
        self.rz_err_list = [abs(self.rzs[i] - self.refzs[i]) for i in range(self.num_points)]

        # overall error lists in each dim
        self.tx_err_list = [abs(self.txs[i] - self.refxs[i]) for i in range(self.num_points)]
        self.ty_err_list = [abs(self.tys[i] - self.refys[i]) for i in range(self.num_points)]
        self.tz_err_list = [abs(self.tzs[i] - self.refzs[i]) for i in range(self.num_points)]

        # human, robot & overall Euclidean norm error list
        if use_depth:
            self.h_err_list = [sqrt((self.hx_err_list[i])**2 + (self.hy_err_list[i])**2 + (self.hz_err_list[i])**2) for i in range(self.num_points)]
            self.r_err_list = [sqrt((self.rx_err_list[i])**2 + (self.ry_err_list[i])**2 + (self.rz_err_list[i])**2) for i in range(self.num_points)]
            self.t_err_list = [sqrt((self.tx_err_list[i])**2 + (self.ty_err_list[i])**2 + (self.tz_err_list[i])**2) for i in range(self.num_points)]
        else:
            self.h_err_list = [sqrt((self.hy_err_list[i])**2 + (self.hz_err_list[i])**2) for i in range(self.num_points)]
            self.r_err_list = [sqrt((self.ry_err_list[i])**2 + (self.rz_err_list[i])**2) for i in range(self.num_points)]
            self.t_err_list = [sqrt((self.ty_err_list[i])**2 + (self.tz_err_list[i])**2) for i in range(self.num_points)]

        ########################################### THESE GO INTO THE HEADER FILE ###########################################

        # total human errors
        self.hx_err_total = sum(self.hx_err_list)
        self.hy_err_total = sum(self.hy_err_list)
        self.hz_err_total = sum(self.hz_err_list)
        self.h_dim_err_total = [self.hx_err_total, self.hy_err_total, self.hz_err_total]    # log this
        self.h_err_total = sum(self.h_err_list)                                             # log this

        # total robot errors
        self.rx_err_total = sum(self.rx_err_list)
        self.ry_err_total = sum(self.ry_err_list)
        self.rz_err_total = sum(self.rz_err_list)
        self.r_dim_err_total = [self.rx_err_total, self.ry_err_total, self.rz_err_total]    # log this
        self.r_err_total = sum(self.r_err_list)                                             # log this

        # total overall errors
        self.tx_err_total = sum(self.tx_err_list)
        self.ty_err_total = sum(self.ty_err_list)
        self.tz_err_total = sum(self.tz_err_list)
        self.t_dim_err_total = [self.tx_err_total, self.ty_err_total, self.tz_err_total]    # log this
        self.t_err_total = sum(self.t_err_list)                                             # log this

        # average human errors
        self.hx_err_ave = self.hx_err_total / self.num_points
        self.hy_err_ave = self.hy_err_total / self.num_points
        self.hz_err_ave = self.hz_err_total / self.num_points
        self.h_dim_err_ave = [self.hx_err_ave, self.hy_err_ave, self.hz_err_ave]            # log this
        self.h_err_ave = self.h_err_total / self.num_points                                 # log this

        # average robot errors
        self.rx_err_ave = self.rx_err_total / self.num_points
        self.ry_err_ave = self.ry_err_total / self.num_points
        self.rz_err_ave = self.rz_err_total / self.num_points
        self.r_dim_err_ave = [self.rx_err_ave, self.ry_err_ave, self.rz_err_ave]            # log this
        self.r_err_ave = self.r_err_total / self.num_points                                 # log this

        # average overall errors
        self.tx_err_ave = self.tx_err_total / self.num_points
        self.ty_err_ave = self.ty_err_total / self.num_points
        self.tz_err_ave = self.tz_err_total / self.num_points
        self.t_dim_err_ave = [self.tx_err_ave, self.ty_err_ave, self.tz_err_ave]            # log this
        self.t_err_ave = self.t_err_total / self.num_points                                 # log this


    ##############################################################################
    def write_header(self):

        # check if the header file already exists
        file_exists = isfile(self.header_file_name)
        
        # initialize the trial ID to 1 if the file doesn't exist
        trial_id = 1
        
        # if the file exists, read the last trial ID and increment it
        if file_exists:
            with open(self.header_file_name, 'r', newline='') as f:
                reader = DictReader(f)
                for row in reader:
                    trial_id = int(row[self.header_field_names[0]]) + 1

        # define the file name of the new trial
        self.data_file_name = self.csv_dir + "trial" + str(trial_id) + ".csv"

        # open the file in append mode
        with open(self.header_file_name, 'a', newline='') as f:

            # dictionary that we want to add as a new row
            new_trial_data = {self.header_field_names[0]: trial_id,
                              self.header_field_names[1]: self.alpha_id,
                              self.header_field_names[2]: self.traj_id,
                              self.header_field_names[3]: self.h_err_ave,
                              self.header_field_names[4]: self.r_err_ave,
                              self.header_field_names[5]: self.t_err_ave,
                              self.header_field_names[6]: self.h_err_total,
                              self.header_field_names[7]: self.r_err_total,
                              self.header_field_names[8]: self.t_err_total,
                              self.header_field_names[9]: self.h_dim_err_ave,
                              self.header_field_names[10]: self.r_dim_err_ave,
                              self.header_field_names[11]: self.t_dim_err_ave,
                              self.header_field_names[12]: self.h_dim_err_total,
                              self.header_field_names[13]: self.r_dim_err_total,
                              self.header_field_names[14]: self.t_dim_err_total
            }

            writer = DictWriter(f, fieldnames=self.header_field_names)
            # write the header row if the file doesn't exist
            if not file_exists:
                writer.writeheader()
            
            # write the data to the file
            writer.writerow(new_trial_data)

        print("\nSuccesfully opened file %s to write header !!!\n" % self.header_file_name)


    ##############################################################################
    def log_data(self):
        
        with open(self.data_file_name, 'w', newline='') as file:

            wr = writer(file)
            # write datapoints [recorded trajectory points]
            for i in range(self.num_points):
                wr.writerow([self.refxs[i], self.refys[i], self.refzs[i],       # this was added (for noisy robot), and a few below also
                             self.hxs[i], self.hys[i], self.hzs[i], self.rxs[i], self.rys[i], self.rzs[i],
                             self.txs[i], self.tys[i], self.tzs[i], self.h_err_list[i], self.h_err_list, self.t_err_list[i],
                             self.hx_err_list[i], self.hy_err_list[i], self.hz_err_list[i],
                             self.rx_err_list[i], self.ry_err_list[i], self.rz_err_list[i],
                             self.tx_err_list[i], self.ty_err_list[i], self.tz_err_list[i],
                             self.times_from_start[i], self.times[i], self.datetimes[i]])

            print("\nSuccesfully opened file %s and finished logging data !!!\n" % self.data_file_name)

