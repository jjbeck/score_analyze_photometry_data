def normalize_df(raw_df, filtered_bout, feedingStart):
    raw_df = raw_df[raw_df['TIME']>=10] #use this line to delete timepoints, usually the beginning
    avg_d0 = raw_df[(raw_df['TIME']>=10) & (raw_df['TIME']<= feedingStart)]['D0'].mean()  #time interval that will be used as baseline
    normalized_d0 = (filtered_bout['D0'] - avg_d0)/avg_d0
    return normalized_d0