import matplotlib.pyplot as plt

def plot_bout_no_overlap(ax, mask, data, feeding, ind):
    ax.set_ylabel('dF/F')
    ax.set_xlabel('time (s)')
    ax.plot(mask['TIME'],data,color='green')
    if ind == 1:
        ax.set_title('Non Feeding Bouts')
    if ind == 2:
        ax.set_title('Feeding Bouts')