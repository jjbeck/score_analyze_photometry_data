import glob
import os
import pandas as pd
import matplotlib.pyplot as plt
import services.z_score_food_drop as z_score_food_drop
import services.save_plot_food_drop as save_plot


#go through directory and act on files based on folder names
for folder in glob.iglob(('/home/jordan/Desktop/dat_photometry_data_to_analyze/*')):
    if 'drop' in folder:
        #create new empty pandas dataframe
        all_traces_food = pd.DataFrame()
        all_traces_object = pd.DataFrame()
        all_traces_food_norm = pd.DataFrame()
        all_traces_object_norm = pd.DataFrame()
        plt.plot()
        for file in glob.iglob(folder + '/*.csv'):
            print(file)
            food_drop_time = int(file[file.rfind('_')+1:-4])
            photometryData = pd.read_csv(file)

            photometry_ind_z_score = z_score_food_drop.calculate_ind_z_score_food_drop(photometryData, food_drop_time, 300)
            file = file[file.rfind('/'):]
            if "food" in file or "hfd" in file:
                photometry_ind_z_score_food = photometry_ind_z_score.reset_index()
                all_traces_food[file] = photometry_ind_z_score['z_score']
                all_traces_food_norm[file] = photometry_ind_z_score['normalized_d0']   
            else:
                photometry_ind_z_score_obj = photometry_ind_z_score.reset_index()
                all_traces_object[file] =  photometry_ind_z_score['z_score']
                all_traces_object_norm[file] =  photometry_ind_z_score['normalized_d0']

        try:
            all_traces_food = all_traces_food.set_index(photometry_ind_z_score_food.iloc['time_diff'])
            all_traces_food_norm = all_traces_food_norm.set_index(photometry_ind_z_score_food['time_diff'])
        except:
            photometry_ind_z_score= photometry_ind_z_score_food.tail(len(all_traces_food))
            all_traces_food = all_traces_food.set_index(photometry_ind_z_score_food['time_diff'])
            all_traces_food_norm = all_traces_food_norm.set_index(photometry_ind_z_score_food['time_diff'])

        all_traces_food_mean = all_traces_food.mean(axis=1) #compute mean of all traces
        all_traces_food_sem = all_traces_food.sem(axis=1) #compute mean of all traces
        all_traces_food_mean_norm = all_traces_food_norm.mean(axis=1) #compute mean of all traces
        all_traces_food_sem_norm = all_traces_food_norm.sem(axis=1) #compute mean of all traces
        
        try:
            all_traces_object = all_traces_object.set_index(photometry_ind_z_score_obj['time_diff'])
            all_traces_object_norm = all_traces_object_norm.set_index(photometry_ind_z_score_obj['time_diff'])
        except:
            photometry_ind_z_score= photometry_ind_z_score_obj.tail(len(all_traces_object))
            all_traces_object = all_traces_object.set_index(photometry_ind_z_score_obj['time_diff'])
            all_traces_object_norm = all_traces_object_norm.set_index(photometry_ind_z_score_obj['time_diff'])

        all_traces_object_mean = all_traces_object.mean(axis=1) #compute mean of all traces
        all_traces_object_sem = all_traces_object.sem(axis=1) #compute mean of all traces
        all_traces_object_mean_norm = all_traces_object_norm.mean(axis=1) #compute mean of all traces
        all_traces_object_sem_norm = all_traces_object_norm.sem(axis=1) #compute mean of all traces

        save_plot.save_food_drop(plt, all_traces_food_mean, all_traces_food_sem, all_traces_object_mean, all_traces_object_sem, 
        all_traces_food_mean_norm, all_traces_food_sem_norm, all_traces_object_mean_norm, all_traces_object_sem_norm, folder, file) #save plot in folder data is in
        
        
        


        
        
