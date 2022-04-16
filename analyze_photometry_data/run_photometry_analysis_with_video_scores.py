import sys

#import services
sys.path.append('services')
from plot_bout_non_overlap import plot_bout_no_overlap
from normalize_df_over_f_photometry import normalize_df

#import native python libraries
import pandas as pd
import glob
import cv2
import matplotlib.pyplot as plt
import numpy as np


#Empty dataframe for filtered non-feedingBouts
nonFilteredFeedingBouts = pd.DataFrame()

#open csv file containing video scoring results
feedingBouts = pd.read_csv('/home/jordan/Desktop/dat_photometry_data_to_analyze/b13024_dat_screen_04012022_feeding_bouts_scored.csv')

#open csv file containing photometry dataset
photometryData = pd.read_csv('/home/jordan/Desktop/dat_photometry_data_to_analyze/b13024_dat_screen_04012022_raw_photometry.csv')

#create empty figure for subplots
plt.figure(figsize=(15, 12))
plt.subplots_adjust(hspace=0.5)
plt.suptitle("Dat photometry", fontsize=18, y=0.95)

#parse through feedingBouts dataframe and get intervals
for ind in feedingBouts.index:
    #Filter feeding and non feeding bouts from raw excel sheets
    if feedingBouts['feeding'][ind] == False:
        filteredFeedingBoutsMask = photometryData[photometryData.TIME.between(feedingBouts['time'][ind-1], feedingBouts['time'][ind])]
        if feedingBouts.last_valid_index() == ind:  
            nonFilteredFeedingBoutsMask = photometryData[photometryData['TIME']>feedingBouts['time'][ind]]
        else:
            nonFilteredFeedingBoutsMask = photometryData[photometryData.TIME.between(feedingBouts['time'][ind], feedingBouts['time'][ind+1])]

        delta_F_over_F_feeding_bout = normalize_df(photometryData, filteredFeedingBoutsMask,feedingBouts['time'].loc[0])
        delta_F_over_F_non_feeding_bouts = normalize_df(photometryData, nonFilteredFeedingBoutsMask,feedingBouts['time'].loc[0])

        # add a new subplot non feeding bout
        plot_bout_no_overlap(plt.subplot(3, 2, ind), mask=nonFilteredFeedingBoutsMask, data=delta_F_over_F_non_feeding_bouts, feeding=False, ind=ind)
       
        # add new subplot feeding bout
        plot_bout_no_overlap(plt.subplot(3, 2, ind + 1), mask=filteredFeedingBoutsMask, data=delta_F_over_F_feeding_bout, feeding=True, ind=ind+1)

plt.show()

        
#Next steps
#Figure out how to plot multiple feedig bouts on same x-y axis
#Figure out how to plot photometry data in real-time with video next to it like in synapse
#Clean up and refactor code with MVC