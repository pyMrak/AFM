# -*- coding: utf-8 -*-
"""
Created on Thu Dec 14 13:56:28 2017

@author: andmra2
"""
from libs import globalPaths

def check(version):
    mainVersion = version.split('_')[0]
    subVersion = version.split('_')[1]
    checkPermission = False
    try:
        permissionsFile = open(globalPaths.path.izmenjava+'Andrej_Mrak/__Nove_Meritve/_Reports/Permissions/' + mainVersion + '.prm', 'r')
        premissions = permissionsFile.readlines()
        
        for permission in premissions:
            permission = permission.strip('\n')
            if permission == subVersion:
                checkPermission = True
                break
    except:
        checkPermission = False
        
    return checkPermission