from email.mime import base
import pandas as pd
import glob
import cv2
import matplotlib.pyplot as plt
import numpy as np

exp_baseline_cutoff = 1100
exp_injection_time = 1400
sal_baseline_cutoff = 1464
sal_injection_time = 1764
food_drop = 1200

## INPUT: raw dataframe
## OUTPUT: dataframe with "normalized_d0" column 
def normalize_df(raw_df, injection_time, baseline):
    raw_df = raw_df[raw_df['TIME']>=10] #use this line to delete timepoints, usually the beginning
    avg_d0 = raw_df[(raw_df['TIME']>=baseline) & (raw_df['TIME']<= injection_time)]['D0'].mean()  #time interval that will be used as baseline
    raw_df['normalized_d0'] = (raw_df['D0'] - avg_d0)/avg_d0
    return raw_df

def calculate_z_score(raw_df, injection_time, baseline, saline):
    
    if saline == True:
        raw_df = raw_df[raw_df['TIME']>= baseline] #use this line to delete timepoints, usually the beginning
        avg_d0 = raw_df[(raw_df['TIME']>=baseline) & (raw_df['TIME']<= injection_time)]['D0'].mean()  #time interval that will be used as baseline
        std_d0 = raw_df[(raw_df['TIME']>=baseline) & (raw_df['TIME']<= injection_time)]['D0'].std()
        raw_df['z_score'] = (raw_df['D0'] - avg_d0)/std_d0
        raw_df['normalized_d0'] = (raw_df['D0'] - avg_d0)/avg_d0
        raw_df['time_diff'] = raw_df['TIME'] - baseline
        

    else:
        raw_df = raw_df[raw_df['TIME']>=baseline] #use this line to delete timepoints, usually the beginning
        avg_d0 = raw_df[(raw_df['TIME']>=baseline) & (raw_df['TIME']<= injection_time)]['D0'].mean()  #time interval that will be used as baseline
        std_d0 = raw_df[(raw_df['TIME']>=baseline) & (raw_df['TIME']<= injection_time)]['D0'].std()
        raw_df['z_score'] = (raw_df['D0'] - avg_d0)/std_d0
        raw_df['normalized_d0'] = (raw_df['D0'] - avg_d0)/avg_d0
        raw_df['time_diff'] = raw_df['TIME'] - baseline
        
    return raw_df



#open csv file containing photometry dataset
photometryData_ghrelin = pd.read_csv('/home/jordan/Desktop/dat_photometry_data_to_analyze/sated_ghrelin_injection/figure_out_injection_b13085_dat_ghrelin_injection_sated.csv')

photometryData_saline = pd.read_csv('/home/jordan/Desktop/dat_photometry_data_to_analyze/sated_ghrelin_injection/figure_out_injection_b13058_dat_saline_injection_sated.csv')


delta_F_over_F_food_drop_ghrelin = calculate_z_score(photometryData_ghrelin, exp_injection_time, exp_baseline_cutoff, False)

delta_F_over_F_food_drop_saline = calculate_z_score(photometryData_saline, sal_injection_time, sal_baseline_cutoff, True)

#filtered_delta_F_over_F_food_drop = delta_F_over_F_food_drop[delta_F_over_F_food_drop.TIME.between(food_drop-200, food_drop+200)]

#plot deltaF/F
#plt.yticks(np.arange(-0.5, 0.05, 0.1)) #y-axis range
plt.ylabel('Z Score')
plt.xlabel('time (s)')
plt.title("B13045 Ghrelin Injection Dat Photometry Recording (n=1)")
plt.plot(delta_F_over_F_food_drop_ghrelin['time_diff'],delta_F_over_F_food_drop_ghrelin['z_score'],color='blue')
plt.plot(delta_F_over_F_food_drop_saline['time_diff'],delta_F_over_F_food_drop_saline['z_score'],color='green')
plt.axvline(sal_injection_time-sal_baseline_cutoff, label = "help")
plt.text(sal_injection_time + 150,-8,'Injection')
plt.axvline(exp_injection_time-exp_baseline_cutoff, label = "help")
plt.text(500 + 150,-7,'Injection')
plt.axvline(food_drop)
plt.text(500 + food_drop + 150,-7,'Food Drop')
plt.legend(["Ghrelin", "Saline"])
plt.savefig('/home/jordan/Desktop/dat_photometry_data_to_analyze/b13045_ghrelin_inj_061322_zscore_try2.png')