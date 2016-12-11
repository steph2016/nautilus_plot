r"""
nautilus_sph_pack2
==================

part of the nautilus - python pipeline (S. Paulin-Henriksson v0)
this is a set of useful definitions
"""
import numpy as np
import sys
import scipy.integrate # for cumulative integration only when computing the column density (function scipy.integrate.cumtrapz)

import sph_util
import nautilus_plot_sph_global_variables
import nautilus_sph_define_buttons
import nautilus_sph_pack1

import nautilus_sph_indices_and_variables
#
#########################
#
class SPH_1Dvariable(nautilus_sph_pack1.SPH_species):
    r"""
    TBC...
    
    Parameters
    ----------
    species_name : string
    variable : int corresponding to a nautilus_variable
        can represent 'abundance', 'density' (in part.cm-3) or 'column' (in part.cm-2)
    simu : SPH_nautilus_simulation
    axis : SPH_axis
    altitudeindex,radiusindex,timeindex : int, list of int or None (TODO: SPH_index obj)
            
    Example
    -------
    >>> v=SPH_1Dvariable(species_name='C',\
variable=nautilus_sph_define_buttons.nautilus_variable.density,\
simu=simu,axis=x,altitudeindex=0,radiusindex=1,timeindex=np.arange(9))
    """
    # TODO: must avoid loading the whole simu.
    def __init__(self,species_name=None,variable=None,simu=None,\
                 axis=None,\
                 altitudeindex=None,radiusindex=None,timeindex=None,\
                 ):
        # warning: test not comprehensive as it would be ok with 'time', 'radius', 'z' or 'none'
        if variable not in \
          nautilus_sph_define_buttons.sph_variable.dictReverse.keys():
            sys.exit('pb: variable name not understood')
#
        simu =\
            nautilus_sph_pack1.read_nautilus_simulation(simu)
#
##################        # temporary for debugging...
        if axis._variable._kind == \
          nautilus_sph_define_buttons.primary_variable.time:
            timeindex=None
        elif axis._variable._kind == \
          nautilus_sph_define_buttons.primary_variable.radius:
            radiusindex=None
        else:
            altitudeindex=None
#############################################
                
# note 'self' because it is inherited !!!
        nautilus_sph_pack1.SPH_species.__init__(self,name=species_name,
          nautilus_simulation=simu)
        self._axis = axis
       

        self.altitudeindex = sph_util.SPH_index(
          index=altitudeindex,minindex=axis._minindex,maxindex=axis._maxindex)
        self.timeindex = sph_util.SPH_index(
          index=timeindex,minindex=axis._minindex,maxindex=axis._maxindex)
        self.radiusindex = sph_util.SPH_index(
          index=radiusindex,minindex=axis._minindex,maxindex=axis._maxindex)
          #TODO: getting rid of indices obj

        indices = nautilus_sph_indices_and_variables.SPH_indices(
          self.altitudeindex,self.timeindex,self.radiusindex)

###################        # temporary for debugging...
# ???!!! 160228 # keep in mind the altitude is in reversed order in simu...
# altitudeindex is only used to read simu ==> reversed
        if isinstance(indices._indices[0],int):
            altitudeindex = simu.\
                  _nautilus_simulation_one_radius[0].\
                  _static_data._vertical_resolution -1 -indices._indices[0]
        else:
            altitudeindex = []
            for i,j in enumerate(indices._indices[0]):
                temp = simu.\
                  _nautilus_simulation_one_radius[0].\
                  _static_data._vertical_resolution -1 -j
                altitudeindex.append(temp)
 #       altitudeindex = indices._indices[0]                 
        timeindex = indices._indices[1]
        radiusindex = indices._indices[2]
            #############################################
            
        if variable == nautilus_sph_define_buttons.sph_variable.abundance:
            self._variable =\
              nautilus_sph_indices_and_variables.SPH_variable(\
              values=self._abundance[indices._indices],kind=variable)
        elif variable == nautilus_sph_define_buttons.sph_variable.density:
            self._variable =\
              nautilus_sph_indices_and_variables.SPH_variable(\
              values=self.compute_density(altitudeindex=self.altitudeindex),
                kind=variable)
        else: #implicitely, variable=='column'
            self._variable =\
              nautilus_sph_indices_and_variables.SPH_variable(\
              values=self.compute_column_density(nautilus_simulation=simu),
              kind=variable)

###################################

    def compute_density(self,altitudeindex=None,format='1D'):#self.altitudeindex):
        """
        TBC...
        """
        #print('entre dans la func')
        ab = self.get_abundance(altitudeindex=altitudeindex,
                              timeindex=self.timeindex,
                              radiusindex=self.radiusindex)
        h_density = self.get_h_density(altitudeindex=altitudeindex,
                              timeindex=self.timeindex,
                              radiusindex=self.radiusindex)
        tab = np.multiply(ab,h_density)
        if format=='1D':
            return tab.reshape([ab.size]) 
        else:
            return tab
###################################
    def compute_column_density(self,nautilus_simulation=None):
        # reminder: abundances are sorted in Increasing order (==> indice 0 corresponds to the disk while indice max corresponds to the surface)
        nbsuppindex,greatestaltindex = sph_util.sph_minmax(
          self.altitudeindex.listindex)
        # to deal with the case alt=0 ==> column=0
        if greatestaltindex < 1:#implicitely alt is a slice (ie. not along an axis)
            return np.zeros([len(self.radiusindex.listindex)*
              len(self.timeindex.listindex)])
        ########################################
        usefulaltitudeindex = sph_util.SPH_index(
          minindex=0,maxindex=greatestaltindex)# reminder: usefulaltitudeindices has greatestaltindex elemnts !!!
        density = self.compute_density(altitudeindex=usefulaltitudeindex,format='3D')
        column_density = np.empty([greatestaltindex,
                                   len(self.timeindex.listindex),
                                   len(self.radiusindex.listindex)]) # the returned value will have len(altitudeindices)-1 values but for the moment, need all the scale from 0
        for i,j in enumerate(self.timeindex.listindex):
            for k,l in enumerate(self.radiusindex.listindex):
                # note the calculation is performed for each time. for the moment useless but the alt values could be different for different time values
                column_density[:,i,k] = scipy.integrate.cumtrapz(density[:,i,k],
                        x=nautilus_simulation._reduced_altitude[:greatestaltindex+1]*
                        nautilus_simulation._nautilus_simulation_one_radius[l].
                        _static_data._scale_height)
          # factor 2 because we go across both side of the disk !!!
          # factor conv_dist top get values in cm^-2 instead of UA^-2 (the dx was in UA during integration)
        column_density *= 2 * nautilus_plot_sph_global_variables.conv_dist
        if len(self.altitudeindex.listindex) == 1:
            return column_density[-1,:,:].reshape([
              len(self.radiusindex.listindex)*
              len(self.timeindex.listindex)])
        else:#implicitely alt is the primary variable
            return column_density[nbsuppindex:,0,0].reshape(
                [len(self.altitudeindex.listindex)-1])
#
#####################################
#
class SPH_2Dvariable:
    r"""
    TBD...
    
    Parameters
    ----------
    species_name : string
    simu : SPH_nautilus_simulation
    variable_name :
    axes : list of SPH_axis
    altitudeindex, radiusindex, timeindex : int, lists of int or None
    boolaltfmt : boolean
    
    Example
    -------
    >>>        ...
    """
    def __init__(self,species_name,simu,variable_name, \
                 axes,\
                 altitudeindex=None,radiusindex=None,timeindex=None,boolaltfmt=False):
        self._axes = axes
        self._variable = variable_name
        self._radiusindex = radiusindex
        self._timeindex = timeindex
        self._altitudeindex = altitudeindex
        self._simu = simu
        s1 = len(axes[0]._values)
        s2 = len(axes[1]._values)
        # for debugging
        self._x2D = np.empty([s2,s1])
        self._y2D = np.empty([s2,s1])
        self._values = np.empty([s2,s1])
        self._tab1dvar = []
        ##############
            # for dealing with the case ...%radius%alt. temporary for debugging !!!
        if self._axes[0]._variable._kind == \
          nautilus_sph_define_buttons.primary_variable.radius and \
          self._axes[1]._variable._kind == \
          nautilus_sph_define_buttons.primary_variable.z and \
          boolaltfmt:
            hval = np.empty(s1)
            for i in range(s1):
                hval[i] = simu.\
                      _nautilus_simulation_one_radius[i].\
                      _static_data._scale_height
            ##################################################################################

            # WARNING!!!!!
#        kind = nautilus_sph_define_buttons.possible_values_from_nautilus.index(variable_name)
        kind = nautilus_sph_define_buttons.possible_variable.index(variable_name)
#        kind = nautilus_sph_define_buttons.possible_variable_along_z.index(variable_name)
####################################
        for i,j in enumerate(axes[1]._values):
            if axes[1]._variable._kind == \
              nautilus_sph_define_buttons.primary_variable.time:
                timeindex = i
            elif axes[1]._variable._kind == \
              nautilus_sph_define_buttons.primary_variable.radius:
                radiusindex = i
            else:
                altitudeindex = i
            temp = SPH_1Dvariable(species_name=species_name,\
                   variable=kind,\
                   simu=simu,\
                   axis=axes[0],\
                   altitudeindex=altitudeindex,radiusindex=radiusindex,timeindex=timeindex)
        # for debugging
            self._values[i,:] = temp._variable._values
            self._tab1dvar.append(temp)
            self._x2D[i,:] = axes[0]._values
            self._y2D[i,:] = np.repeat(j,s1)
#################            
            #  for dealing with the case ...%radius%alt. temporary for debugging !!!
            if self._axes[0]._variable._kind == nautilus_sph_define_buttons.x_variable.radius and \
              self._axes[1]._variable._kind == nautilus_sph_define_buttons.x_variable.z and \
              boolaltfmt:
                self._y2D[i,:] = \
                  np.multiply(self._y2D[i,:],hval)
