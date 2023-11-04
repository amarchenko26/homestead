#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 16 15:09:24 2023

@author: anyamarchenko
"""

import glob , os , sys
import run_software #Created a module that enables us to run stata and python2 as well 
path_Stata = glob.glob("C:\∗\Stata∗\Stata∗.exe")[0] #tell python where my Stata is, this is for windows, update for Mac
path_Python2 = glob.glob("C:\Python27\ArcGIS10.∗\pythonw.exe")[0]

def main(): 
    build()
    analysis()

def build ():
    os.chdir("build")
    print("Construct a rebel−level conflict event datasets from the UCDP") 
    run_software.python(sys.executable, "conflicts_event_to_group.py")
    
    print("Construct by−hand matching results of ethnic groups corresponding to rebels.") 
    run_software.stata(path_Stata, "match_ethnologue_Islam_groups.do")
    
    print("Combine rebel−level conflict event with matching status")
    run_software.python(sys.executable, "conflicts_event_to_group_match.py")
    

os.chdir("..") #chdir means change directory. changes to the upper director

def analysis():
    os.chdir("analysis")
    os.chdir("..")
    
main() # Run the main program, i.e. run everything