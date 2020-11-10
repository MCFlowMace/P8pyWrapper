#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  locustP3.py
#  
#  Authors Florian Thomas <fthomas@uni-mainz.de>
#  
#  Date 10/27/2020
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
import h5py
from scipy.fft import fft, fftshift, fftfreq

from p8pywrapper.inputs import SimConfig

int_max = {8:255, 16:65535}
dft_window = 8192

def applyDFT(data, dt):
    
    dataFreq = fftshift(fft(data, axis=-1),axes=-1)*np.sqrt(1/dft_window)
    frequency = fftshift(fftfreq(dft_window, d=dt))#+100e6
    
    return frequency, dataFreq
    
class LocustResult:
    
    def __init__(self, filename):
        
        self.eggfile = LocustP3File(filename+'.egg')
        self.config = SimConfig.fromJson(filename+'config.json')
        
    def get(self):
        
        return self.eggfile, self.config.toDict()

class LocustP3File:
    
    def __init__(self, filename):
        
        self._inputfile = h5py.File(filename, 'r')
        self._getAttributes()
        
    def _getAttributes(self):
        attr = self._inputfile['streams']['stream0'].attrs
        self.sr = attr['acquisition_rate']*1e6
        self._bitDepth = attr['bit_depth']
        self.nChannels = attr['n_channels']
        self._recordSize = attr['record_size']
        
        attr = self._inputfile['channels']['channel0'].attrs
        self._vRange = attr['voltage_range']
        self._vOffset = attr['voltage_offset']
        
    def keys(self):
        
        return self._inputfile.keys()
        
    def _convertToVoltage(self, data):
        
        return data/int_max[self._bitDepth]*self._vRange + self._vOffset
        
    def _reshapeTS(self, data):
        
        return data.reshape((self.nChannels, -1))
        
        
    def _TStoComplex(self, data):
        
        return data[::2] + 1j*data[1::2]
        
    def loadTS(self):
        
        data = self._inputfile['streams']['stream0']['acquisitions']['0'][0]
        data = self._convertToVoltage(data)
        data = self._TStoComplex(data)
        data = self._reshapeTS(data)
        
        return data
        
    def loadFFT(self):
        
        ts = self.loadTS()
        
        nSlices = int(ts.shape[1]/dft_window)
        tsSliced = ts[:,:nSlices*dft_window].reshape((self.nChannels, nSlices, -1))
        
        #explicit copy to rearange order in memory
        tsFinal = tsSliced.transpose(1,0,2).copy()
        
        frequency, dataFreq = applyDFT(tsFinal, 1/self.sr)
        
        return frequency, dataFreq
