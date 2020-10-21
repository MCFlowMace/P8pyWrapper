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

from .rootfile import RootFile

def filterfunc(key, literal, cycle='2'):
    return literal in key and key[-1]==cycle
    
def filterTSReal(key):
    return filterfunc(key, 'histTSReal_')
    
def filterTSImag(key):
    return filterfunc(key, 'histTSImag_')
    
def filterFFT(key):
    return filterfunc(key, 'histFSfftw_')
    
def filterBeamforming(key):
    return filterfunc(key, 'histAggGridPower_')
    
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
    
#functionality can be extended if required
class KatydidP3File():
    
    def __init__(self, filename):
        
        self._inputFile = RootFile(filename)
        self._keys = self._inputFile.keys()
    
    def _load(self, literal):
        
        f = lambda key: filterfunc(key, literal)
        
        keysF = [key for key in filter(f, self._keys)]
        
        nTimeslices, nChannels = extractDims(keysF)
        x, y = self._inputFile.getHistogram(keysF[0]).data()
        timeslice, channel = extractIndices(keysF[0])
        
        nBins = x.shape[0]
        
        data = np.empty(shape=(nTimeslices, nChannels, nBins), 
                        dtype=y.dtype)

        data[timeslice, channel] = y
        
        for key in keysF:
            x, y = self._inputFile.getHistogram(key).data()
            newTimeslice, channel = extractIndices(key)
            data[newTimeslice, channel] = y
        
        return x, data
    
    def loadTS(self):
        times, real = self._load('histTSReal_')
        _, imag = self._load('histTSImag_')
        
        return times, real + 1.j*imag
