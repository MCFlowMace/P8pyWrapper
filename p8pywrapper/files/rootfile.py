#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  rootFile.py
#  
#  Authors Florian Thomas <fthomas@uni-mainz.de> and René Reimann <rreimann@uni-mainz.de>
#  
#  Date 10/19/2020
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

import re
import numpy as np
import uproot

class DataContainer(object):
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
    
class RootFile(object):
    def __init__(self, path):
        self.path = path
        self.f = uproot.open(path)
        
    # ~ def getTree(self, name):
        # ~ tree = self.f.Get(name)
        # ~ array, labels = tree.AsMatrix(return_labels=True)
        # ~ dtype = [(name, np.float) for name in labels]
        # ~ tree = np.array([tuple(line) for line in array], dtype=dtype)
        # ~ return tree
    
    def keys(self):
        return self.f.keys()
    
    def getHistogram1D(self, name):
        hist = self.f.get(name)
        if not hist: 
            print("Histogram with name {name} not in file")
            return None
        bins = hist.bins
        edges = hist.edges
        values = hist.values
        underflow = hist.underflows
        overflow = hist.overflows
        xlabel = hist.xlabels
        #ylabel = hist.GetYaxis().GetTitle() #ylabel seems to be non-existent
        title = hist.title
        return DataContainer(edges=edges, hist=values, underflow=underflow, overflow=overflow, xlabel=xlabel, title=title)
    
    def getHistogram2D(self, name):
        hist = self.f.get(name)
        if not hist:
            print("Histogram not in file.")
            return None
        edges = hist.edges
        values = hist.values
        xlabel = hist.xlabels
        ylabel = hist.ylabels
        #zlabel = hist.GetZaxis().GetTitle() #zlabel seems to be non-existent
        title = hist.title
        return DataContainer(edges_x=edges[0], edges_y=edges[1], hist=values, xlabel=xlabel, ylabel=ylabel, title=title)
    
    def getHistogram(self, name):
        hist = self.f.get(name)
        if not hist:
            print("Histogram not in file.")
            return None
        if hist._classname==b'TH1D':
            hist = self.getHistogram1D(name)
        elif hist._classname==b'TH2D':
            hist = self.getHistogram2D(name)
        else:
            raise ValueError("Can only handle 1D and 2D histograms.")
        return hist
    
    def get_pars_by_filename(self):
        find_pitch = re.findall("_Angle([\d\.]*)", self.path)
        pitchAngle = None if not find_pitch else float(find_pitch[0])
        find_radius = re.findall("_Radius([\d\.]*)", self.path)
        radius = None if not find_radius else float(find_radius[0])
        find_position = re.findall("_Pos([\d\.]*)\.root", self.path)
        position = None if not find_position else float(find_position[0])
        return (pitchAngle, radius, position)


