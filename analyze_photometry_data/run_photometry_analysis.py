import pandas as pd
import glob
import cv2
import matplotlib.pyplot as plt
import numpy as np

#Empty dataframe for filtered feedingBouts
filteredFeedingBouts = pd.DataFrame()

#Empty dataframe for filtered non-feedingBouts
nonFilteredFeedingBouts = pd.DataFrame()

#open csv file containing video scoring results
feedingBouts = pd.read_csv('/home/jordan/Desktop/dat_photometry_data_to_analyze/b13024_dat_screen_04012022_feeding_bouts_scored.csv')

#open csv file containing photometry dataset
photometryData = pd.read_csv('/home/jordan/Desktop/dat_photometry_data_to_analyze/b13024_dat_screen_04012022_raw_photometry.csv')

#parse through feedingBouts dataframe and get intervals
for ind in feedingBouts.index:
    if feedingBouts['feeding'][ind] == False:
        fileredFeedingBoutsMask = photometryData[photometryData.TIME.between(feedingBouts['time'][ind-1], feedingBouts['time'][ind])]
        filteredFeedingBouts = filteredFeedingBouts.append(fileredFeedingBoutsMask)
        if feedingBouts.last_valid_index() == ind:  
            nonFilteredFeedingBouts = nonFilteredFeedingBouts.append(photometryData[photometryData['TIME']>feedingBouts['time'][ind]])
        else:
            nonFilteredFeedingBouts= nonFilteredFeedingBouts.append(photometryData[photometryData.TIME.between(feedingBouts['time'][ind], feedingBouts['time'][ind+1])])

#get df/f for feeding bouts 

#get df/f got non-feeding bouts
        

        
#Next steps
#Calculate df/f for feeding and non feeding bouts data
#Get graph of individual signals for feeding and non feeding feedingBouts
#Figure out how to plot multiple graphs of these together
#Figure out how to plot photometry data in real-time with video next to it like in synapse
#Clean up and refactor code with MVC