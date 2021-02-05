# -*- coding: utf-8 -*-
"""
Created on Fri Jan 18 10:54:45 2019

@author: andmra2
"""

class paths():
    
    def __init__(self):
        self.readPaths()
        
    def readPaths(self):
        pathFile = open('settings/paths.txt', 'r', encoding="utf-8")
        lines = pathFile.readlines()
        pathFile.close()
        r = False
        for line in lines:
            line = line.strip('\n').split('\t')
            if line[0] == 'izmenjava':
                self.izmenjava = line[1]
                r = True
        if not r:
            self.izmenjava = '//corp.hidria.com/aet/SI-TO-Izmenjava/'
        self.AFM = self.izmenjava+'Andrej_Mrak/ProgramData/AFM/'
        self.download = self.izmenjava+'Andrej_Mrak/AFM/'
        self.encryption = self.AFM+'encryption/'
        self.newUserRequests = self.AFM+'newUserRequests/'
        self.QC = self.AFM+'GlobalFiles/QC.txt'
        self.permissions = self.AFM+'Permissions/'
        self.usage = self.AFM+'Usage/'
        self.messages = self.AFM+'Messages/'
        self.reports = self.AFM+'reports/'
        self.usage = self.AFM+'Usage/'
        self.settings = self.AFM+'settings/'
        self.ideas = self.AFM+'Ideas/'
        
                
                
path = paths()