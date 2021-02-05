# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 14:56:02 2020

@author: andmra2
"""
from os.path import isdir, isfile

from libs.globalPaths import path



settLines = ['measurements\n',
             'global\n',
             'False\n',
             'False\n',
             '28.0\n',
             '24.0\n',
             '14.0\n',
             '12.0\n',
             '0.0\n',
            '60.0\n',
            '0.0\n',
            '30.0\n',
            '700.0\n',
            '1300.0\n',
            'bottom\n',
            '5V\n',
            '\n',
            '\n',
            '1\n',
            '\n',
            '\n',
            'False\n',
            '5011-721-414\n',
            'False\n',
            'False\n',
            '6005\n',
            'False\n',
            '3\n']

def checkVoltage(string):
    if string[-1] == 'V':
        a = int(string[-2])
    else:
        raise TypeError

def writeLines(filename, lines):
    with open(filename, 'w', encoding="utf-8") as f:
        for line in lines:
            f.write(line)

def checkSettings(username):
    global settLines
    userSettFile = path.settings+username+'.set'
    templateFile = path.settings+'user.set'
    if isfile(templateFile):
        with open(templateFile, 'r', encoding="utf-8") as f:
            tempLines = f.readlines()
    else:
        writeLines(templateFile, settLines)
        tempLines = settLines
    if isfile(userSettFile):
        with open(userSettFile, 'r', encoding="utf-8") as f:
            userLines = f.readlines()
    else:
        writeLines(userSettFile, tempLines)
        userLines = tempLines
    tempLines, toChange = checkLines(tempLines, settLines)
    if toChange:
        writeLines(templateFile, tempLines)
    userLines, toChange = checkLines(userLines, tempLines)
    if toChange:
        writeLines(userSettFile, userLines)

    
        
        
def checkLines(chkLines, compLines):
    types = [isdir, str, bool, bool, float, float, float, float, float, float,
             float, int, float, float, str, checkVoltage, str, str, int, str, str,
             bool, str, bool, bool, int, bool, int]
    changed = False
    for i, t in enumerate(types):
        if t == bool:
            if i < len(chkLines):
                if chkLines[i].strip('\n') == 'True' or chkLines[i].strip('\n') == 'False':
                    pass
                else:
                    chkLines[i] = compLines[i]
                    changed = True
            else:
                chkLines.append(compLines[i])
                changed = True
        else:
            if i < len(chkLines):
                try:
                    t(chkLines[i].strip('\n'))
                except:
                    chkLines[i] = compLines[i]
                    changed = True
            else:
                chkLines.append(compLines[i])
                changed = True
    return chkLines, changed
                
        
    
        
        
        
        
    
        
    
    