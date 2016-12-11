r"""
nautilus_plot_sph_global_variables
==================================
part of the nautilus - python pipeline (S. Paulin-Henriksson v0)
Global variables for plotting available at all level (for convenience), that describes the plotting part
"""
conv_time = 3.17e-8 # conversion factor to get time in years (couldn't this be more accurate ?!)
conv_dist = 1.496e13 # conversion factor to write 1AU in cm

colors = ['b','g','r','c','m','y']

VERBOSE_LEVEL = 1

version = 'v0'

#debug_values = True # when set, the variables have default values convenient for debugging.
debug_values = False

label_time = 'time [years]'
label_time_simplified = 'time'
label_radius = 'radius [AU]'
label_radius_simplified = 'radius'
label_altitude = 'altitude [AU]'
label_altitude_simplified = 'altitude'
label_reduced_altitude = 'altitude / H'
label_abundance = label_abundance_simplified = 'abundance'
label_density = 'density [cm-3]'
label_density_simplified = 'density'
label_column = 'column [cm-2]'
label_column_simplified = 'column'
title_fontsize = 20
subtitle_fontsize = 12
####################################

interpolation_scheme_3D = 'gouraud' # interpolation scheme for the 3D interpolation. it turns out the pyplot.pcolormesh() is quite poor as the interpolation scheme can only be 'gouraud' or 'flat'. warning: with the 'flat' scheme, (N-1)x(N-1) rectangular non-centered pixels will be drawn, where x,y,z are NxN ndarrays : the right hand column and the upper line of z are lost !!!
 
##################################

write_plot = True # if true, an ascii file is written on the disk for each new plot
txt_filename = 'out.txt' # warning: in this version, the ascii filename is always the same and overwritten for each plot.

##################################

# not implemented yet
#plotting_device = 'matplotlib' #may be 'matplotlib' or 'gildas'
#plotting_device = 'gildas'

#################################

general_comment_sign = '#' # the quiet universal comment sign is '#' but it can be chosen here. For instance, even if I don't see the point, it can be an old-fashion-1970style '!'

