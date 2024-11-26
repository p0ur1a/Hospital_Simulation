"""
This file contains functions for visualization. While we only follow one variable at this stage
and only need one function to make its graph consecutively, we can expand the project and add 
more functions to this file to visualize them

The important variables in the function are as follows:

    1. average_waiting_times: The average waiting time of each run is stored and will be passed to the
    function at the end to visualize them and draw conclusions based on them

    2. error_codes: these are essentially our simulation stop causes which are patient waiting time
    failure (red), waiting queue failure (pink), and success (green). The reasons for triggering each
    of these causes have been discussed in the project.py extensively.

"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

def plot_average_waiting_times(average_waiting_times, error_codes):
    
    colors = ["#EF9E12" if item == 2 else "red" if item == 1 else "#16C80A" for item in error_codes]

    plt.scatter(range(1, len(average_waiting_times) + 1), average_waiting_times, c=colors)

    plt.plot(range(1, len(average_waiting_times) + 1), average_waiting_times, linestyle='-', color='blue', alpha = 0.3)
    
    plt.xlabel('Number of desks')
    plt.ylabel("Patients' average waiting time")

    plt.legend(handles=[mpatches.Patch(color='red', label='Waiting time failure'),
                        mpatches.Patch(color='#EF9E12', label='Waiting queue failure'),
                        mpatches.Patch(color='#16C80A', label='Success')])

    plt.show()
