from pandas import read_csv, DataFrame
from os import getcwd


NUM_PARTICIPANTS = 24


LOW_AUTONOMY = 0.2
HIGH_AUTONOMY = 0.8


##########################################################################################
def get_raw_data(measure: str):
    
    my_curr_dir = getcwd()
    my_file_dir = my_curr_dir + "\dataframes\\" + measure + ".csv"
    df = read_csv(my_file_dir)
    
    return df


##########################################################################################
def group(low_auto, high_auto):
    
    # mdmt df
    mdmt_df = get_raw_data("mdmt")
    mdmt_df = mdmt_df[(mdmt_df['autonomy']==low_auto) | (mdmt_df['autonomy']==high_auto)]
    dest_path = getcwd() + "\\grouped_dataframes\\grouped_mdmt.csv"
    mdmt_df.to_csv(dest_path, index=False)
    print(" 1/7 \n")
    
    # p_auto df
    p_auto_df = get_raw_data("p_auto")
    p_auto_df = p_auto_df[(p_auto_df['autonomy']==low_auto) | (p_auto_df['autonomy']==high_auto)]
    dest_path = getcwd() + "\\grouped_dataframes\\grouped_p_auto.csv"
    p_auto_df.to_csv(dest_path, index=False)
    print(" 2/7 \n")
    
    # p_trust df
    p_trust_df = get_raw_data("p_trust")
    p_trust_df = p_trust_df[(p_trust_df['autonomy']==low_auto) | (p_trust_df['autonomy']==high_auto)]
    dest_path = getcwd() + "\\grouped_dataframes\\grouped_p_trust.csv"
    p_trust_df.to_csv(dest_path, index=False)
    print(" 3/7 \n")
    
    # pupil df
    pupil_df = get_raw_data("pupil")
    pupil_df = pupil_df[(pupil_df['autonomy']==low_auto) | (pupil_df['autonomy']==high_auto)]
    dest_path = getcwd() + "\\grouped_dataframes\\grouped_pupil.csv"
    pupil_df.to_csv(dest_path, index=False)
    print(" 4/7 \n")
    
    # tapping_err df
    tapping_err_df = get_raw_data("tapping_err")
    tapping_err_df = tapping_err_df[(tapping_err_df['autonomy']==low_auto) | (tapping_err_df['autonomy']==high_auto)]
    dest_path = getcwd() + "\\grouped_dataframes\\grouped_tapping_err.csv"
    tapping_err_df.to_csv(dest_path, index=False)
    print(" 5/7 \n")
    
    # tlx df
    tlx_df = get_raw_data("tlx")
    tlx_df = tlx_df[(tlx_df['autonomy']==low_auto) | (tlx_df['autonomy']==high_auto)]
    dest_path = getcwd() + "\\grouped_dataframes\\grouped_tlx.csv"
    tlx_df.to_csv(dest_path, index=False)
    print(" 6/7 \n")
    
    # traj err df
    traj_err_df = get_raw_data("traj_err")
    traj_err_df = traj_err_df[(traj_err_df['autonomy']==low_auto) | (traj_err_df['autonomy']==high_auto)]
    dest_path = getcwd() + "\\grouped_dataframes\\grouped_traj_err.csv"
    traj_err_df.to_csv(dest_path, index=False)
    print(" 7/7 \n")
    
    print(" Grouping of all csv files finished !!! \n")


##########################################################################################
def main():
    
    group(LOW_AUTONOMY, HIGH_AUTONOMY)
    

    
##########################################################################################
if __name__ == "__main__":
    
    main()
    