#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  katydidP3.py
#  
#  Authors Florian Thomas <fthomas@uni-mainz.de>
#  
#  Date 10/21/2020
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

import numpy as np
import time

from .rootfile import RootFile

def filterfunc(key, literal, cycle='2'):
    return literal in key and key[-1]==cycle
    
def filteredKeys(keys, literal):
    f = lambda key: filterfunc(key, literal)
        
    return [key for key in filter(f, keys)]
    
#not nice to have two versions of both but that prevents 
#using a slowing if or loop
def extractIndices(key):
    keySplit = key[:-2].split('_')
    timeslice = int(keySplit[1])
    channel = int(keySplit[2])
    return timeslice, channel

def extractDims(keys):
    
    totalTimeslices=-1
    totalChannels=-1
    for key in keys:
        timeslice, channel = extractIndices(key)
        totalTimeslices = max(timeslice, totalTimeslices)
        totalChannels = max(channel, totalChannels)
        
    return totalTimeslices+1, totalChannels+1
    
def extractIndex(key):
    keySplit = key[:-2].split('_')
    timeslice = int(keySplit[1])
    return timeslice

def extractDimension(keys):
    
    totalTimeslices=-1
    for key in keys:
        timeslice = extractIndex(key)
        totalTimeslices = max(timeslice, totalTimeslices)
        
    return totalTimeslices+1
    
#functionality can be extended if required
class KatydidP3File():
    
    def __init__(self, filename):
        
        self._inputFile = RootFile(filename)
        self._keys = self._inputFile.keys()
    
    def _load1D(self, keysF):
        
        nTimeslices, nChannels = extractDims(keysF)
        value, x, y = self._inputFile.getHistogram(keysF[0]).data()
        timeslice, channel = extractIndices(keysF[0])
        
        nBins = x.shape[0]
        
        data = np.empty(shape=(nTimeslices, nChannels, nBins), 
                        dtype=value.dtype)

        data[timeslice, channel] = value
        
        for key in keysF[1:]:
            timeslice, channel = extractIndices(key)
            data[timeslice, channel] = self._inputFile.getDataFast(key)
        
        return x, data
        
    def _load2D(self, keysF):
        
        nTimeslices = extractDimension(keysF)
        value, x, y = self._inputFile.getHistogram(keysF[0]).data()
        timeslice = extractIndex(keysF[0])
        
        nGridx = x.shape[0]
        nGridy = y.shape[0]
        
        data = np.empty(shape=(nTimeslices, nGridx, nGridy), 
                        dtype=value.dtype)

        data[timeslice] = value
        
        for key in keysF[1:]:
            timeslice = extractIndex(key)
            data[timeslice] = self._inputFile.getDataFast(key)
        
        return x, y, data
    
    def loadTS(self):
        
        keysReal = filteredKeys(self._keys, 'histTSReal_')
        keysImag = filteredKeys(self._keys, 'histTSImag_')
        
        times, real = self._load1D(keysReal)
        _, imag = self._load1D(keysImag)
        
        return times, real + 1.j*imag
        
    def loadFFT(self):
        
        keysFFT = filteredKeys(self._keys, 'histFSfftw_')
        
        frequency, magnitude = self._load1D(keysFFT)
        return frequency, magnitude
        
    def loadAgg(self):
        
        keysAgg = filteredKeys(self._keys, 'histAggGridPower_')
        
        x, y, magnitude = self._load2D(keysAgg)
        
        return x, y, magnitude
        
    def load(self):
        
        return self.loadTS(), self.loadFFT(), self.loadAgg()
