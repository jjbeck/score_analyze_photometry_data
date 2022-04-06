#Import modules
import pandas as pd
import glob
import cv2
import matplotlib.pyplot as plt
import numpy as np

feeding = False
feedingStart = 0

#create empty pandas dataset to populate
feedingBouts = pd.DataFrame()



def scoreFeedingBout(time):
  global feeding
  global feedingStart
  global feedingBouts
  if feeding == False:
    feedingStart = time/1000
    print('feeding bout started at {}'.format(feedingStart))
    feeding = True
  else:
    print('feeding bout finished at {}'.format(time/1000))
    start = pd.DataFrame({'time': [feedingStart], 'feeding': [True]})
    end = pd.DataFrame({'time': [time/1000], 'feeding': [False]})
    feedingBouts = feedingBouts.append(start)
    feedingBouts = feedingBouts.append(end)
    feeding = False
    feedingBouts.to_csv('/home/jordan/Desktop/dat_photometry_data_to_analyze/b13024_dat_screen_04012022_feeding_bouts_scored.csv')
    print(feedingBouts)
  

#Parse through files and start playing video
cap = cv2.VideoCapture('/home/jordan/Desktop/dat_photometry_data_to_analyze/b13024_dat_screen_04012022_raw_video.avi')

cap.set(cv2.CAP_PROP_POS_MSEC,600000)     

if (cap.isOpened()== False):
  print("Error opening video stream or file")

while(cap.isOpened()):
  ret, frame = cap.read()

  if ret == True:
    cv2.imshow('frame', frame)
    k = cv2.waitKey(33)
    if k==113:    # Esc key to stop
        break
    elif k==32:  # normally -1 returned,so don't print it
        scoreFeedingBout(cap.get(cv2.CAP_PROP_POS_MSEC))
  else:
    break


cap.release()
cv2.destroyAllWindows()


#Next steps
#Add button for moving/non moving
#clean up and refactor code with MVC model