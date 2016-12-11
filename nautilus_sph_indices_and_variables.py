r"""
nautilus_sph_indices_and_variable
=================================
part of the nautilus - python pipeline (S. Paulin-Henriksson v0)
objects SPH_variable, SPH_axis, SPH_index, SPH_indices. preliminary versions v000
"""
import numpy as np
import sys

import nautilus_plot_sph_global_variables
import nautilus_sph_define_buttons

import nautilus_sph_pack1
#
###########################
#
class SPH_variable:
    r"""
    describing a variable (currently 'time', 'radius', 'z'=='altitude' (?), 'abundance', 'density' or 'column'). attributes : _kind (int), _reduced (boolean), _norm (float), _values (array), _label (string)
    """
#
    def __init__(self,kind=0,\
                 values=None,norm=1.0,size=None,reduced=False):
        r"""
        Parameters
        ----------
            values: (ndarray) values of the variable. default None
            kind: (int corresponding to a 'sph_variable' --> definition in the file 'nautilus_sph_define_buttons.py', currently 0<->'time', 1<->'radius', 2<->'z'=='altitude' (?), 3<->'abundance', 4<->'density' or 5<->'column' or 6<->'none') nature of the variable. default 0 (ie. 'time')
            norm: (float) normalisation factor. if norm != 1 the original array is copied in memory and the copy is normalised by the factor norm. the original array is not modified. default 1
            size: (int) if values==None then a size must be given to initiate the ndarray. if the values are given, size is ignored. default None 
            reduced: (boolean) if True and this kind of variable can be reduced (currently only 'z' can be 'z/H') then this can be set here
            
        Example
        ------- 
            var = SPH_variable(values=array, kind=nautilus_sph_define_buttons.sph_variable.abundance)
        """
        if kind not in \
          nautilus_sph_define_buttons.sph_variable.dictReverse.keys():
            print('pb: kind ',kind,' unknown.')
            sys.exit('pb: a SPH_variable was defined with a weird kind ==> exit')
        self._kind = kind
        self._norm = norm
        self._reduced = reduced
        if isinstance(values,np.ndarray):
            self._values = values
            if norm != 1:
            # warning: the syntaxe 'x=x*y' (instead of 'x*=y') is required to avoid changing the original array !!!
            #indeed, with this syntaxe, a new array with modified values is created in memory
            # while the original array is not modified
                self._values = self._values*self._norm
        else:
            #note, the input must contain values or size
            self._values = np.empty(size)
        self.__setlabel()
#
    def __setlabel(self):
        if self._kind == nautilus_sph_define_buttons.sph_variable.time:
            self._label = \
              nautilus_plot_sph_global_variables.label_time
            self._simplified_label = \
              nautilus_plot_sph_global_variables.label_time_simplified
        elif self._kind == nautilus_sph_define_buttons.sph_variable.radius:
            self._label = \
              nautilus_plot_sph_global_variables.label_radius
            self._simplified_label = \
              nautilus_plot_sph_global_variables.label_radius_simplified
        elif self._kind == nautilus_sph_define_buttons.sph_variable.z:
            if self._reduced:
                self._label = \
                    nautilus_plot_sph_global_variables.label_reduced_altitude
            else:
                self._label = \
                    nautilus_plot_sph_global_variables.label_altitude
            self._simplified_label = \
                nautilus_plot_sph_global_variables.label_altitude_simplified
        elif self._kind == nautilus_sph_define_buttons.sph_variable.abundance:
            self._label = self._simplified_label = \
              nautilus_plot_sph_global_variables.label_abundance
        elif self._kind == nautilus_sph_define_buttons.sph_variable.density:
            self._label = \
              nautilus_plot_sph_global_variables.label_density
            self._simplified_label = \
              nautilus_plot_sph_global_variables.label_density_simplified
        elif self._kind == nautilus_sph_define_buttons.sph_variable.column:
            self._label = \
              nautilus_plot_sph_global_variables.label_column
            self._simplified_label = \
              nautilus_plot_sph_global_variables.label_column_simplified
#
#######################
#
class SPH_axis:
    r"""
    describing an axis of a non-nautilus variable (noted 'primary variable', currently 'time', 'radius' or 'z' (reduced or not)). attributs: _variable (SPH_variable), _simu (SPH_nautilus_simulation), _minindex (int), _maxindex (int), _values (1D array), _label_simplified & _label (str)
    
    160207: possible to define an axis just with the minimum info written in out.txt files if simu is Non. Then val must be an array and 'radiusindex_used_for_alt' is used as a boolean
    
    Parameters
    ----------
    simu : SPH_nautilus_simulation or str giving a filename
    primaryvariable : int corresponding to a 'primary_variable'
        currently 'time', 'radius' or 'z'), default value 0 (ie.'time')
    minindex, maxindex : int or None
        minimum and maximum indices to be taken into account. values[minindex] must be < values[maxindex] (and they both have to be meaningful), otherwise these keywords are ignored. note the altitude is in reversed order (min index = max value & max index = min value)
    radiusindex_used_for_alt : int or None
        meaningful only if the variable is altitude, then if int -> z ; if None -> of z_over_H
    val: if no simu...
        
    Example
    -------
    >>> axis=SPH_axis(variable=nautilus_sph_define_buttons.x_variable.time,\
                         simu='nautilus_simulation.pkl',\
                         mindex=10,maxindex=50,\
                         radiusindex_used_for_alt=1)
    """
    # rk: min/maxindex in input are expressed to describe the position in the ndarray SPH_species._abundance !!! ==> the altitude is in reversed order compared to simu !!! this means the galactic disk (ie. z=0) is at the beginning and the ndarray ends with z=much
    def __init__(self,primaryvariable=0,\
                 simu=None,\
                 minindex=0,maxindex=50,\
                 radiusindex_used_for_alt=None,
                 val=None,mute=False):
        variable=primaryvariable # for compatibility (160212)
# basic tests
        if variable not in \
          nautilus_sph_define_buttons.primary_variable.dictReverse.keys():
            print('pb: kind ',variable,' unknown.')
            sys.exit('pb: a SPH_axis was defined with a weird variable ==> exit')
        if simu != None:
            self._simu =\
              nautilus_sph_pack1.read_nautilus_simulation(simu)
        else:
            tab = val
            if not isinstance(tab,np.ndarray):
                sys.exit('pb: a SPH_axis was improperly defined...')    
# init the values and the labels
# 160212: use the variable labels
        reduced = False
        if variable == \
          nautilus_sph_define_buttons.primary_variable.time:
            if simu != None:
                tab = self._simu._time
                norm = nautilus_plot_sph_global_variables.conv_time
            else:
                norm=1
            #self._label_simplified = \
            #      nautilus_plot_sph_global_variables.label_time_simplified
            #self._label = \
            #      nautilus_plot_sph_global_variables.label_time
        elif variable == \
          nautilus_sph_define_buttons.primary_variable.radius:
            if simu != None:
                tab = self._simu._radius
            #self._label_simplified = \
            #      nautilus_plot_sph_global_variables.label_radius_simplified
            #self._label = \
            #      nautilus_plot_sph_global_variables.label_radius
            norm = 1.
        else:#implicitely variable is altitude
            if simu != None:
                tab = self._simu._reduced_altitude
                
                if isinstance(radiusindex_used_for_alt,int):# then the altitude is not reduced (ie: abs. values)
                    norm = \
                          self._simu.\
                          _nautilus_simulation_one_radius[radiusindex_used_for_alt].\
                          _static_data._scale_height
               #     self._label = \
               #           nautilus_plot_sph_global_variables.label_altitude
                else:
                    norm = 1.
                    reduced = True
               #     self._label = nautilus_plot_sph_global_variables.\
               #           label_reduced_altitude                
            else:# ie. if simu==None ==> just plot, then 'radiusindex_used_for_alt' is just a boolean
                norm = 1.
                if radiusindex_used_for_alt: #which, in the case 'no simu', is a boolean
                #    self._label = nautilus_plot_sph_global_variables.\
                #          label_reduced_altitude  
                    pass                
                else:
                    #self._label = nautilus_plot_sph_global_variables.\
                    #      label_altitude
                    reduced = True
            #self._label_simplified = nautilus_plot_sph_global_variables.\
            #          label_altitude_simplified
                                
        newkind=nautilus_sph_define_buttons.possible_variable.index(\
          nautilus_sph_define_buttons.possible_primary_variable[variable])
        self._variable =\
              SPH_variable(values=tab,kind=newkind,norm=norm,reduced=reduced)
# init minimum and maximum
        if simu != None and \
          isinstance(minindex,int) and \
          isinstance(maxindex,int) and \
          minindex < len(tab) and \
          minindex >= 0 and \
          maxindex < len(tab) and \
          maxindex >= 0 and \
          minindex < maxindex:
            self._minindex = minindex
            self._maxindex = maxindex
        else:
            self._minindex = 0
            self._maxindex = len(tab)-1
            if simu != None and not mute and \
              nautilus_plot_sph_global_variables.VERBOSE_LEVEL > 0:
                s = 'min/max values not understood on axis '
                s += nautilus_sph_define_buttons.x_variable.dictReverse[variable]
                s += ' ==> not taken into account'
                nautilus_sph_pack1.printwarning(s)
        self._values = self._variable._values[self._minindex:self._maxindex+1] # does this duplicate the values in memory ? if yes, obviously, this step could/should be avoided
#
##############################
#
#TODO: GETTING RID !!!
class SPH_indices:
    r"""
    set of 3 integer(s) used to read some value(s) in a ndarray. usually representing a set zindex/timeindex/radiusindex. each index can be an integer or a list of integers, the number of lists is put in an attribut '_nblist' and the lists are listed in the attribut '_numlist'. then the attribut '_combinaisons' lists all the possible sets of 3 integers. attributs: _indices (list), _nblist (int), _numlist (list), _numint (list), _combinaisons (list)
    TBC...
    """
    def __init__(self,i1,i2,i3):
        self._indices = [i1._index,i2._index,i3._index]
        self._nblist = 0
        self._numlist = []
        self._numint = [0,1,2]
        for j,k in enumerate([i1,i2,i3]):
            if not isinstance(k._index,int):
                self._nblist += 1
                self._numlist += [j]
                self._numint.remove(j)
                self._indices[j] = k._listindex         
        if self._nblist > 1:
            print('warning: several lists in indices...')
                        
        if self._nblist < 1:
            print('warning: no list in indices...')                           
        self._combinaisons = [] # _combinaisons still useful ?
        for c1, c1b in enumerate(i1._listindex):
            for c2, c2b in enumerate(i2._listindex):
                for c3, c3b in enumerate(i3._listindex):
                    temp = [c1b,c2b,c3b]
                    self._combinaisons.append(temp)
#
##################################
#
def reverseindex(listindices,vertical_resolution):
    """
    convenient conversion between altitude indices strarting from outside the cloud (==> indice 0 is the outside and indice max is the disk), like SPH_species objects, and indices strarting from the disk (indice 0 is the disk and the outside is indice max), like nautilus simulations   
    """
    return list(vertical_resolution-1-np.array(listindices))
    
