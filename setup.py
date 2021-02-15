#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  setup.py
#  
#  Authors Florian Thomas <fthomas@uni-mainz.de>
#  
#  Date 10/20/2020
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

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="p8pywrapper",
    version="0.0.1",
    author="Florian Thomas",
    author_email="fthomas@uni-mainz.de",
    description="A wrapper for the P8 simulation chain",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MCFlowMace/P8pyWrapper",
    packages=setuptools.find_packages(),
    install_requires=[
        'numpy',
        'scipy',
        'matplotlib',
        'h5py',
        'uproot'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)
