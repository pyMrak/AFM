# -*- coding: utf-8 -*-
"""
Created on Thu Dec 14 13:56:28 2017

@author: andmra2
"""
from time import strftime


def getIntDate(date=None):
    koef = [1,30,365]
    curr = 0
    if date:
        for k, d in zip(koef, date):
            curr += d*k
    else:
        sym = ["%d","%m","%y"]
        for k, s in zip(koef, sym):
            #print(strftime(s))
            curr += int(strftime(s))*k
    return curr

if __name__ == "__main__":
    #print(getIntDate()+int(365/2))
    #print('Today date:',getIntDate())
    #print('Due date:',getIntDate([1,1,23]))
    pass
else:
    from libs import globalPaths


def check(version):
    
    mainVersion = version.split('_')[0]
    subVersion = version.split('_')[1]
    checkPermission = False
    online = False
    try:
        permissionsFile = open(globalPaths.path.permissions + mainVersion + '.prm', 'r', encoding="utf-8")
        premissions = permissionsFile.readlines()
        
        for permission in premissions:
            permission = permission.strip('\n')
            if permission == subVersion:
                checkPermission = True
                online = True
                break
    except FileNotFoundError as e:
        #print(e)
        if getIntDate() < 8426: #1.01.2023
            checkPermission = True
    except Exception as e:
        #print(e)
        pass
    return checkPermission, online


    


