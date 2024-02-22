from csv import DictReader, DictWriter
from os.path import isfile
from math import isnan


#####################################################################################################
class TappingDataLogger:

    def __init__(self, csv_dir, part_id, alpha_id, traj_id, rhythm_id, tempo, 
                 error, errp, ref_times, recorded_times, times_from_start, error_list, errp_list):
        
        self.csv_dir = csv_dir
        self.part_id = part_id
        self.alpha_id = alpha_id
        self.traj_id = traj_id
        self.rhythm_id = rhythm_id
        self.tempo = tempo
        
        self.error = error
        self.errp = errp
        self.ref_times = ref_times
        self.recorded_times = recorded_times
        self.times_from_start = times_from_start
        self.error_list = error_list
        self.errp_list = errp_list

        self.file_name = self.csv_dir + "\part" + str(self.part_id) + ".csv"
        self.file_field_names = ['trial_number', 'alpha_id', 'traj_id', 'rhythm_id', 'tempo', 'ave. error', 'ave. error (%)',
                                 'ref_times', 'recorded_times', 'times_from_start', 'error_list', 'errp_list']


    ##############################################################################
    def log_data(self):

        # check if the header file already exists
        file_exists = isfile(self.file_name)
        
        # initialize the trial ID to 1 if the file doesn't exist
        trial_id = 1
        
        # if the file exists, read the last trial ID and increment it
        if file_exists:
            with open(self.file_name, 'r', newline='') as f:
                reader = DictReader(f)
                for row in reader:
                    trial_id = int(row[self.file_field_names[0]]) + 1

        # open the file in append mode
        with open(self.file_name, 'a', newline='') as f:

            # dictionary that we want to add as a new row
            new_trial_data = {self.file_field_names[0]: trial_id,
                              self.file_field_names[1]: self.alpha_id,
                              self.file_field_names[2]: self.traj_id,
                              self.file_field_names[3]: self.rhythm_id,
                              self.file_field_names[4]: self.tempo,
                              self.file_field_names[5]: self.error,
                              self.file_field_names[6]: self.errp,
                              self.file_field_names[7]: self.ref_times,
                              self.file_field_names[8]: self.recorded_times,
                              self.file_field_names[9]: self.times_from_start,
                              self.file_field_names[10]: self.error_list,
                              self.file_field_names[11]: self.errp_list
            }

            writer = DictWriter(f, fieldnames=self.file_field_names)
            # write the header row if the file doesn't exist
            if not file_exists:
                writer.writeheader()
            
            # write the data to the file
            writer.writerow(new_trial_data)

        print("\nSuccesfully opened file %s to write tapping data !!!\n" % self.file_name)




#####################################################################################################
class EyeDataLogger:

    def __init__(self, csv_dir, part_id, alpha_id, traj_id, rhythm_id, tempo, 
                 left_gaze_points, right_gaze_points, left_pupil_sizes, right_pupil_sizes):
        
        self.csv_dir = csv_dir
        self.part_id = part_id
        self.alpha_id = alpha_id
        self.traj_id = traj_id
        self.rhythm_id = rhythm_id
        self.tempo = tempo
        
        self.left_gaze_points = left_gaze_points
        self.right_gaze_points = right_gaze_points
        self.left_pupil_sizes = left_pupil_sizes
        self.right_pupil_sizes = right_pupil_sizes

        self.file_name = self.csv_dir + "\part" + str(self.part_id) + ".csv"
        self.file_field_names = ['trial_number', 'alpha_id', 'traj_id', 'rhythm_id', 'tempo', 'left_ave_size', 'right_ave_size',
                                 'left_points', 'right_points', 'left_sizes', 'right_sizes']

    
    ##############################################################################
    def calc_averages(self):
        
        left_sum = 0.0
        left_count = 0
        for i in range(len(self.left_pupil_sizes)):
            if not isnan(self.left_pupil_sizes[i]):
                left_sum += self.left_pupil_sizes[i]
                left_count += 1
                
        right_sum = 0.0
        right_count = 0
        for i in range(len(self.right_pupil_sizes)):
            if not isnan(self.right_pupil_sizes[i]):
                right_sum += self.right_pupil_sizes[i]
                right_count += 1
        
        if left_count > 0:
            self.left_ave = left_sum / left_count
        else:
            self.left_ave = 0.0
        if right_count > 0:
            self.right_ave = right_sum / right_count
        else:
            self.right_ave = 0.0
        

    ##############################################################################
    def log_data(self):

        # check if the header file already exists
        file_exists = isfile(self.file_name)
        
        # initialize the trial ID to 1 if the file doesn't exist
        trial_id = 1
        
        # if the file exists, read the last trial ID and increment it
        if file_exists:
            with open(self.file_name, 'r', newline='') as f:
                reader = DictReader(f)
                for row in reader:
                    trial_id = int(row[self.file_field_names[0]]) + 1

        # open the file in append mode
        with open(self.file_name, 'a', newline='') as f:

            # dictionary that we want to add as a new row
            new_trial_data = {self.file_field_names[0]: trial_id,
                              self.file_field_names[1]: self.alpha_id,
                              self.file_field_names[2]: self.traj_id,
                              self.file_field_names[3]: self.rhythm_id,
                              self.file_field_names[4]: self.tempo,
                              self.file_field_names[5]: self.left_ave,
                              self.file_field_names[6]: self.right_ave,
                              self.file_field_names[7]: self.left_gaze_points,
                              self.file_field_names[8]: self.right_gaze_points,
                              self.file_field_names[9]: self.left_pupil_sizes,
                              self.file_field_names[10]: self.right_pupil_sizes
            }

            writer = DictWriter(f, fieldnames=self.file_field_names)
            # write the header row if the file doesn't exist
            if not file_exists:
                writer.writeheader()
            
            # write the data to the file
            writer.writerow(new_trial_data)

        print("\nSuccesfully opened file %s to write eye data !!!\n" % self.file_name)


############################# FUNCTIONS TO GET RHYTHM TIMESTAMPS ############################

# rhythm 1 (tap, rest, tap, rest)
# rhythm 2 (tap, tap, rest, rest)
# rhythm 3 (tap, tap, rest, tap)
# rhythm 4 (tap, rest, tap, tap)
# rhythm 5 (tap, rest, tap, rest, tap, tap, tap, rest)
# rhythm 6 (tap, rest, tap, tap, rest, tap, tap, rest)

def get_intervals(base_interval, rhythm_id):
    match rhythm_id:
        case 1:
            interval_counts = [2, 2]
        case 2:
            interval_counts = [1, 3]
        case 3:
            interval_counts = [1, 2, 1]
        case 4:
            interval_counts = [2, 1, 1]
        case 5:
            interval_counts = [2, 2, 1, 1, 2]
        case 6:
            interval_counts = [2, 1, 2, 1, 2]
            
    num_intervals = len(interval_counts)
    intervals = [interval_counts[i] * base_interval for i in range(num_intervals)]
    return num_intervals, intervals


def get_timestamps(tempo, max_time, rhythm_id):
    # base interval length = 60 / tempo [in seconds]
    base_interval = float(60 / tempo)
    num_intervals, intervals = get_intervals(base_interval, rhythm_id)
    time_stamps = []
    timer = 0.0
    interval_index = 0
    while timer <= max_time:
        time_stamps.append(timer)
        timer += intervals[interval_index]
        if interval_index < num_intervals-1:
            interval_index += 1
        else:
            interval_index = 0
    return time_stamps
