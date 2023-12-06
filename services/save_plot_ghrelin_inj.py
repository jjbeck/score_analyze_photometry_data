import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline


def save_injection_plot(plt, photometryData, photometryDataSem, objectData, objectDataSem,
photometryDataNorm, photometryDataSemNorm, objectDataNorm, objectDataSemNorm, directory, filename):

    #set up constant variables for figure
    plt.ylabel('Z Score')
    plt.xlabel('time (s)')

    #get custom filename for figure
    name_ids = filename.split('_')
    plt_title = directory[directory.rfind('/')+1:]
    plt_title = plt_title.split('_')
    plt.title(plt_title[0] + ' ' + plt_title[1] + ' ' +  plt_title[2] + ' ' +  plt_title[3])
    #plt.title(name_ids[1] + ' ' + name_ids[2] + ' ' +  name_ids[3] + ' ' +  name_ids[4])
    
    #plot and format photometry data
    plt.plot(photometryData.index, photometryData)
    plt.fill_between(photometryData.index, photometryData-photometryDataSem, photometryData+photometryDataSem, alpha=0.2, edgecolor='#1B2ACC',
    linestyle='-')


    #plot and format control data
    plt.plot(objectData.index, objectData)
    plt.fill_between(objectData.index, objectData-objectDataSem, objectData+objectDataSem, alpha=0.2, edgecolor='#1B2ACC',
    linestyle='-')

   
    #plot and format additional figure elements
    plt.axvline(0)
    plt.axvline(1200)
    plt.legend(['Ghrelin Injection', 'Saline Injection'], loc='upper right')
    

    #save figure to file
    plt.savefig(directory + '/' + plt_title[0] + ' ' + plt_title[1] + ' ' +  plt_title[2] + '_zscore' + '.png')


    #set up constant variables for figure
    plt.clf()
    plt.title(plt_title[0] + ' ' + plt_title[1] + ' ' +  plt_title[2] + ' ' +  plt_title[3])
    plt.ylabel('dF/F')
    plt.xlabel('time (s)')

    #plot and format photometry data
    plt.plot(photometryDataNorm.index, photometryDataNorm)
    plt.fill_between(photometryDataNorm.index, photometryDataNorm-photometryDataSemNorm, photometryDataNorm+photometryDataSemNorm, alpha=0.2, edgecolor='#1B2ACC',
    linestyle='-')


    #plot and format control data
    plt.plot(objectDataNorm.index, objectDataNorm)
    plt.fill_between(objectDataNorm.index, objectDataNorm-objectDataSemNorm, objectDataNorm+objectDataSemNorm, alpha=0.2, edgecolor='#1B2ACC',
    linestyle='-')

   
    #plot and format additional figure elements
    plt.axvline(0)
    plt.axvline(1200)
    plt.legend(['Ghrelin Injection', 'Saline Injection'], loc='upper right')
    

    #save figure to file
    plt.savefig(directory + '/' + plt_title[0] + ' ' + plt_title[1] + ' ' +  plt_title[2] + '_normalized' + '.png')