import glob
import os
import pandas as pd
import matplotlib.pyplot as plt
import services.z_score_ghrelin_inj as z_score_ghrelin_inj
import services.save_plot_ghrelin_inj as save_plot_ghrelin_inj


#go through directory and act on files based on folder names
for folder in glob.iglob(('/home/jordan/Desktop/dat_photometry_data_to_analyze/*')):
    if 'injection' in folder:
        #create new empty pandas dataframe
        all_traces_ghrelin = pd.DataFrame()
        all_traces_saline = pd.DataFrame()
        all_traces_ghrelin_norm = pd.DataFrame()
        
        all_traces_saline_norm = pd.DataFrame()
        plt.plot()
        for file in glob.iglob(folder + '/*.csv'):
            print(file)
            injection_time = int(file[file.rfind('_')+1:-4])
            photometryData = pd.read_csv(file)
            photometry_ind_z_score = z_score_ghrelin_inj.calculate_ind_z_score_injection(photometryData, injection_time)
    
            file = file[file.rfind('/'):]
            if "ghrelin" in file:
                photometry_ind_z_score_ghr = photometry_ind_z_score.reset_index()
                all_traces_ghrelin[file] = photometry_ind_z_score['z_score']
                all_traces_ghrelin_norm[file] = photometry_ind_z_score['normalized_d0']   
            if "saline" in file:
                photometry_ind_z_score_sal = photometry_ind_z_score.reset_index()
                all_traces_saline[file] =  photometry_ind_z_score['z_score']
                all_traces_saline_norm[file] =  photometry_ind_z_score['normalized_d0']

        if not all_traces_saline.empty:
            try:
                all_traces_saline = all_traces_saline.set_index(photometry_ind_z_score_sal['time_diff'])
                all_traces_saline_norm = all_traces_saline_norm.set_index(photometry_ind_z_score_sal['time_diff'])
            except:
                photometry_ind_z_score= photometry_ind_z_score_sal.tail(len(all_traces_saline))
                all_traces_saline = all_traces_saline.set_index(photometry_ind_z_score_sal['time_diff'])
                all_traces_saline_norm = all_traces_saline_norm.set_index(photometry_ind_z_score_sal['time_diff'])

            all_traces_saline_mean = all_traces_saline.mean(axis=1) #compute mean of all traces
            all_traces_saline_sem = all_traces_saline.sem(axis=1) #compute mean of all traces
            all_traces_saline_norm_mean = all_traces_saline_norm.mean(axis=1) #compute mean of all traces
            all_traces_saline_norm_sem = all_traces_saline_norm.sem(axis=1) #compute mean of all traces

        
        try:
            all_traces_ghrelin = all_traces_ghrelin.set_index(photometry_ind_z_score_ghr['time_diff'])
            all_traces_ghrelin_norm = all_traces_ghrelin_norm.set_index(photometry_ind_z_score_ghr['time_diff'])
        except:
            photometry_ind_z_score= photometry_ind_z_score_ghr.tail(len(all_traces_ghrelin))
            all_traces_ghrelin = all_traces_ghrelin.set_index(photometry_ind_z_score_ghr.iloc[:-1]['time_diff'])
            all_traces_ghrelin_norm = all_traces_ghrelin_norm.set_index(photometry_ind_z_score_ghr.iloc[:-1]['time_diff'])

        all_traces_ghrelin_mean = all_traces_ghrelin.mean(axis=1) #compute mean of all traces
        all_traces_ghrelin_sem = all_traces_ghrelin.sem(axis=1) #compute mean of all traces
        all_traces_ghrelin_norm_mean = all_traces_ghrelin_norm.mean(axis=1) #compute mean of all traces
        all_traces_ghrelin_norm_sem = all_traces_ghrelin_norm.sem(axis=1) #compute mean of all traces
   
        
        
        save_plot_ghrelin_inj.save_injection_plot(plt, all_traces_ghrelin_mean, all_traces_ghrelin_sem, all_traces_saline_mean, all_traces_saline_sem,
        all_traces_ghrelin_norm_mean, all_traces_ghrelin_norm_sem, all_traces_saline_norm_mean, all_traces_saline_norm_sem, folder, file) #save plot in folder data is in
        