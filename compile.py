# -*- coding: utf-8 -*-
"""
Created on Wed Jan 29 11:51:09 2020

@author: andmra2
"""
import os

import PyInstaller.__main__ 

package_name = 'AFM'
PyInstaller.__main__.run([
    '--name=%s' % package_name,
    '--windowed',
    #'--add-binary=%s' % os.path.join('resource', 'path', '*.png'),
    #'--add-data=%s' % os.path.join('resource', 'path', '*.txt'),
    '--icon=%s' % os.path.join('resource', 'Graphic/Icons', 'windowIcon.ico'),
    os.path.join('AFM', '__main__.py'),
])
#
#command = "pyinstaller --icon=Graphic/Icons/windowIcon.ico --noconsole AFM.py"
#os.system(command)