#!/usr/bin/env python3

from keyboard import read_key
from time import time
from os import getcwd
from utils import TappingDataLogger, EyeDataLogger, get_timestamps
from playsound import playsound
import tobii_research as tr
import matplotlib.pyplot as plt


###################################################################################
### Python implementation of "The Rhythm Method" from the 2015 paper.
### Eye-tracking recording is also run using this script simultaneously.
###################################################################################


###################   rhythms   ###################

# rhythm 1 (tap, rest, tap, rest)
# rhythm 2 (tap, tap, rest, rest)
# rhythm 3 (tap, tap, rest, tap)
# rhythm 4 (tap, rest, tap, tap)
# rhythm 5 (tap, rest, tap, rest, tap, tap, tap, rest)
# rhythm 6 (tap, rest, tap, tap, rest, tap, tap, rest)

SAVE_TAP_DATA = False
SAVE_EYE_DATA = False

###################   experiment settings   ###################

PART_ID = 0
ALPHA_ID = 0
TRAJ_ID = 0
RHYTHM_ID = 5


TEMPOS = [115, 120, 125, 130, 135]
TEMPO = TEMPOS[RHYTHM_ID - 1]

MAX_TIME = 10       # seconds

USE_EYETRACKER = False


##########################################################################################
class RhythmMethod():
    
    def __init__(self, log_tap_data, log_eye_data, part_id, alpha_id, traj_id, 
                 rhythm_id, tempo, max_time, use_eyetracker):
        
        self.use_eyetracker = use_eyetracker
        if self.use_eyetracker:
            self.found_eyetrackers = tr.find_all_eyetrackers()
            self.my_eyetracker = self.found_eyetrackers[0]
            self.print_tracker_info()
        
            self.left_gaze_points = []
            self.right_gaze_points = []
            self.left_pupil_sizes = []
            self.right_pupil_sizes = []
        
        self.log_tap_data = log_tap_data
        self.log_eye_data = log_eye_data
        
        self.part_id = part_id
        self.alpha_id = alpha_id
        self.traj_id = traj_id
        self.rhythm_id = rhythm_id
        self.tempo = tempo
        self.max_time = max_time
        
        self.load_rhythm()
        self.recorded = []
        self.times_from_start = []
        
        self.started = False
        self.start_time = 0.0
        
        self.recording_started = False
        self.recording_start_time = 0.0
        
        self.use_intervals = True
        
        cwd = getcwd()
        self.tap_csv_dir = cwd + '\secondary task\data'
        self.eye_csv_dir = cwd + '\secondary task\data_tobii'
        
        rhythms_dir = cwd + "\secondary task" + "\\" + "rhythms"
        match self.rhythm_id:
            case 1: 
                self.sound_file = '\Tempo115short.wav'
            case 2: 
                self.sound_file = '\Tempo120short.wav'
            case 3: 
                self.sound_file = '\Tempo125short.wav'
            case 4: 
                self.sound_file = '\Tempo130short.wav'
            case 5: 
                self.sound_file = '\Tempo135short.wav'
            case _: 
                print("The rhythm ID does not match a corresponding sound file!")
            
        self.sound = rhythms_dir + self.sound_file
        
        
    #############################################
    def load_rhythm(self):
        self.truth = get_timestamps(self.tempo, self.max_time, 2)
        self.num_taps = len(self.truth)
        print("Successfully loaded rhythm #%d" % self.rhythm_id)
        
    #############################################
    def run(self):
        
        print("\nPress the 'right-arrow' key when initial 5 second smoothing is finished ... ")
        
        while True:
            
            entry = read_key()
            
            if entry == "right":
                if not self.started:
                    self.started = True
                    self.start_time = time()
                    print("\nPlaying sound within the next 5 seconds ... \n")
                    print("Then, Press the 'space' key to tap the rhythm! \n")
                    playsound(self.sound)
            
            if entry == "space":
                self.times_from_start.append(time() - self.start_time - 5)
                if not self.recording_started:
                    self.recorded.append(0.0)
                    self.recording_started = True
                    self.recording_start_time = time()
                    print("\n Heard first tap, started recording taps! \n")
                    if self.use_eyetracker:
                        self.my_eyetracker.subscribe_to(tr.EYETRACKER_GAZE_DATA,
                                            self.gaze_data_callback, as_dictionary=True)
                        print("\n Using eyetracker, started listening to eye-tracker data!\n")
                else:
                    self.recorded.append(time() - self.recording_start_time)
            
            if entry == "q":
                print("Stopping recording of tapping data. \n")
                if self.use_eyetracker:
                    print("\n Also stopped subscribing to eye tracker data. \n")
                    self.my_eyetracker.unsubscribe_from(tr.EYETRACKER_GAZE_DATA, self.gaze_data_callback)
                break
        
        self.clean_up_record()
        self.calculate_error()
        
        _ = input("Press 'enter' to write tapping and eye-tracking data ... ")
        
        if self.log_tap_data:
            self.write_tapping_data()
        
        if self.use_eyetracker:
            if self.log_eye_data:
                self.write_eye_data()
                # self.plot_pupil_diameters()
    
    
    ################################  RHYTHM METHOD STUFF  ################################
    # used to remove every second entry, since key-presses are registered twice for some reason ...
    def clean_up_record(self):
        new_recorded = []
        # print("There are %d entries in the pre-clean version" % len(self.recorded))
        # first remove duplicates
        for i in range(len(self.recorded)):
            if i % 2 == 0:
                new_recorded.append(self.recorded[i])
        
        # then, out of {recorded, truth}, reduce the longer one to the length of the shorter one
        recorded_size = len(new_recorded)
        if recorded_size > self.num_taps:
            self.recorded = new_recorded[0:self.num_taps]
        else:
            self.recorded = new_recorded
            self.truth = self.truth[0:recorded_size]
            self.num_taps = recorded_size
        # print("After cleaning, there are %d entries!" % len(self.recorded))
    
    ############################################# 
    def print_record(self):
        print("\nThe true times are %s\n" % self.truth)
        print("The recorded times were %s\n" % self.recorded)
        
    #############################################
    def calculate_error(self):
        
        self.error_list = []
        self.errp_list = []
        self.total_error = 0.0
        self.total_errp = 0.0
        
        if self.use_intervals:
            # calculate error using the inter-tap intervals
            for i in range(self.num_taps - 1):
                my_gap = self.recorded[i+1] - self.recorded[i]
                true_gap = self.truth[i+1] - self.truth[i]
                err = my_gap - true_gap
                errp = err / true_gap * 100
                self.error_list.append(err)
                self.errp_list.append(errp)
                self.total_error += abs(err)
                self.total_errp += abs(errp)
            
        else:
            # calculate error using differences in timestamps of the taps
            for i in range(self.num_taps):
                err = self.recorded[i] - self.truth[i]
                self.error_list.append(err)
                self.total_error += abs(err)

        self.ave_error = self.total_error / (self.num_taps - 1)
        self.ave_errp = self.total_errp / (self.num_taps - 1)
        
        # print("\nThe list of error values are %s\n" % self.error_list)
        # print("The total magnitude of error is %.3f\n" % self.total_error)
        print("=" * 80)
        print("The average percentage error is %.3f %%\n" % self.ave_errp)
            
    #############################################
    def write_tapping_data(self):
        
        # initialize the data logger object, and write to files
        tdl = TappingDataLogger(self.tap_csv_dir, self.part_id, self.alpha_id, self.traj_id, 
                                self.rhythm_id, self.tempo, self.ave_error, self.ave_errp,
                                self.truth, self.recorded, self.times_from_start, 
                                self.error_list, self.errp_list)

        # double check if we want to write to csv file
        # _ = input("Please hit 'enter' to write tapping data to csv file ... ")
        tdl.log_data()
        
    
    ################################  EYE TRACKER STUFF  ################################
    def gaze_data_callback(self, gaze_data):
        # get gaze points
        left_eye_gaze = gaze_data['left_gaze_point_on_display_area']
        right_eye_gaze = gaze_data['right_gaze_point_on_display_area']
        # flip tuple point vertically
        new_left_eye_gaze = (left_eye_gaze[0], 1.0-left_eye_gaze[1])
        new_right_eye_gaze = (right_eye_gaze[0], 1.0-right_eye_gaze[1])
        # get pupil diameters
        left_pupil_diameter = gaze_data['left_pupil_diameter']
        right_pupil_diameter = gaze_data['right_pupil_diameter']
        
        print("(left, right) pupil diameters = (%.3f, %.3f)" % 
              (left_pupil_diameter, right_pupil_diameter))
        
        self.left_gaze_points.append(new_left_eye_gaze)
        self.right_gaze_points.append(new_right_eye_gaze)
        self.left_pupil_sizes.append(left_pupil_diameter)
        self.right_pupil_sizes.append(right_pupil_diameter)
        
        
    #############################################
    def write_eye_data(self):
        
        # initialize the data logger object, and write to files
        edl = EyeDataLogger(self.eye_csv_dir, self.part_id, self.alpha_id, self.traj_id, self.rhythm_id, 
                                self.tempo, self.left_gaze_points, self.right_gaze_points, 
                                self.left_pupil_sizes, self.right_pupil_sizes)
        edl.calc_averages()

        # double check if we want to write to csv file
        # _ = input("Please hit 'enter' to write eye data to csv file ... ")
        edl.log_data()
    
    #############################################
    def plot_gaze_trajectory(self):
        plt.plot(*zip(*self.left_gaze_points), color='b', label='left eye')
        plt.plot(*zip(*self.right_gaze_points), color='r', label='right eye')
        plt.xlabel("x")
        plt.ylabel("y")
        plt.title("Left and Right eye gaze points")
        plt.legend()
        plt.show()
        
    #############################################
    def plot_pupil_diameters(self):
        
        plt.subplot(1, 2, 1)
        plt.plot(self.left_pupil_sizes, color='b', label='left eye')
        plt.xlabel("datapoints")
        plt.ylabel("diameter (mm)")
        plt.title("Left eye pupil diameters")
        plt.legend()
        
        plt.subplot(1, 2, 2)
        plt.plot(self.right_pupil_sizes, color='r', label='right eye')
        plt.xlabel("datapoints")
        plt.ylabel("diameter (mm)")
        plt.title("Right eye pupil diameters")
        plt.legend()
        
        plt.show()
    
    #############################################
    def print_tracker_info(self):
        print("Address: " + self.my_eyetracker.address)
        print("Model: " + self.my_eyetracker.model)
        print("Name (It's OK if this is empty): " + self.my_eyetracker.device_name)
        print("Serial number: " + self.my_eyetracker.serial_number)
    

               
##########################################################################################
def main():
    
    rm = RhythmMethod(SAVE_TAP_DATA, SAVE_EYE_DATA, PART_ID, ALPHA_ID, TRAJ_ID, 
                           RHYTHM_ID, TEMPO, MAX_TIME, USE_EYETRACKER)
    
    rm.run()
    

##########################################################################################
if __name__ == "__main__":
    main()