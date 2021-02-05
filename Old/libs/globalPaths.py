# -*- coding: utf-8 -*-
"""
Created on Fri Jan 18 10:54:45 2019

@author: andmra2
"""

class paths():
    
    def __init__(self):
        self.readPaths()
        
    def readPaths(self):
        pathFile = open('settings/paths.txt', 'r')
        lines = pathFile.readlines()
        pathFile.close()
        for line in lines:
            line = line.strip('\n').split('\t')
            if line[0] == 'qcpath':
                self.QC = line[1]
            elif line[0] == 'izmenjava':
                self.izmenjava = line[1]
            elif line[0] == 'download':
                self.download = line[1]
                
                
path = paths()