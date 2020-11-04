#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  LocustKass.py
#  
#  Authors Florian Thomas <fthomas@uni-mainz.de>
#  
#  Date 11/4/2020
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


import json
import math
import time
from shutil import copyfile
import os

import re

#https://stackoverflow.com/questions/38853644/python-xml-parseerror-junk-after-document-element

def getRandSeed():
    
    t = int( time.time() * 1000.0 )
    seed = ((t & 0xff000000) >> 24) +\
             ((t & 0x00ff0000) >>  8) +\
             ((t & 0x0000ff00) <<  8) +\
             ((t & 0x000000ff) << 24)
             
    return seed

kassConfigDict = {'seedKass': '$SEED',
                   'tMax': '$TMAX',
                   'xMin': '$XMIN',
                   'yMin': '$YMIN',
                   'xMax': '$XMAX',
                   'yMax': '$YMAX',
                   'zMin': '$ZMIN',
                   'zMax': '$ZMAX',
                   'pitchMin': '$PITCHMIN',
                   'pitchMax': '$PITCHMAX',
                   'geometry': '$GEOMETRY' }
    
class KassConfig:
    
    def __init__(self,
                    seedKass=None,
                    tMax = None,
                    xMin = None,
                    xMax = None,
                    yMin = None,
                    yMax = None,
                    zMin = None,
                    zMax = None,
                    pitchMin = None,
                    pitchMax = None,
                    geometry = None):
        
        self.seedKass = seedKass
        self.tMax = tMax
        self.xMin = xMin
        self.xMax = xMax
        self.yMin = yMin
        self.yMax = yMax
        self.zMin = zMin
        self.zMax = zMax
        self.pitchMin = pitchMin
        self.pitchMax = pitchMax
        self.geometry = geometry
        
        self._setRandomSeed()
        
    def _setRandomSeed(self):
        
        if not self.seedKass:
            self.seedKass = getRandSeed()
            
    def makeKassConfig(self, inPath, outPath):
        
        with open(inPath) as conf:
            xml = conf.read()
        
        vals = self.__dict__
        for key in vals:
            xml=xml.replace(kassConfigDict[key], '"'+str(vals[key])+'"')
            
        with open(outPath, 'w') as newConf:
            newConf.write(xml)
        
sSim = 'simulation'
sArray = 'array-signal'
sDigit = 'digitizer'
sNoise = 'gaussian-noise'
sGen = 'generators'

locustConfigDict = {'nChannels': [sSim, 'n-channels'],
                    'vRange': [sDigit, 'v-range'],
                    'vOffset': [sDigit, 'v-offset'],
                    'eggPath': [sSim, 'egg-filename'],
                    'recordSize': [sSim, 'record-size'],
                    'loFrequency': [sArray, 'lo-frequency'],
                    'elementsPerStrip': [sArray, 'nelements-per-strip'],
                    'nSubarrays': [sArray, 'n-subarrays'],
                    'zShift': [sArray, 'zshift-array'],
                    'elementSpacing': [sArray, 'element-spacing'],
                    'seedLocust': [sNoise,'random-seed'],
                    'tfReceiverBinWidth': [sArray, 'tf-receiver-bin-width'],
                    'tfReceiverFilename': [sArray, 'tf-receiver-filename'],
                    'noisePower': [sNoise, 'noise-floor-psd']}
    
def getConfigFromFile(locustFile):
    with open(locustFile, 'r') as infile:
        return json.load(infile)

class LocustConfig:
    
    def __init__(self, 
                    nChannels=None,
                    noisePower=None,
                    vRange=None,
                    vOffset=None,
                    eggPath=None,
                    recordSize=None,
                    loFrequency=None,
                    elementsPerStrip=None,
                    nSubarrays=None,
                    zShift=None,
                    elementSpacing=None,
                    seedLocust=None,
                    tfReceiverBinWidth=None,
                    tfReceiverFilename=None):
        
        self.nChannels = nChannels
        self.noisePower = noisePower
        self.vRange = vRange
        self.vOffset = vOffset
        self.eggPath = eggPath
        self.recordSize = recordSize
        self.loFrequency = loFrequency
        self.elementsPerStrip = elementsPerStrip
        self.nSubarrays = nSubarrays
        self.zShift = zShift
        self.elementSpacing = elementSpacing
        self.seedLocust = seedLocust
        self.tfReceiverBinWidth = tfReceiverBinWidth
        self.tfReceiverFilename = tfReceiverFilename
        
        self._setRandomSeed()
        

        
    def _finalizeConfig(self, configDict):
                    
        vals = self.__dict__
        for key in vals:
            #get value from config template if it was not set
            if vals[key] is None:
                jsonKeys = locustConfigDict[key]
                if jsonKeys[0] in configDict:
                    subDict = configDict[jsonKeys[0]]
                    if jsonKeys[1] in subDict:
                        vals[key] = subDict[jsonKeys[1]]
                    
    def _setRandomSeed(self):
        
        if not self.seedLocust:
            self.seedLocust = getRandSeed()
            
    def _overwriteJson(self, configDict):
        
        vals = self.__dict__
        for key in vals:
            jsonKeys = locustConfigDict[key]
            if vals[key] is not None:
                configDict[jsonKeys[0]][jsonKeys[1]] = vals[key]
        
        return configDict
            
    def makeLocustConfig(self, inPath, outPath):
        
        config = getConfigFromFile(inPath) #self.syncConfig(inPath)
        #get missing parameters from config template
        self._finalizeConfig(config)
        #overwrite config with parameters from self
        config = self._overwriteJson(config)
        
        if self.noisePower!=0:
            config[sGen].insert(-1,'gaussian-noise')
                
        with open(outPath, 'w') as outFile:
            json.dump(config, outFile, indent=2)
        

def getNoisePower(snr):
    return 0

class SimConfig:
    
    def __init__(self, 
                    nChannels=None,
                    snr = None,
                    vRange = None,
                    vOffset = None,
                    eggPath = None,
                    locustTemplate = None,
                    kassTemplate = None,
                    recordSize = None,
                    loFrequency = None,
                    elementsPerStrip = None,
                    nSubarrays = None,
                    zShift = None,
                    elementSpacing = None,
                    seedKass = None,
                    seedLocust= None,
                    tfReceiverBinWidth = None, 
                    tfReceiverFilename = None,
                    tMax=0.5e-4,
                    xMin=0.0,
                    xMax=0.0,
                    yMin=0.0,
                    yMax=0.0,
                    zMin=0.0,
                    zMax=0.0,
                    pitchMin=90.0,
                    pitchMax=90.0,
                    geometry="/tmp/hexbug/Phase3/Trap/FreeSpaceGeometry_V00_00_04.xml"):
       
        
        
        #files
        self.locustTemplate = locustTemplate
        self.kassTemplate = kassTemplate
        
        noisePower = getNoisePower(snr)
        self.locustConfig = LocustConfig(nChannels,
                                        noisePower,
                                        vRange,
                                        vOffset,
                                        eggPath,
                                        recordSize,
                                        loFrequency,
                                        elementsPerStrip,
                                        nSubarrays,
                                        zShift,
                                        elementSpacing,
                                        seedLocust,
                                        tfReceiverBinWidth,
                                        tfReceiverFilename)
                                        
        self.kassConfig = KassConfig(seedKass,
                                        tMax,
                                        xMin,
                                        xMax,
                                        yMin,
                                        yMax,
                                        zMin,
                                        zMax,
                                        pitchMin,
                                        pitchMax,
                                        geometry)
    
    def toJson(self, filename):
        
        with open(filename, 'w') as outfile:
            json.dump(self.__dict__, outfile, indent=2, 
                            default=lambda x: x.__dict__)
            
    @classmethod
    def fromJson(cls, filename):
        
        instance = cls()
        instance.locustConfig = LocustConfig()
        instance.kassConfig = KassConfig()
        
        with open(filename, 'r') as infile:
            config = json.load(infile)
            instance.locustTemplate = config['locustTemplate']
            instance.kassTemplate = config['kassTemplate']
            instance.locustConfig.__dict__ = config['locustConfig']
            instance.kassConfig.__dict__ = config['kassConfig']
            
        return instance
        
    def makeConfig(self, filename):
        self.locustConfig.makeLocustConfig(self.locustTemplate, filename+'locust.json')
        self.kassConfig.makeKassConfig(self.kassTemplate, filename+'kass.xml')
