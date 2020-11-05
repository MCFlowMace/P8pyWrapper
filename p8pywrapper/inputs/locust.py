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

"""
    cmd_str = "{} config={}".format(locust_binary_path,locust_config_path)
    print(cmd_str)
    output = subprocess.check_output(cmd_str, shell=True, stderr=subprocess.STDOUT)
    
    
    try: # Locust
        output = call_locust(locust_config_path)
        print('\tCreated: {}'.format(locust_egg_wnoise))
    except subprocess.CalledProcessError as e:
        print("Error: {}".format(e.output))
        return
    end_time = time.time()
    print('\tLocust simulation time was {}s'.format(end_time-start_time))
"""

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
        


# Start the container, mount the shared directory(ies), and execute the Locust commands:
#docker run -it --rm -v workingdir:/tmp -v workingdir/output:${p8locustdir}/output project8/p8compute /bin/bash -c /tmp/locust-tutorial/scripts/locustcommands.sh

