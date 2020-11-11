#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  datacontainer.py
#  
#  Copyright 2020 Florian Thomas <fthomas@uni-mainz.de>
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
from .plotting import PlotWrapper

class DataContainer(object):
    
    #interesting idea but maybe inheritance is better choice long-term?
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
            
    def data(self):
        
        #questionable design choice
        if self.container=='TH1D':
            
            return self.yvalues, self.xvalues, None
            
        elif self.container=='TH2D':
            
            return self.zvalues, self.xvalues, self.yvalues
            
        else:
            
            return None
    
    #not sure yet if plot functionality should stay in the class like that        
    def plot(self):
        
        PlotWrapper.plot(self.externalPlot)
        
        
    def _plotHist2D(self, fig, ax):
        
        xmin = self.edges_x[0]
        xmax = self.edges_x[-1]
        ymin = self.edges_y[0]
        ymax = self.edges_y[-1]

        im = ax.imshow(self.zvalues.transpose(), 
                        extent=(xmin, xmax, ymin, ymax), 
                        origin='lower', zorder=2)
        cbar = fig.colorbar(im)

        ax.set_aspect('equal')
        ax.set_xlabel(self.xlabel)
        ax.set_ylabel(self.ylabel)
        ax.set_title(self.title)
        cbar.ax.set_ylabel(self.zlabel)
    
    def _plotHist1D(self, ax):
    
        ax.step(self.xvalues,self.yvalues)
        ax.set_xlabel(self.xlabel)
        ax.set_ylabel(self.ylabel)
        ax.set_title(self.title)
        
    #gives the option of modifying the plot
    def externalPlot(self, fig, ax):
        
        if self.container=='TH1D':
            self._plotHist1D(ax)
            
        elif self.container=='TH2D':
            self._plotHist2D(fig, ax)
            
        else:
            raise ValueError("Can only handle 1D and 2D histograms.")
