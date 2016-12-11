r"""
nautilus_sph_global_variables
=============================
part of the nautilus - python pipeline (S. Paulin-Henriksson v0)
Global variables available at all level (for convenience), that describe the nautilus files.
"""
fmt_outfiles = 'default' # otherwise ? for the momet only 1 fmt implemented... could it be a diff format for python 3.4+ or 2.7 ?

# names of the columns in '..._species.in' files
column_names = ['name','charge','H','He','C','N','O',\
                'Si','S','Fe','Na','Mg','Cl','P','F']
# number of columns in the '...species.in' files
nbcol = len(column_names)

column_names_in_static_file = ['Distance [AU]', 'H Gas density [part/cm^3]', \
                'Gas Temperature [K]', \
                'Visual Extinction [mag]', \
                'Diffusion coefficient [cm^2/s]']
comment_sign_in_static_file = '!'
static_filename = '1D_static.dat'

# try 161210
#pickle_filename = 'nautilus_simulation_oct2015-python27.pkl'
pickle_filename = 'nautilus_simulation_oct2015.pkl'
#############################

gas_filename = 'gas_species.in'
grain_filename = 'grain_species.in'

from sph_enum import sph_enum
chemical_species_kind = sph_enum("chemical_species_kind","gas","grain")

