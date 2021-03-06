import pandas as pd
import glob
import cv2
import matplotlib.pyplot as plt
import numpy as np

food_drop = 490

## INPUT: raw dataframe
## OUTPUT: dataframe with "normalized_d0" column 
def normalize_df(raw_df, injection_time):
    raw_df = raw_df[raw_df['TIME']>=100] #use this line to delete timepoints, usually the beginning
    avg_d0 = raw_df[(raw_df['TIME']>=100) & (raw_df['TIME']<= injection_time-100)]['D0'].mean()  #time interval that will be used as baseline
    raw_df['normalized_d0'] = (raw_df['D0'] - avg_d0)/avg_d0
    return raw_df

def calculate_z_score(raw_df, injection_time):
    raw_df = raw_df[raw_df['TIME']>=30] #use this line to delete timepoints, usually the beginning
    avg_d0 = raw_df[(raw_df['TIME']>=30) & (raw_df['TIME']<= injection_time-60)]['D0'].mean()  #time interval that will be used as baseline
    std_d0 = raw_df[(raw_df['TIME']>=30) & (raw_df['TIME']<= injection_time-60)]['D0'].std()
    raw_df['z_score'] = (raw_df['D0'] - avg_d0)/std_d0
    return raw_df

#open csv file containing photometry dataset
photometryData = pd.read_csv('/home/jordan/Desktop/dat_photometry_data_to_analyze/b13058_dat_screen_04012022_raw_photometry.csv')

delta_F_over_F_food_drop = calculate_z_score(photometryData, food_drop)

filtered_delta_F_over_F_food_drop = delta_F_over_F_food_drop[delta_F_over_F_food_drop.TIME.between(food_drop-200, food_drop+200)]

#plot deltaF/F
#plt.yticks(np.arange(-0.5, 0.05, 0.1)) #y-axis range
plt.ylabel('Z Score')
plt.xlabel('time (s)')
plt.title("Dat Photometry Recording (n=1)")
plt.plot(filtered_delta_F_over_F_food_drop['TIME'],filtered_delta_F_over_F_food_drop['z_score'],color='green')
plt.axvline(food_drop)
plt.text(food_drop -70,-4.5,'Food Drop')
plt.savefig('/home/jordan/Desktop/dat_photometry_data_to_analyze/b13058_food_drop.png')