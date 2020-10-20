#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  plotwrapper.py
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

class PlotWrapper:

    def __init__(self):

        #self.fig, self.ax = plt.subplots()
        self.initialized = False

    def add(self, f, *args):

        if not self.initialized:
            self.fig, self.ax = plt.subplots()
            
        f(self.fig, self.ax, *args)

    def finish(self, name=''):

        if name=='':
            display(self.fig)
        else:
            self.fig.savefig(name)
        
        plt.close(self.fig)
        self.initialized = False
        
    def save(self, name):
        
        self.fig.savefig(name)

    @classmethod
    def plot(cls, f, *args, name=''):

        #just a shorthand for quick plots

        tmp = cls()
        tmp.add(f, *args)
        tmp.finish(name)
