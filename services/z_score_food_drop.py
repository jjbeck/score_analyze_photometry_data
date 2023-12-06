import pandas as pd
import glob
import cv2
import matplotlib.pyplot as plt
import numpy as np


def calculate_ind_z_score_food_drop(trace, food_drop_time, interval):
    trace = trace[trace['TIME']>=30] #use this line to delete timepoints, usually the beginning
    avg_d0 = trace[(trace['TIME']>= food_drop_time-interval) & (trace['TIME']<= food_drop_time-10)]['D0'].mean()  #time interval that will be used as baseline
    std_d0 = trace[(trace['TIME']>= food_drop_time-interval) & (trace['TIME']<= food_drop_time-10)]['D0'].std()
    trace['z_score'] = (trace['D0'] - avg_d0)/std_d0
    trace['normalized_d0'] = (trace['D0'] - avg_d0)/avg_d0
    trace['time_diff'] = trace['TIME'] - food_drop_time
    trace.loc[(trace.z_score > 5),'z_score']=0
    trace.loc[(trace.z_score < -5),'z_score']=0
    return trace[trace.TIME.between(food_drop_time-interval, food_drop_time+interval)]