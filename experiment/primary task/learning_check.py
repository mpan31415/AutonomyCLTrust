from pandas import read_csv, DataFrame
from os import getcwd
import matplotlib.pyplot as plt

NUM_PARTICIPANTS = 24

####### Plots the measure again trial numbers for each of the autonomy levels #######
PLOT_ONLY = True
####### if FALSE, will not plot, and instead write data to dataframe for learning effect analysis #######


##########################################################################################
def get_raw_data(part_id):
    
    my_curr_dir = getcwd()
    my_data_file = my_curr_dir + "\primary task\data" + "\part" + str(part_id) + "\part" + str(part_id) + "_header.csv"
    df = read_csv(my_data_file).iloc[5:,:]
    
    return df


##########################################################################################
def err_within_round(auto_id: int):
    
    trial1_err_list = []
    trial2_err_list = []
    trial3_err_list = []
    trial4_err_list = []
    trial5_err_list = []
    trial_err_lists = [trial1_err_list, trial2_err_list, trial3_err_list, trial4_err_list, trial5_err_list]
    
    # get summation
    for part_id in range(1, NUM_PARTICIPANTS+1):
        # get raw dataframe
        raw = get_raw_data(part_id)
        this_auto_group = raw[raw['alpha_id']==int(5-auto_id)]
        this_err_list = this_auto_group['overall_ave'].tolist()
        for trial_id in range(1, 6):
            trial_err_lists[trial_id-1].append(this_err_list[trial_id-1])
    
    # compute averages for each trial (for this autonomy level)
    trial_ave_err_list = []
    for trial_id in range(1, 6):
        trial_err_list = trial_err_lists[trial_id-1]
        trial_ave_err = sum(trial_err_list) / len(trial_err_list)
        trial_ave_err_list.append(trial_ave_err)
                
    return trial_err_lists, trial_ave_err_list


pid_low_list = []
pid_high_list = []


#######################################################
if PLOT_ONLY:
    for auto_id in range(5):
        trial_err_lists, trial_ave_err_list = err_within_round(auto_id)
        plt.subplot(2, 3, auto_id+1)
        plt.plot(trial_ave_err_list, color='r', label='average errors')
        plt.ylim([0.0, 0.03])
        # Naming the x-axis, y-axis and the whole graph
        plt.xlabel("Trial ID")
        plt.ylabel("Average error (m)")
        plt.title("Average Error vs. Trial ID (Autonomy " + str(auto_id) + ")")
        plt.legend()
    plt.show()

#######################################################
else:
    
    for auto_id in range(5):
    
        trial_err_lists, trial_ave_err_list = err_within_round(auto_id)
        
        pid_big_list = []
        trial_id_big_list = []
        err_big_list = []
        for trial_id in range(1, 6):
            for part_id in range(1, 25):
                pid_big_list.append(part_id)
                trial_id_big_list.append(trial_id)
                err_big_list.append(trial_err_lists[trial_id-1][part_id-1])
        
        # generate new dataframe
        df_dict = {
            'pid': pid_big_list,
            'trial_id': trial_id_big_list,
            'error': err_big_list
        }
        this_auto_df = DataFrame(df_dict)
        
        # write new dataframe to csv file
        dest_path = getcwd() + "\primary task\learning_effect" + '\\tap_impact' + str(auto_id) + '.csv'
        this_auto_df.to_csv(dest_path, index=False)
        
        print(" Successfully written pre-processed data to csv file! \n")