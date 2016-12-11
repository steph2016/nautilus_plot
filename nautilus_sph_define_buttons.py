r"""
nautilus_sph_define_buttons
===========================
part of the nautilus - python pipeline (S. Paulin-Henriksson v0)
Global variables available at all level (for convenience), that define the buttons of the graphical interface (typically different in python 3.4 or python 2.7)
"""
# texts on buttons & frames
title_main_window = 'select your choices for the plot(s)'
title_frame1 = '1. select chemical species'
text_x = 'x-axis:'
text_y = 'y-axis:'
text_z = 'z-axis:'
text5 = 'scale:'
text_time_slice = 'time slice:'
text_time_min = '     tmin:' # the white spaces are made on purpose to enlarge the text
text_time_max = '     tmax:'
text_radius_min = ' radmin'
text_radius_max = '  radmax'
text_altitude_min = 'z/H min'
text_altitude_max = 'z/H max'
text_radius_slice = 'radius slice:'
text_altitude_slice = 'z/H slice:'
text_reduced_altitude = 'z-axis format:'
text_add_button = 'add'
text_remove_button = 'remove'
text_warning_continue = 'the continue button below must'
text_warning_continue2 = 'be clicked when axes are modified'
text_continue_button = 'continue'
title_frame2 = '2. select axes and scales'
title_frame3 = '3. select slices & min/max (time in years, z & radius in AU, z/H dimensionless)'
text_plot_button = 'plot'

# buttons sizes. note the buttons are larger in python 2.7 than in 3.4+ because the font is larger
from sys import version_info
if version_info[0]>2:
    width_variable_button = width_x_button = width_3D_button = 10
    width_variable_grid = width_x_grid = width_3D_grid = 12
    width_scale_button = width_plot_button = 7
    width_scale_grid = width_max_grid = width_min_grid = width_plot_grid = 9
    width_fmt_button = 9
    width_fmt_grid = 10
    width_timeslice_button = width_radiusslice_button = width_altitudeslice_button = 12
    width_timeslice_grid = width_radiusslice_grid = width_altitudeslice_grid = 14
    width_min_button = width_max_button = 12
    width_continue_button = 10
    width_max_grid = width_min_grid = 14
    width_continue_grid = 12
else:
    width_variable_button = width_x_button = width_3D_button = 12
    width_variable_grid = width_x_grid = width_3D_grid = 14
    width_scale_button = width_plot_button = 10
    width_scale_grid = width_max_grid = width_min_grid = width_plot_grid = 12
    width_timeslice_button = width_radiusslice_button = width_altitudeslice_button = 14
    width_timeslice_grid = width_radiusslice_grid = width_altitudeslice_grid = 16
    width_min_button = width_max_button = 10
    width_continue_button = width_max_grid = width_min_grid = 12
    width_continue_grid = 14

# enumerations. for compatibility with python 2.7 & 3.4+, I found convenient to define a specific 'enum' class
from sph_enum import sph_enum
order = ['x','y','z']# ugly: TODO: look for a pythonic way 
# warning: the name 'possible_values_along_x' is obsolete (but kept for compatibility, could be easily removed...(?)
possible_values_along_x = ["time", "radius", "z"]
# new format allowing several spellings for one key
# for instance, here, there are 3 keys: 'time', 'radius' and 'altitude'; 'altitude' can also be noted 'alt' or 'z'
possible_primary_variable_for_enum = ['time','radius',['altitude','alt','z']]
possible_primary_variable = ['time','radius','z']

# warning: the name 'possible_values_from_nautilus' is obsolete (but kept for compatibility, could be easily removed...
possible_values_from_nautilus = possible_nautilus_variable = ["abundance", "density", "column"]

# old warning (still useful ?): order matters !!! it is important to have first 'along_x' variables, then 'nautilus' variables, then 'none'
possible_variable_for_enum = possible_primary_variable_for_enum + possible_nautilus_variable
possible_variable = possible_primary_variable + possible_nautilus_variable
#possible_variable_along_z = possible_variable + ['none']
possible_variable_along_z = possible_nautilus_variable + ['none']

nautilus_variable = sph_enum("nautilus_variable",*possible_nautilus_variable)

# warning: the name 'x_variable' is obsolete (but kept for compatibility, could be easily removed...
x_variable = sph_enum("x_variable",*possible_values_along_x)
primary_variable = sph_enum("primary_variable",*possible_primary_variable_for_enum)
                         
sph_variable = sph_enum("sph_variable",*possible_variable_for_enum)
sph_variable_with_none = sph_enum("sph_variable_with_none",*possible_variable_along_z) # bad name (bad choice) !!!
                         
scale_variable = sph_enum("scale_variable",\
                          "linear", "log")

altitude_fmt = sph_enum("altitude_fmt",\
                        'z_over_H','z')
    
