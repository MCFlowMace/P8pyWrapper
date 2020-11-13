#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  plotting.py
#  
#  Authors Florian Thomas <fthomas@uni-mainz.de>
#  
#  Date 10/20/2020
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

import matplotlib.pyplot as plt
import numpy as np

def run_from_ipython():
    try:
        __IPYTHON__
        return True
    except NameError:
        return False

class PlotWrapper:

    def __init__(self):

        #self.fig, self.ax = plt.subplots()
        self.initialized = False

    def add(self, f, *args):

        if not self.initialized:
            self.initialized = True
            self.fig, self.ax = plt.subplots()
            
        f(self.fig, self.ax, *args)

    def finish(self, name=''):

        if name=='':
            if run_from_ipython():
                display(self.fig)
            else:
                plt.show()
        else:
            self.fig.savefig(name)
        
        plt.close(self.fig)
        self.initialized = False
        
    def save(self, name):
        
        self.fig.savefig(name, dpi=600)

    @classmethod
    def plot(cls, f, *args, name=''):

        #just a shorthand for quick plots

        tmp = cls()
        tmp.add(f, *args)
        tmp.finish(name)


def plotBeamforming(fig, ax, R, data, cbar_label='', ax_unit='cm'):
    
    im_masked = np.ma.masked_where(data==0,data)
    im=ax.imshow(im_masked,extent=(-R,R,-R,R),origin='lower', zorder=2)

    cbar = fig.colorbar(im)
    ax.set_aspect('equal')
    ax.set_xlim(-(R+0.5),R+0.5)
    ax.set_ylim(-(R+0.5),R+0.5)
    
    xlabel='x[' + ax_unit + ']'
    ylabel='y[' + ax_unit + ']'
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    
    cbar.ax.set_ylabel(cbar_label)

def plotSpectrum(fig, ax, data, t_min, t_max, f_min, f_max, 
                    cbar_label='', x_unit='ms', y_unit='MHz'):
    
    im = ax.imshow(data.transpose(), extent=(t_min, t_max, f_min, f_max),
                        zorder=2, origin='lower')
    
    aspect = (t_max-t_min)/(f_max-f_min)*2 #data.shape[0]/data.shape[1]*2
    
    ax.set_aspect(aspect)
    
    cbar = fig.colorbar(im)
    xlabel='t[' + x_unit + ']'
    ylabel='f[' + y_unit + ']'
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    
    cbar.ax.set_ylabel(cbar_label)
