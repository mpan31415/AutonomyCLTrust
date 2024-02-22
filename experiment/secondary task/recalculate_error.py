
###############################################################################################################
### Recalculates the tapping error accounting for when the "space" key is pressed and held for a brief moment,
### which will unwantedly register as 2 or more consecutive taps.
###############################################################################################################

TRUTH = []

RECORDED = []


###############################################################################################################
def clean_up_record(truth, recorded, logging):
    
    truth_size = len(truth)
    recorded_size = len(recorded)
    
    if logging:
        print("Before cleaning, there are %d entries in recorded!" % recorded_size)
        print("Before cleaning, there are %d entries in truth!" % truth_size)
    
    # then, out of {recorded, truth}, reduce the longer one to the length of the shorter one
    if recorded_size > truth_size:
        recorded = recorded[0:truth_size]
    else:
        truth = truth[0:recorded_size]
        truth_size = recorded_size
        
    assert len(recorded) == len(truth)
    
    if logging:
        print("After cleaning, there are %d entries in recorded!" % len(recorded))
        print("After cleaning, there are %d entries in truth!" % len(truth))
    
    return truth, recorded, len(truth)
    

###############################################################################################################
def recalculate(truth, recorded, num_taps):

    error_list = []
    errp_list = []
    total_error = 0.0
    total_errp = 0.0
    
    # calculate error using the inter-tap intervals
    for i in range(num_taps - 1):
        my_gap = recorded[i+1] - recorded[i]
        true_gap = truth[i+1] - truth[i]
        err = my_gap - true_gap
        errp = err / true_gap * 100
        error_list.append(err)
        errp_list.append(errp)
        total_error += abs(err)
        total_errp += abs(errp)

    ave_error = total_error / (num_taps - 1)
    ave_errp = total_errp / (num_taps - 1)
    
    print("\nerror_list = %s\n" % error_list)
    print("Errp list = %s\n" % errp_list)
    
    print("=" * 80)
    
    print("Average err = %.5f %%" % ave_error)
    print("Average err percentage =  %.5f %%\n" % ave_errp)
    

###############################################################################################################
def main():
    
    truth, recorded, num_taps = clean_up_record(TRUTH, RECORDED, False)
    
    recalculate(truth, recorded, num_taps)
    

###############################################################################################################
if __name__ == "__main__":
    main()