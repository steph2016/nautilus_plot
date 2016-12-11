# -*- coding: utf-8 -*-
r"""
nautilus_sph_pack3
==================

part of the nautilus - python pipeline (S. Paulin-Henriksson v0)
definitions
"""
import sys
import nautilus_plot_sph_global_variables
import numpy as np
if sys.version_info[0]>2:
    import tkinter as tk
    #import tkinter.ttk as ttk
else:
    import Tkinter as tk
    #import ttk
#
###########################
#
class SPH_params:
    """
    TBD
    """
    def __init__(self,frame=None,textslice='',textmin='',textmax='',\
      simple_list=[],width_slice_button=1,width_slice_grid=1):
        """
        Parameters
        ----------
        f : ttk.LabelFrame
        
        ...
        """
        if frame is None:
            sys.exit('parameters defined without any frame !!!')
        else:
            self._frame = frame
        self._remember_min = self._remember_max = self._remember_slice = -1
        if frame != 'gildas':
            self._svarslice = tk.StringVar(frame)
            self._svarmin = tk.StringVar(frame)
            self._svarmax = tk.StringVar(frame)
        else:
            self._svarslice = self._svarmin = self._svarmax = -1
        self._omslice = self._ommin = self._ommax = 0
        if frame != 'gildas':
            self._labelmin = tk.Label(frame, text=textmin)
            self._labelmax = tk.Label(frame, text=textmax)
            self._labelslice = tk.Label(frame, text=textslice)
        else:
            self._labelmin = textmin
            self._labelmax = textmax
            self._labelslice = textslice
        self._simple_list = simple_list
        self._width_slice_button = width_slice_button
        self._width_slice_grid = width_slice_grid
        self._slice_index=-1
###################################
    def reminder(self):
        if isinstance(self._remember_min,str):
            self._svarmin.set(self._remember_min)
        if isinstance(self._remember_max,str):
            self._svarmax.set(self._remember_max)
        if isinstance(self._remember_slice,str):
            self._svarslice.set(self._remember_slice)
#
################################
#
class sph_plotfromtxt:
    """
    TBD
    """
    def __init__(self,filename='out.txt'):
        """
        TBD
        """
        comments=[]
#    axes={}
        self._speclist=[]
        for line in open(filename, 'rt'):
        # I do not know how to read only lines beginning with a specific caracter.
            if line[0] == nautilus_plot_sph_global_variables.\
              general_comment_sign:
                comments.append(line)
    # now read lines without the specific caracter
        tab=np.loadtxt(filename,\
          comments=nautilus_plot_sph_global_variables.general_comment_sign)
        self._nbdim=2
        for i, j in enumerate(comments):
            if j.find('xlabel')>0:
                self._xkind = (j.split('xlabel: ')[1]).rstrip()
                self._xkind = self._xkind.replace('altitude','z')
 #           axes['x'] = xkind
            elif j.find('ylabel')>0:
                self._ykind = (j.split('ylabel: ')[1]).rstrip()
                self._ykind = self._ykind.replace('altitude','z')
 #           axes['y'] = ykind
            elif j.find('zlabel')>0:
                self._zkind = (j.split('zlabel: ')[1]).rstrip()
                self._zkind = self._zkind.replace('altitude','z')
 #           axes['z'] = zkind
                self._nbdim = 3
            elif j.find('species')>0:
                self._speclist.append((j.split('species ')[1]).rstrip())           

        if len(self._speclist) < 1:
            sys.exit('pb: no species found...')
        if self._nbdim==3 and len(self._speclist)>1:
            sys.exit('pb: when nbdim==3, only 1 species allowed. several found...')
# TODO: complete tests to verify compliance
        if self._nbdim==2:
            lendim = len(tab) / (1 + len(self._speclist))
            prim=tab[0:lendim]
            val=np.empty([len(self._speclist),lendim])
            for i,j in enumerate(self._speclist):
                istart = (i+1)*lendim
                ifin = istart + lendim
                val[i,:]=tab[istart:ifin]
            if self._xkind.find('time')>0 or \
              self._xkind.find('radius')>0 or \
              self._xkind.find('z')>0:
                self._xval=prim
                self._yval=val
            else:
                self._yval=prim
                self._xval=val
            self._zval=None
        else:
            lendim=len(tab)/3
            self._xval=tab[0:lendim]
            self._yval=tab[lendim:2*lendim]
            self._zval = tab[2*lendim::]
