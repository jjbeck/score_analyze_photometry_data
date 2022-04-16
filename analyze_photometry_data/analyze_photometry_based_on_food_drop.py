import pandas as pd
import glob
import cv2
import matplotlib.pyplot as plt
import numpy as np

food_drop = 828

## INPUT: raw dataframe
## OUTPUT: dataframe with "normalized_d0" column 
def normalize_df(raw_df, food_drop):
    raw_df = raw_df[raw_df['TIME']>=10] #use this line to delete timepoints, usually the beginning
    avg_d0 = raw_df[(raw_df['TIME']>=10) & (raw_df['TIME']<= 828)]['D0'].mean()  #time interval that will be used as baseline
    raw_df['normalized_d0'] = (raw_df['D0'] - avg_d0)/avg_d0
    return raw_df

#open csv file containing photometry dataset
photometryData = pd.read_csv('/home/jordan/Desktop/dat_photometry_data_to_analyze/b13024_dat_screen_04012022_raw_photometry.csv')


delta_F_over_F_food_drop = normalize_df(photometryData, food_drop)

filtered_delta_F_over_F_food_drop = delta_F_over_F_food_drop[delta_F_over_F_food_drop.TIME.between(food_drop-400, food_drop+400)]

#plot deltaF/F
#plt.yticks(np.arange(-0.5, 0.05, 0.1)) #y-axis range
plt.ylabel('dF/F')
plt.xlabel('time (s)')
plt.plot(filtered_delta_F_over_F_food_drop['TIME'],filtered_delta_F_over_F_food_drop['normalized_d0'],color='green')
plt.axvline(food_drop)
plt.show()