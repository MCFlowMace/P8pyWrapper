# P8pyWrapper
An attempt at universal python wrappers for the Project 8 simulation chain. No ROOT installation required.

## Installation

Run `pip install -e .` in the directory with setup.py.

## Usage example

To load all data from a Phase III Katydid ROOT file as numpy arrays you can do the following:

```python
from p8pywrapper.files import KatydidP3File

file = KatydidP3File(filename)
timebins, voltage = file.loadTS()
frequency, fft = file.loadFFT()
x, y, agg = file.loadAgg()

```
`timebins` now contains one set of timestamps that apply for all timeslices. That means for the actual times in the i-th timeslice you have `t[i,0]=i*timebins[-1]+timebins[1]` or `t[i]=i*timebins[-1]+timebins`. `voltage[i,j,k]` contains the complex-valued voltage in timeslice i, at channel j for the time `t[i,k]`. `frequency` and `fft` contain the frequencies and the magnitude of the DFT per channel in a similar manner. Finally `agg[i]` contains the beamformed result of timeslice i with the `x` and `y` as the spatial grid positions.
