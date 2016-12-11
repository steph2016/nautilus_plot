r"""
nautilus_sph_plot
=================
part of the nautilus - python pipeline (S. Paulin-Henriksson v0)

graphical interface
"""
#import sph_util
import nautilus_sph_define_buttons
import nautilus_sph_pack1
import nautilus_sph_pack2
import nautilus_sph_pack3
import nautilus_sph_indices_and_variables
import nautilus_plot_sph_global_variables
import nautilus_sph_global_variables

import numpy as np
import matplotlib.pyplot as plt # for most plotting functions
#from mpl_toolkits.mplot3d import Axes3D
#from matplotlib.colors import LogNorm
import matplotlib.colors # for colorscaling in 3D plots
import sys
#testing the python version: 2.7 or 3.3+
if sys.version_info[0]>2:
    import tkinter as tk
    import tkinter.ttk as ttk
else:
    import Tkinter as tk
    import ttk
#
##########################
#
class SPH_windowplot:
    r"""
    graphical window... TBC
    Parameters
    ----------
    master : tk.Tk() object
    simu : pkl
        a pickle file containing a nautilus simulation. simu can be the file name of the pickle file or directly the 'SPH_nautilus_simulation' object.

    Example
    -------
    >>> root = tk.Tk()
    >>> window1 = nautilus_sph_plot.SPH_windowplot(root)
    """
# modif 161210
#    def __init__(self,master,simu='nautilus_simulation1510.pkl'):
    def __init__(self,master,simu=nautilus_sph_global_variables.pickle_filename):
################################################
        self._continue_count = 0 # to count the number of times the continue button is clicked
        self._master = master
        self._simu =\
            nautilus_sph_pack1.read_nautilus_simulation(simu)
# initialisation list of chemical species        
        self._speclist = self._simu._gas_list.getcolumn('name')._values + \
          self._simu._grain_list.getcolumn('name')._values
# initialisation list of bins for time, radius and z. these 'simple' lists are only
# used for convenient screening : they show the number of the bin together with
# 3 digits
        time_simp = \
              ['%d: %.2e' % (i+1,\
              j*nautilus_plot_sph_global_variables.conv_time) \
              for i, j in enumerate(self._simu._time)]
        radius_simp = \
              ['%d: %.2e' % (i+1, j) \
              for i, j in enumerate(self._simu._radius)]
# modif 160212: _reduced_altitude must be in the pickle file,
# already in reverse order
        altitude_simp = \
            ['%d: %.2e' % (i+1, j) \
            for i, j in enumerate(self._simu._reduced_altitude)]
# initialisation LabelFrames
        self._f = ttk.LabelFrame(\
          self._master,text=nautilus_sph_define_buttons.title_frame1)
        self._f2 = ttk.LabelFrame(\
          self._master,text=nautilus_sph_define_buttons.title_frame2)
        self._f3 = ttk.LabelFrame(\
          self._master,text=nautilus_sph_define_buttons.title_frame3)
# initialisation parameters of time, radius and z
        self._timeparams = nautilus_sph_pack3.SPH_params(frame=self._f3,\
          textslice=nautilus_sph_define_buttons.text_time_slice, \
          textmin=nautilus_sph_define_buttons.text_time_min,\
          textmax=nautilus_sph_define_buttons.text_time_max,\
          width_slice_button = nautilus_sph_define_buttons.width_timeslice_button,\
          width_slice_grid = nautilus_sph_define_buttons.width_timeslice_grid,\
          simple_list=time_simp)
        self._radiusparams = nautilus_sph_pack3.SPH_params(frame=self._f3,\
          textslice=nautilus_sph_define_buttons.text_radius_slice, \
          textmin=nautilus_sph_define_buttons.text_radius_min,\
          textmax=nautilus_sph_define_buttons.text_radius_max,\
          width_slice_button = nautilus_sph_define_buttons.width_radiusslice_button,\
          width_slice_grid = nautilus_sph_define_buttons.width_radiusslice_grid,\
          simple_list=radius_simp)
        self._altitudeparams = nautilus_sph_pack3.SPH_params(frame=self._f3,\
          textslice=nautilus_sph_define_buttons.text_altitude_slice, \
          textmin=nautilus_sph_define_buttons.text_altitude_min,\
          textmax=nautilus_sph_define_buttons.text_altitude_max,\
          width_slice_button = nautilus_sph_define_buttons.width_altitudeslice_button,\
          width_slice_grid = nautilus_sph_define_buttons.width_altitudeslice_grid,\
          simple_list=altitude_simp)
# running
        self.__frame1()
        self.__frame2()

######################

    def __frame2(self):
        self._f2.pack(expand=1,fill=tk.BOTH)
        
#        list_val = nautilus_sph_define_buttons.possible_values_from_nautilus
#        list_x = nautilus_sph_define_buttons.possible_values_along_x
#        list_3rd = ['none'] + list_x
        list_y = list_x = nautilus_sph_define_buttons.possible_variable
        list_z = nautilus_sph_define_buttons.possible_variable_along_z
        list_fmt = \
          nautilus_sph_define_buttons.scale_variable.dictReverse.values()
        list_altfmt = \
          nautilus_sph_define_buttons.altitude_fmt.dictReverse.values()
#
        self._wx = tk.Label(self._f2, text=nautilus_sph_define_buttons.text_x)
        self._wx.grid(row=0, column=0, sticky=tk.E)
        self._xval = tk.StringVar(self._f2)
        self._omx = tk.OptionMenu(self._f2, self._xval, *list_x)
        self._omx.config(\
          width=nautilus_sph_define_buttons.width_variable_button)
        self._omx.grid(\
          row=0, column=1, padx=nautilus_sph_define_buttons.width_variable_grid)
#
        self._wy = tk.Label(self._f2, text=nautilus_sph_define_buttons.text_y)
        self._wy.grid(row=1, column=0, sticky=tk.E)
        self._yval = tk.StringVar(self._f2)
        self._omy = tk.OptionMenu(self._f2, self._yval, *list_y)
        self._omy.config(width = nautilus_sph_define_buttons.width_x_button)
        self._omy.grid(\
          row=1, column=1, padx=nautilus_sph_define_buttons.width_x_grid)
#
        self._wz = tk.Label(\
          self._f2, text=nautilus_sph_define_buttons.text_z)
        self._wz.grid(row=2, column=0, sticky=tk.E)
        self._zval = tk.StringVar(self._f2)
        self._zval.set('none')
        self._omz = tk.OptionMenu(self._f2, self._zval, *list_z)
        self._omz.config(width=nautilus_sph_define_buttons.width_3D_button)
        self._omz.grid(\
          row=2, column=1, padx=nautilus_sph_define_buttons.width_3D_grid)
#
        self._wscax = tk.Label(self._f2, text=nautilus_sph_define_buttons.text5)
        self._wscax.grid(row=0, column=2, sticky=tk.E)
        self._scax = tk.StringVar(self._f2)
        self._omscax = tk.OptionMenu(self._f2, self._scax, *list_fmt)
        self._omscax.config(\
          width = nautilus_sph_define_buttons.width_scale_button)
        self._omscax.grid(\
          row=0, column=3, padx=nautilus_sph_define_buttons.width_scale_grid)
#
        self._wscay = tk.Label(self._f2, text=nautilus_sph_define_buttons.text5)
        self._wscay.grid(row=1, column=2, sticky=tk.E)
        self._scay = tk.StringVar(self._f2)
        self._omscay = tk.OptionMenu(self._f2, self._scay, *list_fmt)
        self._omscay.config(\
          width = nautilus_sph_define_buttons.width_scale_button)
        self._omscay.grid(\
          row=1, column=3, padx=nautilus_sph_define_buttons.width_scale_grid)
#
        self._wscaz = tk.Label(self._f2, text=nautilus_sph_define_buttons.text5)
        self._wscaz.grid(row=2, column=2, sticky=tk.E)
        self._scaz = tk.StringVar(self._f2)
        self._omscaz = tk.OptionMenu(self._f2, self._scaz, *list_fmt)
        self._omscaz.config(\
          width = nautilus_sph_define_buttons.width_scale_button)
        self._omscaz.grid(\
          row=2, column=3, padx=nautilus_sph_define_buttons.width_scale_grid)
#
        self._waltfmt = tk.Label(\
          self._f2, text=nautilus_sph_define_buttons.text_reduced_altitude)
        self._waltfmt.grid(row=1, column=4, sticky=tk.E)
        self._altfmt = tk.StringVar(self._f2)
        self._altfmt.set(nautilus_sph_define_buttons.altitude_fmt.dictReverse[0])
        self._omaltfmt = tk.OptionMenu(self._f2, self._altfmt, *list_altfmt)
        self._omaltfmt.config(\
          width = nautilus_sph_define_buttons.width_fmt_button)
        self._omaltfmt.grid(\
          row=1, column=5, padx=nautilus_sph_define_buttons.width_fmt_grid)
#
        self._continue_button = tk.Button(\
            self._f2,text=nautilus_sph_define_buttons.\
            text_continue_button,command=self.__makelistaxes)
        self._continue_button.config(\
            width = nautilus_sph_define_buttons.width_continue_button)
        self._continue_button.grid(\
            row=2,column=6,padx=nautilus_sph_define_buttons.width_continue_grid)
        self._w22 = tk.Label(\
            self._f2, text=nautilus_sph_define_buttons.text_warning_continue)
        self._w22.grid(row=0, column=6, sticky=tk.E)
        self._w23 = tk.Label(\
            self._f2, text=nautilus_sph_define_buttons.text_warning_continue2)
        self._w23.grid(row=1, column=6, sticky=tk.E)

# convenient debugging values when debug option enabled
        if nautilus_plot_sph_global_variables.debug_values:
            self._yval.set('abundance')
            self._xval.set('time')
            self._scax.set('log')
            self._scay.set('log')
            self._altfmt.set('z_over_H')
            self.__defslices()

###########################

    def __frame1(self):
        self._f.pack(expand=1)# why not try grid ? warning: the grid method crashes !!!
        self._list_spec = tk.Listbox(self._f,selectmode=tk.EXTENDED,height=4)
        if sys.version_info[0]>2:
            self._scrollbar1 = tk.Scrollbar(self._list_spec, orient=tk.VERTICAL)
            self._list_spec.config(yscrollcommand=self._scrollbar1.set)
        self._list_chosen_spec = tk.Listbox(\
          self._f,selectmode=tk.EXTENDED,height=6)
        if sys.version_info[0]>2:
            self._scrollbar2 = tk.Scrollbar(\
              self._list_chosen_spec, orient=tk.VERTICAL)
            self._list_chosen_spec.config(yscrollcommand=self._scrollbar2.set)
        self._tb1 = tk.Button(\
          self._f,text=nautilus_sph_define_buttons.\
          text_add_button,command=self.__addspec)
        self._tb2 = tk.Button(\
          self._f,text=nautilus_sph_define_buttons.\
          text_remove_button,command=self.__removespec)          
        self._spec = tk.StringVar(self._f)
        self._t=tk.Entry(self._f,textvariable=self._spec)
        self._list_spec.grid(row=0,column=0,rowspan=4)
        # better/pythonic way to do this ?!
        for i, j in enumerate(self._speclist):# use extend, see google 
            self._list_spec.insert(tk.END, j)
        ####################
        self._tb1.grid(row=1,column=1)
        self._tb2.grid(row=2,column=1)
        self._list_chosen_spec.grid(row=0,column=2,rowspan=6)
        self._t.grid(row=5,column=0)
# convenient debugging values when debugging is on
        if nautilus_plot_sph_global_variables.debug_values:
            self._spec.set('C,Fe')
            self.__addspec()
            
###########################

    def __addspec(self):
        written = self._spec.get().split(',')
        
# useful test but lousy coding... better/pythonic way to do that ?
        if '' in written:
            written.remove('')
####################

        selected=[]
        if written:
            for item in written:
                if item in self._list_chosen_spec.get(0,tk.END):
                    print('warning: ',item,\
                          ' already in the chosen list ==> ignored')
                elif item in self._list_spec.get(0,tk.END):
                    selected.append(item)
                else:
                    print('warning: ',item,' is not recognised ==> ignored')
        else:
            for index in self._list_spec.curselection():
                selected.append(self._list_spec.get(0,tk.END)[int(index)])
        if selected:
            for item in selected:
                self._list_chosen_spec.insert( tk.END, item )
                self._list_spec.delete( \
                    self._list_spec.get(0,tk.END).index(item) )

################################

    def __removespec(self):
        selected = []
        for index in self._list_chosen_spec.curselection():
            selected.append(self._list_chosen_spec.get(0,tk.END)[int(index)])
        if selected:
            for item in selected:
                self._list_chosen_spec.delete( \
                    self._list_chosen_spec.get(0, 'end').index(item) )
                self._list_spec.insert( self._speclist.index(item), item )

###############################

    def __defslices(self):
        self._continue_count+=1
        if self._continue_count == 1:
            self._f3.pack(expand=1,fill=tk.BOTH)
        if self._continue_count > 1:# comment: could be 'else' because continue_count is larger than 0 by def...
            for i,j in enumerate(\
              nautilus_sph_define_buttons.possible_primary_variable):
                if j=='time':
                    variableparams = self._timeparams
                elif j=='radius':
                    variableparams = self._radiusparams
                else: #implicitely 'altitude'
                    variableparams = self._altitudeparams
                valslice = variableparams._svarslice.get()
                valmin = variableparams._svarmin.get()
                valmax = variableparams._svarmax.get()
                variableparams._remember_slice = \
                  variableparams._remember_max = \
                  variableparams._remember_min = -1
                if isinstance(variableparams._omslice,tk.OptionMenu):
                    variableparams._remember_slice = valslice
                    variableparams._omslice.grid_remove()
                    variableparams._labelslice.grid_remove()
                if isinstance(variableparams._ommin,tk.OptionMenu):
                    variableparams._remember_min = valmin
                    variableparams._remember_max = valmax
                    variableparams._ommin.grid_remove()
                    variableparams._ommax.grid_remove()
# beware the confusion between forget() & .grid_remove() ?
                variableparams._labelmin.grid_remove()
                variableparams._labelmax.grid_remove()
            self._plotbut.forget() # useful ?
#
        numminmax = 0
        numslice = 0
#
        for i,j in enumerate(\
          nautilus_sph_define_buttons.possible_primary_variable):
            if j=='time':
                variableparams = self._timeparams
            elif j=='radius':
                variableparams = self._radiusparams
            else:# implicitely 'altitude'
                variableparams = self._altitudeparams
            if j in self._dict_axes.values():
                numminmax += 1
                variableparams._ommin = tk.OptionMenu(self._f3,\
                  variableparams._svarmin, *variableparams._simple_list)
                variableparams._ommax = tk.OptionMenu(self._f3,\
                  variableparams._svarmax, *variableparams._simple_list)
                variableparams._ommin.config(\
                  width=nautilus_sph_define_buttons.width_min_button)
                variableparams._ommax.config(\
                  width=nautilus_sph_define_buttons.width_max_button)
                variableparams.reminder()
                variableparams._ommin.grid(\
                  row=numminmax, column=1, \
                  padx=nautilus_sph_define_buttons.width_min_grid)
                variableparams._ommax.grid(\
                  row=numminmax, column=3, \
                  padx=nautilus_sph_define_buttons.width_max_grid)
                variableparams._omslice = 0
                variableparams._labelmin.grid(row=numminmax, column=0, sticky=tk.E)
                variableparams._labelmax.grid(row=numminmax, column=2, sticky=tk.E)
            else:
                numslice += 1
                num = 2*(numslice-1)
                variableparams._labelslice.grid(row=0, column=num, sticky=tk.E)
                variableparams._omslice = tk.OptionMenu(self._f3,\
                  variableparams._svarslice, *variableparams._simple_list)
                variableparams.reminder()
                variableparams._omslice.config(width = variableparams._width_slice_button)
                variableparams._omslice.grid(row=0, column=num+1, \
                  padx=variableparams._width_slice_grid)
                variableparams._ommin = variableparams._ommax = 0
        self._plotbut = tk.Button(\
            self._f3,text=nautilus_sph_define_buttons.text_plot_button,\
            command=self.__plot)
        self._plotbut.config(\
            width = nautilus_sph_define_buttons.width_plot_button)
        self._plotbut.grid(\
            row=1,column=4,padx=nautilus_sph_define_buttons.width_plot_grid)
# convenient debugging values
        if nautilus_plot_sph_global_variables.debug_values:
            self._radslice.set('2: 1.00e+02')
            self._altslice.set('33: 2.05e+00')
            self._timemin.set('10: 1.00e+01')
            self._timemax.set('29: 1.29e+03')
            
###############################

    def __plot(self,write=True):
        self._fig = plt.figure()
        self._frame1 = self._fig.add_subplot(1,1,1)
        
# dealing with the nautilus variable
        kind = nautilus_sph_define_buttons.possible_variable.index(\
                 self._dict_axes[nautilus_sph_define_buttons.order\
                 [self._position_nautilus_variable]])
        self._nautilus_variable = \
          nautilus_sph_indices_and_variables.SPH_variable(kind=kind)

# dealing with other variable(s) 
        for i,j in enumerate(\
          nautilus_sph_define_buttons.possible_primary_variable):
            if j=='time':
                variableparams = self._timeparams
            elif j=='radius':
                variableparams = self._radiusparams
            else:# implicitely 'altitude'
                variableparams = self._altitudeparams
            if ':' in variableparams._svarslice.get():
                variableparams._slice_index = \
                  int((variableparams._svarslice.get().split(':'))[0]) -1
            else:
                variableparams._slice_index = None

        self._axes = []
        if self._altfmt.get() == 'z':
            radiusindex_used_for_alt = self._radiusparams._slice_index
        else: # implicitely fmt is 'z_over_H':
            radiusindex_used_for_alt = None
        for i,j in enumerate(sorted(self._dict_axes)):
            if self._list_axetype[i] == 'primary':
                var = self._dict_axes[j]
                if var == 'time':
                    variableparams = self._timeparams
                elif var == 'radius':
                    variableparams = self._radiusparams
                else:# implicitely var == 'z':
                    variableparams = self._altitudeparams
                minvar = variableparams._svarmin.get()
                maxvar = variableparams._svarmax.get()
                if ':' in minvar:
                    minindex = int((minvar.split(':'))[0]) -1
                else:
                    minindex = None
                if ':' in maxvar:    
                    maxindex = int((maxvar.split(':'))[0]) -1
                else:
                    maxindex = None
#                
                kind = nautilus_sph_define_buttons.possible_variable.index(var)
                temp = nautilus_sph_indices_and_variables.SPH_axis(
                  primaryvariable=kind,\
                  simu=self._simu,minindex=minindex,maxindex=maxindex,\
                  radiusindex_used_for_alt=radiusindex_used_for_alt)
                self._axes.append(temp)
        self.__maketitle()
#        
        if self._nbdim == 2:
            self.__plot2D()
        else:
            self.__plot3D()
        if write:
            self.__write_plot()

        plt.show() # seems necessary according to 'http://stackoverflow.com/questions/458209/is-there-a-way-to-detach-matplotlib-plots-so-that-the-computation-can-continue' to ensure window is not closed
        
############################

    def __plot2D(self):
        t=[]
        labels=[]
        nbcol = len(nautilus_plot_sph_global_variables.colors)
        self._chosen_species = []
        kind = nautilus_sph_define_buttons.possible_variable.index(\
               self._dict_axes[nautilus_sph_define_buttons.order[\
               self._position_nautilus_variable]])
        for spec_cur in self._list_chosen_spec.get(0, tk.END):
            temp = nautilus_sph_pack2.SPH_1Dvariable(\
                  species_name=spec_cur,\
                  variable=kind,\
                  simu=self._simu, \
                  axis=self._axes[0],\
                  altitudeindex=self._altitudeparams._slice_index,\
                  radiusindex=self._radiusparams._slice_index,\
                  timeindex=self._timeparams._slice_index)   
            self._chosen_species.append(temp)# comment 160106: the name 'chosen_species' is not clear anymore since it doesn't contain strings but 'SPH_1Dvariable' objects
#
        if kind == nautilus_sph_define_buttons.sph_variable.column and \
          self._chosen_species[0]._axis._variable._kind == \
          nautilus_sph_define_buttons.sph_variable.altitude:
            self._chosen_species[0]._axis._values = (
              self._chosen_species[0]._axis._values[0:-1]+
              self._chosen_species[0]._axis._values[1:])/2
#
              
        if  self._list_axetype[0] == 'primary':
            xlab = self._axes[0]._variable._label
            ylab = self._nautilus_variable._label
            xval = self._chosen_species[0]._axis._values                
        else:
            xlab = self._nautilus_variable._label
            ylab = self._axes[0]._variable._label
            yval = self._chosen_species[0]._axis._values
        self._frame1.set_xlabel(xlab)
        self._frame1.set_ylabel(ylab)
#            
        for i1, i2 in enumerate(self._chosen_species):
            if  self._list_axetype[0] == 'primary':
                yval = i2._variable._values
            else:
                xval = i2._variable._values
            
            temp, = self._frame1.plot(xval,yval,'bo', label=i2._name, \
                color=nautilus_plot_sph_global_variables.colors[i1%nbcol])
            temp, =  self._frame1.plot(xval,yval, '-', \
                color=nautilus_plot_sph_global_variables.colors[i1%nbcol])
            labels.append(i2._name)
            t.append(temp)
            
        self._frame1.grid(True)
        plt.legend(t,labels,loc=2)
        if self._scax.get() == 'log':
            plt.xscale('log')
        if self._scay.get() == 'log':
            plt.yscale('log')

        plt.draw()

############################

    def __plot3D(self):
        if nautilus_plot_sph_global_variables.VERBOSE_LEVEL > 0:
            s = 'this is a 3D plot ==> only the first species is plotted'
            s += ', even if several were selected'
            nautilus_sph_pack1.printwarning(s)
        temp = (self._list_chosen_spec.get(0, 0))[0]
        temps = self._dict_axes['z']
        self._var2D = nautilus_sph_pack2.SPH_2Dvariable(\
            temp,\
            self._simu,temps, \
            self._axes,\
            altitudeindex=self._altitudeparams._slice_index,\
            radiusindex=self._radiusparams._slice_index,\
            timeindex=self._timeparams._slice_index,
            boolaltfmt=self._altfmt.get()=='z')
#
        self._frame1.set_xlabel(self._axes[0]._variable._label)
        if self._xval.get() == 'radius' and \
          self._yval.get() == 'z' and \
          self._altfmt.get() == 'z':
            self._frame1.set_ylabel('altitude')
        else:
            self._frame1.set_ylabel(self._axes[1]._variable._label)
#
        interp=nautilus_plot_sph_global_variables.interpolation_scheme_3D
        if self._scaz.get() == 'log':
            nnn = matplotlib.colors.LogNorm()
        else:
            nnn = matplotlib.colors.Normalize()
            
        plt.pcolormesh(self._var2D._x2D,self._var2D._y2D,\
                self._var2D._values,\
                norm=nnn,\
                shading=interp)
#
        plt.xlim( [np.min(self._var2D._x2D), np.max(self._var2D._x2D)] )
        plt.ylim( [np.min(self._var2D._y2D), np.max(self._var2D._y2D)] )
#
        tit = self._nautilus_variable._label + '(' +\
          (self._list_chosen_spec.get(0, 0))[0] + ')'
        colbar = plt.colorbar()
        colbar.set_label(tit)
        if self._scax.get() == 'log':
            plt.xscale('log')
        if self._scay.get() == 'log':
            plt.yscale('log')

        plt.draw()

###############################

    def __write_plot(self):
        if self._nbdim==2:
            if self._list_axetype[0] == 'primary':
                ylabel = self._chosen_species[0]._variable._label
                xlabel = self._axes[0]._variable._label
            else:
                xlabel = self._chosen_species[0]._variable._label
                ylabel = self._axes[0]._variable._label
        else:# impliciely ndim==3==> z is the nautilus variable
            #list_axes = [self._x.get(),self._third.get()]
            xlabel = self._axes[0]._variable._label
            ylabel = self._axes[1]._variable._label
            if self._yval.get()=='z' and 'radius' not in self._dict_axes.values():
                ylabel += self.__addH()
            zlabel = self._var2D._tab1dvar[0]._variable._label
        if self._xval.get()=='z' and 'radius' not in self._dict_axes.values():
            xlabel += self.__addH()
#
        l = ['text file, SPH-nautilus-python script ' +\
                  nautilus_plot_sph_global_variables.version]
        l.append('nbdim = %i' % self._nbdim)   
        l.append('xlabel: ' + xlabel)
        l.append('ylabel: ' + ylabel)
        if self._nbdim == 3:
            l.append('zlabel: ' + zlabel)
        if 'z' not in self._dict_axes.values():
            temp = self._simu._reduced_altitude[self._altitudeparams._slice_index]
            s = 'altitude/H value: ' + str(temp)
            if 'radius' not in self._dict_axes.values():
                s += self.__addH()
            l.append(s)
        if 'radius' not in self._dict_axes.values():
            s = 'radius value: ' + str(\
                  self._simu._radius[self._radiusparams._slice_index]) + \
                  ' [AU]'
            l.append(s)
        if 'time' not in self._dict_axes.values():
            temp = self._simu._time[self._timeparams._slice_index] * \
                  nautilus_plot_sph_global_variables.conv_time
            s = 'time value: ' + str('%e' % temp)
            #s = 'time value: ' + str(temp)
            s += ' [years]'
            l.append(s)
        l.append('---> ' + self._axes[0]._variable._label + ' values:')
        if self._nbdim == 2:
            val = self._axes[0]._values
        else:
            val=self._var2D._x2D
        savecomment(\
          filename=nautilus_plot_sph_global_variables.txt_filename,\
          mode='wt',listofstrings=l)
        #output.write(str(xval) + '\n')
        savendarray(\
          filename=nautilus_plot_sph_global_variables.txt_filename,\
          ndarray=val)

# following preliminary for debugging but not optimised for the weird behaviour of numpy.savetxt()
        if self._nbdim == 2:
            l = ['---> ' + self._chosen_species[0]._variable._label + ' values:']
            savecomment(\
              filename=nautilus_plot_sph_global_variables.txt_filename,\
               mode='at',listofstrings=l)
        
            for i,j in enumerate(self._chosen_species):
                l = ['* for species ' + j._name]
                savecomment(\
                   filename=nautilus_plot_sph_global_variables.txt_filename,\
                   mode='at',listofstrings=l)
                savendarray(\
                   filename=nautilus_plot_sph_global_variables.txt_filename,\
                   ndarray=j._variable._values)
        else:# implicitely 3D
            l = ['---> ' + self._axes[1]._variable._label + ' values:']
            savecomment(\
              filename=nautilus_plot_sph_global_variables.txt_filename,\
              mode='at',listofstrings=l)
            savendarray(\
              filename=nautilus_plot_sph_global_variables.txt_filename,\
              ndarray=self._var2D._y2D)
            temp = self._list_chosen_spec.get(0, 0)
            l = ['---> ' + self._zval.get() + ' values:']
            l.append('* for species ' + str(temp))
            savecomment(\
                   filename=nautilus_plot_sph_global_variables.txt_filename,\
                   mode='at',listofstrings=l)
            savendarray(\
                   filename=nautilus_plot_sph_global_variables.txt_filename,\
                   ndarray=self._var2D._values)

#########################

    def __addH(self):
        s = ' (H='
        s += '%e' % self._simu.\
           _nautilus_simulation_one_radius[self._radiusparams._slice_index].\
           _static_data._scale_height
        s += ' [AU])'
        return s        

#########################

    def __maketitle(self):
        tit = self._nautilus_variable._simplified_label
        tit += ' .vs. ' + self._axes[0]._variable._simplified_label
        if self._nbdim == 3:
            tit += ' .vs. ' + self._axes[1]._variable._simplified_label
        subtit = 'for: '
        slicecount = 0
        #if ':' in self._altitudeparams._svarslice.get():
        if 'z' not in self._dict_axes.values():
            subtit += 'z/H=' + (self._altitudeparams._svarslice.get().split(':'))[1]
            slicecount += 1
        #if ':' in self._timeparams._svarslice.get():
        if 'time' not in self._dict_axes.values():
            if slicecount > 0:
                subtit += ' ; '
            subtit += 'time=' + (self._timeparams._svarslice.get().split(':'))[1] + ' [years]'
            slicecount += 1
        #if ':' in self._radiusparams._svarslice.get():
        if 'radius' not in self._dict_axes.values():
            if slicecount > 0:
                subtit += ' ; '
            subtit += 'radius=' + (self._radiusparams._svarslice.get().split(':'))[1] + ' [AU]'
        plt.title(subtit,fontsize=nautilus_plot_sph_global_variables.subtitle_fontsize)
        plt.suptitle(tit,fontsize=nautilus_plot_sph_global_variables.title_fontsize)# note, the matplotlib command is not 'subtitle' but 'suptitle' !!! the suptitle appears ABOVE the title !!! that is why tit ans subtit are upside down !!!

########################

    def __makelistaxes(self):
        #self._dict_nautilus_axes = {}
        #self._dict_primary_axes = {}
        comment = False
# reorganisation 1: if the x axis is empty, y->x and z->y and 'none'->z
        if self._xval.get() == 'none' or self._xval.get() == '':
            self._xval.set(self._yval.get())
            self._yval.set(self._zval.get())
            self._zval.set('none')
            comment = True
# reorganisation 2: if the y axis is empty, z->y and 'none'->z
        if self._yval.get() == 'none' or self._yval.get() == '':
            self._yval.set(self._zval.get())
            self._zval.set('none')
            comment = True
        if comment:
            s = 'reorganisation of variables...'
            nautilus_sph_pack1.printwarning(s)
#
        self._dict_axes = {'x': self._xval.get(),\
          'y': self._yval.get(),'z': self._zval.get()}
        self._list_axetype = []
#
# it turns out python dictionnaries are not sorted !!!
# ==> a simple enumerate(dict) do not list all the keys in the order !!!
# to have an ordered enumeration, a couple of solutions exist
# like the following or ordered dict (TBV)
        for j in sorted(self._dict_axes.keys()):
            if self._dict_axes[j] in \
              nautilus_sph_define_buttons.possible_primary_variable:
                self._list_axetype.append('primary')
            elif self._dict_axes[j] in \
              nautilus_sph_define_buttons.possible_nautilus_variable:
                self._list_axetype.append('nautilus')
        self._nbdim = len(self._list_axetype)
        ok = True
# test 1: there can be only 1 or 2 primary variable(s) and 1 nautilus variable
        if self._nbdim<2 or self._nbdim>3 or \
          self._list_axetype.count('nautilus') != 1:
            ok = False
# test 2: if 3D the nautilus variable must be on the z axis
        if self._nbdim==3 and self._list_axetype[2] != 'nautilus':
            ok = False
# test 3: if 3D x must be different than y
        if self._nbdim==3 and self._xval.get()==self._yval.get():
            ok = False
# test 4: if 3D and altitude is a variable, then it must be along the y-axis
        if self._nbdim==3 and \
          'z' in self._dict_axes.values() and \
          self._dict_axes['y'] != 'z':
            ok = False
#
        if ok:
            # convenient but could be optimised
            self._position_nautilus_variable = \
              self._list_axetype.index('nautilus')
            self._list_axetype.append('none')
            #self._
            self.__defslices()
        else:
            s='the choice of axes is not compliant with this version of the script. '
            s+='reminder of the rules: '
            s+='1. the plot must have one and only one axe from nautilus'
            s+=' and the same variable cannot be selected twice ; '
            s+='2. if the plot is 3D, '
            s+='the nautilus variable must be along the z-axis ; '
            s+='3. if the plot is 3D and the altitude is one of the variables, '
            s+='the altitude (often noted "z") must be along the y-axis.'
            nautilus_sph_pack1.printwarning(s)
#
#######################
#        
def savendarray(filename='toto.txt',ndarray=np.array([0])):
    # it turns out numpy.savetxt() requires to open the file in BINARY mode to save it in TEXT mode... weird... probably not understood or this sucks...
    f=open(filename,'ab')
    np.savetxt(f,ndarray)
    f.close()
#
######################
#
def savecomment(filename='toto.txt',mode='wt',listofstrings=['tutu']):
    with open(filename,mode) as output:
        for i, j in enumerate(listofstrings):
            output.write(nautilus_plot_sph_global_variables.\
                         general_comment_sign + ' ' + j + '\n')
      
