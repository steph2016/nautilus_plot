r"""
nautilus_sph_pack1
==================

part of the nautilus - python pipeline (S. Paulin-Henriksson v0)

some definitions...
"""
# modif 160129 to get rid of astropy
#from astropy.table import Table # TBC !!! it seems possible/easy to avoid astropy
import sph_table
###################################
import numpy as np
import sys
import os
import pickle
import struct # used to read binary files
import subprocess

import nautilus_sph_global_variables
import sph_util
#import nautilus_sph_pack1
# useless
#import nautilus_plot_sph_global_variables
#import nautilus_sph_define_buttons
#import nautilus_sph_indices_et_variables
#
#########################
#
class SPH_species:
    r"""
    chemical species defined by a molecule name and possibly abundances if linked to a nautilus simulation. attributes: _name (string), _kind(int corresponding to the 'chemical_species_kind' enum), _content_line (list of strings), _abundance(ndarray or none)
    
    Parameters
    ----------
    name : string
        name of the species in the '...species.in' files
        
    Other parameters
    ----------------
    nautilus_simulation : SPH_nautilus_simulation or string giving a filename, default None
        if of type SPH_nautilus_simulation or filename, then ._numline gives the rank of the specie in the simulation (eg. in the '...species.in' files), ._kind may be 'gas' or 'grain' and '._content_line' is the full line of the corresponding '...species.in' file
              
    abundance_in_memory: boolean, default True.
        if nautilus_simulation is properly defined and abundance_in_memory, then the 3D abundance (z x time x radius, in this order !) is kept in memory. if no nautilus_simulation, this keyword is ignored
        
    Examples
    --------
    >>> SPH_species(name='C')
    >>> SPH_species(name='MgH2',nautilus_simulation='sim151013.pkl')
    """
    def __init__(self,name='H',nautilus_simulation=None,abundance_in_memory=True):
        self._name = name
        self._content_line = []
        self._numline = -1
        self._nautilus_simulation_ID = None # TODO: not useful yet
        if nautilus_simulation!=None:
            nautilus_simulation = read_nautilus_simulation(nautilus_simulation)
            #TODO:
            # self._nautilus_simulation_ID = nautilus_simulation._ID
            self.locate_species(nautilus_simulation)
            if abundance_in_memory:
                self.__load_abundance(nautilus_simulation)
#            self._abundance = np.empty([nbaltitude,nbtime,nbradius])
#            for i,j in enumerate(simu._radius):
#                self.H_density.append(simu._nautilus_simulation_one_radius[i].\
#                   _H_number_density[0,::-1])
        else:
            self._kind = ''
            #self._nautilus_simulation_ID = None#nautilus_simulation._ID
            self._abundance = None
####################
    def __load_abundance(self,simu):
        # modif 160129 to get rid of astropy
        #nbaltitude = len(simu._nautilus_simulation_one_radius[0]._static_data._tab['Distance [AU]'])
        nbaltitude = len(simu._nautilus_simulation_one_radius[0]._static_data._tab.getcolumn('Distance [AU]')._values)
     
        nbtime = len(simu._time)
        nbradius = len(simu._radius)
        self._abundance = np.empty([nbaltitude,nbtime,nbradius])
        self.h_density = np.empty([nbaltitude,nbtime,nbradius])
        for i in range(nbradius):
            self._abundance[:,:,i] = \
              simu._nautilus_simulation_one_radius[i]._abundances[self._numline,::-1,:] # '::-1' for sorting correctly the altitude (reminder: in the simu, the altitude is in the reversed order !)
            self.h_density[:,:,i]= \
              simu._nautilus_simulation_one_radius[i].\
              _H_number_density[:,::-1].T# partly useless because bins are the same for all times
              #warning 2: note alt-time order is not the same !!! ==> transpose
######################
    def locate_species(self,nautilus_simulation):
        r"""            
        Parameters
        ----------
        nautilus_simulation : SPH_nautilus_simulation
            locate the species in the nautilus simulation, ie. gives the line number, the kind and the full line of the corresponding '...species.in' file
            
        Example
        -------
        >>> species.locate_species(sim151013)
        """
        self._kind = 'gas'
        tab = nautilus_simulation._gas_list
        self.__locate(tab)
        if self._numline < 0:
            self._kind = 'grain'
            tab = nautilus_simulation._grain_list
            self.__locate(tab)
        if self._numline < 0:
            print(self._name,"...")
            sys.exit('pb: species unknown...')
###########################
    def __locate(self,tab):
        # modif 160129 to get rid of astropy
        #l = list(tab['name'])
        l = tab.getcolumn('name')._values
        if self._name in l:
            self._numline = l.index(self._name)
            # modif 160129 to get rid of astropy
            #self._content_line = list(tab[self._numline])
            self._content_line = tab._core[self._numline]
#############################
    def get_abundance(self,timeindex=None,altitudeindex=None,radiusindex=None):
        r"""
        convenient interface to handle the abundance array. in function of indices, an array is returned th
    
        Parameters
        ----------
        timeindex,altitudeindex,radiusindex : SPH_index objects    
    
        Example
        -------
        >>> H.get_abundance(radiusindex=r,timeindex=t,altitudeindex=a)    
        """
        if isinstance(altitudeindex,sph_util.SPH_index) and \
          isinstance(timeindex,sph_util.SPH_index) and \
          isinstance(radiusindex,sph_util.SPH_index):
            tab = self._abundance[np.ix_(altitudeindex.listindex,
                                         timeindex.listindex,
                                         radiusindex.listindex)]
        else:
            tab = 0
        return tab
#############################
    def get_h_density(self,timeindex=None,altitudeindex=None,radiusindex=None):
        r"""
        convenient interface to handle the h_density array. in function of indices, an array is returned th
    
        Parameters
        ----------
        timeindex,altitudeindex,radiusindex : SPH_index objects    
    
        Example
        -------
        >>> H.get_abundance(radiusindex=r,timeindex=t,altitudeindex=a)    
        """
        if isinstance(altitudeindex,sph_util.SPH_index) and \
          isinstance(timeindex,sph_util.SPH_index) and \
          isinstance(radiusindex,sph_util.SPH_index):
            tab = self.h_density[np.ix_(altitudeindex.listindex,
                                         timeindex.listindex,
                                         radiusindex.listindex)]
        else:
            tab = 0
        return tab
#
##############################
#
class SPH_static_file:
    r"""
    describe a nautilus file of type '1D_static.dat'. warning: assume a specific fmt !!!

    Parameters
    ----------
    filename : string, default=='1D_static.dat'
        commentsign: (string, usually 1 character) default is specified in 'nautilus_sph_global_variable.py'

    Examples
    --------
    >>> f=SPH_static_file()
    >>> f=SPH_static_file(filename='toto',commentsign='#')
    """
    def __init__(self,filename='1D_static.dat',\
                 commentsign=nautilus_sph_global_variables.comment_sign_in_static_file):
        self._filename = filename
        self._commentsign = commentsign
# warning: assume a specific fmt !!!
# TODO: very clumsy reading, quickly changed to get rid of astropy! must be optimised !
        self._columnnames = nautilus_sph_global_variables.column_names_in_static_file
        for line in open(filename,'rt'):
            #while line[0] == commentsign:
            if line.find('Midplan temperature (K) at 100 AU')>0:
                self._midplan_temperature_100 = float((line.split())[-1])
            elif line.find("Atmosphere (4H) temperature (K) at 100 AU")>0:
                self._atmo_temperature_100 = float((line.split())[-1])
            elif line.find('Radius where the structure is computed (cm)')>0:
                self._radius = float((line.split())[-1])
            elif line.find('Midplan temperature (K) at the requested radius')>0:
                self._midplan_temperature_radius = float((line.split())[-1])
            elif line.find('Atmosphere temperature (K) at the requested radius')>0:
                self._atmo_temperature_radius = float((line.split())[-1])
            elif line.find('Mass of the central object (g)')>0:
                self._mass_central = float((line.split())[-1])
            elif line.find('UV field coming from the star at 100 AU')>0:
                self._uv_field_100 = float((line.split())[-1])
            elif line.find('UV field coming from the star at the requested radius')>0:
                self._uv_field_radius = float((line.split())[-1])
            elif line.find('Vertical resolution')>0:
                self._vertical_resolution = int((line.split())[-1])
            elif line.find('Scale Height H in au')>0:
                self._scale_height = float((line.split())[-1])
                
                
        # modif or getting rid of astropy
        #self._tab = Table.read(filename, format='ascii',comment=commentsign, \
        #        names=self._columnnames) # TBC !!! it seems possible/easy to avoid astropy
        self._tab = sph_table.SPH_table(filename, commentsign=commentsign, \
                columnnames=self._columnnames)

        # modif 160129 for getting rid of astropy
        #if len(self._tab) != self._vertical_resolution:
        if len(self._tab._core) != self._vertical_resolution:
            sys.exit("error: the vertical resolution indicated in the header does not correspond to the number of lines in the table")
#
##############################################
#
class SPH_nautilus_outputfile:
    r"""
    represents an output nautilus file (usually a .out), as saved in binary by the fortran program using the (lousy & painful) 'f77' fmt.
    
    Parameters
    ----------
    nautilus_outputfilename : str, default=='abundances.out'
    nb_z: int, default==64
        number of altitude bins. 
            
    Examples
    --------
    >>> f=SPH_nautilus_outputfile()
    >>> f=SPH_nautilus_outputfile(nautilus_outputfilename='toto',nb_z=100)
    """
    def __init__(self,nautilus_outputfilename='abundances.out', \
                 nb_z=64):
        values = self.__read_nwrite(abundance_file=nautilus_outputfilename)
        self._time = float(values[0][0])
        self._gas_temperature = np.array(values[1][0:nb_z])
        self._dust_temperature = np.array(values[1][nb_z:2*nb_z])
        self._H_number_density = np.array(values[1][2*nb_z:3*nb_z])
        self._visual_extinction = np.array(values[1][3*nb_z:4*nb_z])
        self._x_ionisation_rate = float(values[1][4*nb_z])
        self._abundances = np.array(values[2])
####################
    def __read_nwrite(self,abundance_file,n=3):
        values = []
        with open(abundance_file,'rb') as fff:
            for i in range(n):
                val = self.__read_1write(fff)
                values.append(val)
        return values
####################
    def __read_1write(self,t,si=4,sd=8):
        # first, read an int giving the # of bytes of the next data
        temp=struct.unpack('i',t.read(si))
        temp=int(temp[0])
        # then, read n doubles
        n=int(temp/sd)
        values=struct.unpack('d'*n,t.read(temp))
        # then, another int (the same, why did fortran do that ?! maybe its to be able to read in the backward direction...)
        temp=struct.unpack('i',t.read(si))
        return values
#
########################################################
#
class SPH_nautilus_simulation_1r:
    r"""
    describe an usual 1-radius nautilus simulation
    Parameters
    ----------
    nbpoints_time : int, default==64
    nbspecies : int, default 737
    static_filename : string, default=='1D_static.dat'
            
    Examples
    --------
    >>> s=SPH_nautilus_simulation_1r()
    >>> s=SPH_nautilus_simulation_1r(nbpoints_time=10,nbspecies=50,static_filename='toto')
    """
    def __init__(self,nbpoints_time=64, \
                 nbspecies=737,static_filename='1D_static.dat'):
        self._static_data = SPH_static_file(filename=static_filename)
        self._static_filename = static_filename
        self._time = np.empty([nbpoints_time])
        self._gas_temperature = np.empty([nbpoints_time,\
                               self._static_data._vertical_resolution])
        self._dust_temperature = np.empty([nbpoints_time,\
                               self._static_data._vertical_resolution])
        self._H_number_density = np.empty([nbpoints_time,\
                               self._static_data._vertical_resolution])
        self._visual_extinction = np.empty([nbpoints_time,\
                               self._static_data._vertical_resolution])
        self._x_ionisation_rate = np.empty([nbpoints_time])
        #warning !!!: space & time are inverted compared to the other tab !!!
        self._abundances = np.empty([nbspecies,\
                                     self._static_data._vertical_resolution,\
                                     nbpoints_time])
        radius_value = self._static_data._radius
        for timecounter in range(nbpoints_time):
# warning: assume a specific fmt !!!
# TODO: if the following copies values instead of pointers, this should be optimised. TBV
                filename = 'abundances.' + "%06i"%(timecounter+1) + '.out'
# modif 160131 to get rid of paths (then the script must be run in the directory containing the different radiuses)
#                filename = nautilus_sph_global_variables.general_path + \
#                  '/' + nautilus_sph_global_variables.path + '/' + \
                filename = "%03i"%radius_value + 'AU/' + filename
    
                temp = SPH_nautilus_outputfile(nautilus_outputfilename=filename,\
                                nb_z=self._static_data._vertical_resolution)
                self._time[timecounter] = temp._time
                self._gas_temperature[timecounter,:] = temp._gas_temperature
                self._dust_temperature[timecounter,:] = temp._dust_temperature
                self._H_number_density[timecounter,:] = temp._H_number_density
                self._visual_extinction[timecounter,:] = temp._visual_extinction
                self._x_ionisation_rate[timecounter] = temp._x_ionisation_rate
                self._abundances[:,:,timecounter] = \
                   temp._abundances.reshape(\
                      self._static_data._vertical_resolution,nbspecies).T # note the 'T' for the translation
#
########################################################
#
class SPH_nautilus_simulation:
    r"""
    entire nautilus simulation with several chemical species, radiuses, times, distances to the axis. default values correspond to the debugging run of the 151013: nbtimes=64, nbradius=3 (usual values nbspecies=737 and nbz=64 are given by joined ascii files). Chemical species are listed in joined ascii files (by default 'gas_species.in' and 'grain_species.in'), z values and co are also given in the joined ascii file (by default ''1D_static.dat''). All other values are read in binary files output of nautilus (usually '.out' files in a lousy 'f77' fmt)
    
    Parameters
    ----------
    nbpoints_time : int, default==64
        the number time values
    radiuses : list of int, default==[50,100,200]
        the radiuses (distances from the galactic center in AU) at witch the simulation were run
    gas_filename : string, default=='gas_species.in'
        the ascii file listing all gas species
    grain_filename: string, default=='grain_species.in'
        the ascii file listing all grain species    
    Examples
    --------
    >>> h = SPH_nautilus_simulation(nbpoints_time=64, radiuses=[50,100,200], gas_filename='gas_species.in', grain_filename='grain_species.in',simulation_ID='test')
    >>> h = SPH_nautilus_simulation()
    """
    def __init__(self,nbpoints_time=64, \
                 radiuses=[50,100,200], \
                 gas_filename='gas_species.in', \
                 grain_filename='grain_species.in', \
                 simulation_ID='nautilus_simulation1510.pkl'):
        self._ID = simulation_ID
        self._gas_filename = gas_filename
        self._grain_filename = grain_filename
        # modif 160129 to get rid of astropy
        #self._gas_list = Table.read(gas_filename, format='ascii',\
                #names=nautilus_sph_global_variables.column_names)# TODO: it seems easy & convenient to avoid astropy
        #self._nspec_gas = len(self._gas_list)
        self._gas_list = sph_table.SPH_table(filename=gas_filename,columnnames=nautilus_sph_global_variables.column_names)
        self._nspec_gas = len(self._gas_list._core)
        
        # modif 160129 to get rid of astropy
        #self._grain_list = Table.read(grain_filename, format='ascii',\
         #       names=nautilus_sph_global_variables.column_names)
        #self._nspec_grain = len(self._grain_list)
        self._grain_list = sph_table.SPH_table(filename=grain_filename,columnnames=nautilus_sph_global_variables.column_names)
        self._nspec_grain = len(self._grain_list._core)

        self._nspec_tot = self._nspec_gas + self._nspec_grain
        self._nb_radius = len(radiuses)
        self._radius = np.array(radiuses)
        self._nautilus_simulation_one_radius = []
        for radiuscounter in range(self._nb_radius):
# modif 160131 to get rid of paths (then the script must be run in the directory containing the different radiuses)
#fff = nautilus_sph_global_variables.general_path + \
 #                 '/' + nautilus_sph_global_variables.path + '/' + \
            fff = "%03i"%radiuses[radiuscounter] + 'AU/'
        
            static_filename = fff + nautilus_sph_global_variables.static_filename
            temp = SPH_nautilus_simulation_1r( \
                 nbpoints_time=nbpoints_time, \
                 nbspecies=self._nspec_tot, \
                 static_filename=static_filename)
            # in this simulation, it turns out that times and reduced_altitude are the always the same for any radius,
            #so it can be considered as a property of the whole nautilus simulation.
            #but it is not necessarily the case.
            if radiuscounter == 0:
                self._time = temp._time
                self._reduced_altitude = (np.array(temp._static_data\
                  ._tab.getcolumn('Distance [AU]')._values))[::-1] / \
                  temp._static_data._scale_height
            else:
                if not (self._time==temp._time).any():
                    sys.exit("pb: time values not the same in all the radius bins...")
                # TODO: same test for reduced alt
            del temp._time
            if temp._static_data._radius != radiuses[radiuscounter]:# add new
                sys.exit(\
                    "pb: radius values not the same in the command and in the static file")
            self._nautilus_simulation_one_radius.append(temp)
###################################
    def save(self,pickle_file='toto.pkl'):
        r"""
        Parameters
        ----------
        pickle_file : string, default=='toto.pkl'
           name of the save file

        Example
        -------
        >>> h.save(pickle_file='simu.pkl')
        """
        if not isinstance(pickle_file,str):# normaly useless...
            pickle_file = self._ID
        print('save nautilus simulation (%i species x %i times x %i altitudes x %i radius) in %s' \
          % (self._nspec_tot,len(self._time),\
             self._nautilus_simulation_one_radius[0]._static_data._vertical_resolution,\
             self._nb_radius,pickle_file))
        with open(pickle_file, 'wb') as output:
            pickle.dump(self, output, pickle.HIGHEST_PROTOCOL) # TODO: could be adapted to other protocoles
#
########################
#
def printwarning(output):
    r"""
    TBD
    """
    s = 'warning: '
    s += output
    print(s)
#
#######################
#
def read_nautilus_simulation(f):
    r"""
    Parameters
    ----------
        f : string or pkl
    """
    if isinstance(f,str): # 'f' is interpreted as a filename containing a nautilus simulation in a pickle format
        if not os.path.isfile(f):
            create_nautilus_simulation_pickle_fmt(f)
        with open(f,'rb') as input:
            simu = pickle.load(input)
    elif isinstance(f,SPH_nautilus_simulation): # 'f' is interpreted as the nautilus simulation itself
        simu = f
    else:
        print('pb with ',f)
        sys.exit("pb reading the nautilus simulation: input not understood (must be a file name or a 'SPH_nautilus_simulation' object)")
    return simu
#
###########################
#
def create_nautilus_simulation_pickle_fmt(pickle_file='nautilus_simulation1510.pkl',
                                          nbpoints_time=64,
                                          radiuses=[50,100,200],
                                          gas_filename='gas_species.in',
                                          grain_filename='grain_species.in',
                                          simulation_ID='nautilus_simulation1510',
                                          automatic_search=True
                                          ):
    """
        Parameters
    ----------
        pickle_file : string giving the filename or pickle file
        nbpoints_time : int
        radiuses : 
        gas_filename : 
        grain_filename : 
        simulation_ID : useless, must be significant in a future upgrade
        automatic_search :
    """
    if automatic_search: # then other values are not taken into account !!!
# search of available radiuses
        test = str(subprocess.check_output('ls -d *AU',shell=True))
        test = test.split('AU')
        radiuses = []
        for i,j in enumerate(test[0:-1]):
            radiuses.append(int(j[-3:]))
# search of nbpoints_time
        cmd = 'ls ' + "%03i"%radiuses[0] + 'AU/ab* | wc -l'
        nbpoints_time = int(subprocess.check_output(cmd,shell=True))
#
        gas_filename = nautilus_sph_global_variables.gas_filename
        grain_filename = nautilus_sph_global_variables.grain_filename
# warning: can be disabled to let the choice of the pickle filename to the gildas script
        pickle_file = nautilus_sph_global_variables.pickle_filename
#
    h = SPH_nautilus_simulation(nbpoints_time=nbpoints_time,
                                radiuses=radiuses,
                                gas_filename=gas_filename,
                                grain_filename=grain_filename,
                                simulation_ID=simulation_ID)
    h.save(pickle_file)
