#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  locust.py
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

from .config import SimConfig
import subprocess
import os

class Locust:
    
    def __init__(self, workingdir, hexbugdir,
                container='project8/p8compute',
                locustversion='v2.1.2', 
                p8computeversion='v0.10.1'):
                            
        self.workingdir=workingdir+'/'
        self.outputdir = self.workingdir+'output/'
        self.locustversion=locustversion
        self.p8computeversion=p8computeversion
        self.p8locustdir='/usr/local/p8/locust/'+locustversion
        self.p8computedir='/usr/local/p8/compute/'+p8computeversion
        self.container=container
        self.hexbugdir=hexbugdir
        
        self._genCommandScript()
        
    def run(self, config, filename):
        
        #try: # Locust
         #   output = call_locust(locust_config_path)
        #except subprocess.CalledProcessError as e:
        
        filenamelocust = filename+'locust.json'
        filenamekass = filename+'kass.xml'
        config.setXml('/tmp/output/'+filenamekass)
        config.setEgg(self.p8locustdir+'/output/'+filename+'.egg')
        config.makeConfig(self.outputdir+filenamelocust, 
                            self.outputdir+filenamekass)
        config.toJson(self.outputdir+filename+'config.json')
        
        cmd = self._assembleCommand('/tmp/output/'+filename)
        
        print(cmd)
        
        os.system(cmd)
        
        deleteCmd = 'rm -f ' + self.outputdir+filenamelocust
        deleteCmd += ' ' + self.outputdir+filenamekass
        deleteCmd += ' ' + self.outputdir+'Phase3Seed*Output.root'
        
        os.system(deleteCmd)

        
    def _assembleCommand(self, configFile):
        cmd = 'docker run -it --rm -v '
        cmd += self.workingdir
        cmd += ':/tmp -v '
        cmd += self.workingdir
        cmd += '/output:'
        cmd += self.p8locustdir
        cmd += '/output -v '
        cmd += self.hexbugdir
        cmd += ':/hexbug '
        cmd += self.container
        cmd += ' /bin/bash -c "/tmp/locustcommands.sh '
        cmd += configFile
        cmd += 'locust.json"'
        
        return cmd
        
    def _genCommandScript(self):
        
        commands = '#!/bin/bash\n'
        commands += 'source ' + self.p8computedir+'/setup.sh\n'
        commands += 'source ' + self.p8locustdir+'/bin/kasperenv.sh\n'
        commands += 'LocustSim config=$1'
        
        with open(self.workingdir+'locustcommands.sh', 'w') as outFile:
            outFile.write(commands)
            
        os.system('chmod +x '+self.workingdir+'locustcommands.sh')
        
