#!/Users/steph/anaconda/bin/python3.5 -i
r"""
nautilus_plot
=============

nautilus_plot is a python interface for easy plotting from nautilus outputs, written by Stephane Paulin-Henriksson (SPH). Typical use (in the directory containing the nautilus simulations):
* in a shell: > nautilus_plot.py
* in python: > exec(open('nautilus_plot.py').read() (or any alias like 'run nautilus_plot' in ipython)

This is a preliminary version (v1) compatible with python 3.4+ & 2.7. the matplotlib's backend must be 'TkAgg' (configured in the matplotlibrc file)
"""
import nautilus_sph_define_buttons
import nautilus_sph_global_variables
import nautilus_sph_plot
import nautilus_sph_pack1

import numpy as np
import sys
import os.path
if sys.version_info[0]>2:
    # for Python 3
    import tkinter as tk
else:
    # for Python 2
    import Tkinter as tk

if __name__ == '__main__':
        
    np.set_printoptions(edgeitems=1000)
    if not os.path.isfile(nautilus_sph_global_variables.pickle_filename):     
        print('the pickle file ',nautilus_sph_global_variables.pickle_filename,
              ' does not exist')
####################
        print(" ==> creating it from local data.")
        #print("     for the moment, 3 radiuses (50, 100 and 200 AU), 64 times & 64 alt")
        nautilus_sph_pack1.create_nautilus_simulation_pickle_fmt(
            pickle_file=nautilus_sph_global_variables.pickle_filename)
#######################        
    root = tk.Tk()
    root.title(nautilus_sph_define_buttons.title_main_window)
    window = nautilus_sph_plot.SPH_windowplot(root)
