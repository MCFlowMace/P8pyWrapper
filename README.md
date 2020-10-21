# P8pyWrapper
An attempt at universal python wrappers for the Project 8 simulation chain. No ROOT installation required.

## Installation

Run `pip install -e .` in the directory with setup.py.

## Usage example

To load all time series from a Phase III Katydid ROOT file you can do the following:

```python
from p8pywrapper.files import KatydidP3File

file = KatydidP3File(filename)
timebins, voltage = file.loadTS()

```
`timebins` now contains one set of timestamps that apply for all timeslices. That means for the actual times in the i-th timeslice you have `t[i,0]=i*timebins[-1]+timebins[1]` or `t[i]=i*timebins[-1]+timebins`. `voltage[i,j,k]` contains the complex-valued voltage in timeslice i, at channel j for the time `t[i,k]`.
