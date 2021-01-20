# P8pyWrapper
Personal python wrappers for the Project 8 simulation chain. No ROOT installation required.

## Installation

Run `pip install -e .` in the directory with setup.py.

## Usage example

Run a Locust simulation:

```python

from p8pywrapper.inputs import SimConfig, Locust

workingdir='/home/flthomas/Project8/p8compute_share/workspace'
hexbugdir = '/home/flthomas/Project8/p8compute_share/hexbug'

#template files
locustConf = hexbugdir + '/Phase3/LocustPhase3ModTemplate.json'
kassConf = hexbugdir + '/Phase3/LocustKassElectronsTemplate.xml'

#modify the config templates
conf = SimConfig(locustTemplate=locustConf, kassTemplate=kassConf, 
                    nChannels=60, xMin=0.02, xMax=0.02, tMax=0.00015, recordSize=41000)

#run Locust in the container
locustWrapper = Locust(workingdir, hexbugdir)
locustWrapper.run(conf, 'offcenter_60_channels_long')

```
This will create an egg file `offcenter_60_channels_long.egg` and a json file `offcenter_60_channels_longconfig.json` in `workingdir`. The json file is used to import the `SimConfig` object back into python.

Load data from Locust egg file:

```python
from p8pywrapper.files import LocustP3File, LocustResult

lFile, config = LocustResult(fileName).get()
timeseries = lFile.loadTS()
frequencyC, dataFreq = lFile.loadFFT()

```
`config`contains a dictionary with the used simulation parameters.

To load all data from a Beamforming Katydid ROOT file as numpy arrays you can do the following:

```python
from p8pywrapper.files import KatydidP3File

file = KatydidP3File(filename)
timebins, voltage = file.loadTS()
frequency, fft = file.loadFFT()
x, y, agg = file.loadAgg()

```
`timebins` now contains one set of timestamps that apply for all timeslices. That means for the actual times in the i-th timeslice you have `t[i,0]=i*timebins[-1]+timebins[1]` or `t[i]=i*timebins[-1]+timebins`. `voltage[i,j,k]` contains the complex-valued voltage in timeslice i, at channel j for the time `t[i,k]`. `frequency` and `fft` contain the frequencies and the magnitude of the DFT per channel in a similar manner. Finally `agg[i]` contains the beamformed result of timeslice i with the `x` and `y` as the spatial grid positions.
