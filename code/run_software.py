#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 16 15:06:59 2023

@author: anyamarchenko
"""

import os, sys, subprocess, re
### You can run stata , python , and arcgis (python 2) by using this module.

def stata(path_stata, script):
    "Run stata dofile in batch mode, and deletes the log file"
    subprocess.run([path_stata, "/e", "do", script]) 
    os.remove("{}.log".format(script[0:-3])) #remove log file
# Explore by yourself to show line−by−line command in ipython console

def python(path_python, script):
    "Run Python script without arcpy"
    run = subprocess.run([path_python, script], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
    print(run.stdout)
    # returncode = 0 if code runs successfully.
    
    if run.returncode != 0:
        # stops when pyfile has an error
        sys.exit("Error : {script}".format(script = script))

