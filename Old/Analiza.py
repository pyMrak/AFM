# -*- coding: utf-8 -*-
"""
#Created on Wed Jan 11 12:39:39 2017

@author: andmra2
"""


from libs.logger import newLog
from libs import Permission
from libs import GUI_module as GUI
from libs import globalPaths

from PyQt5.QtWidgets import QApplication
import sys

version = 'ver2_2'
if Permission.check(version):
    app = QApplication(sys.argv)
    program = GUI.Main(version)
    sys.exit(app.exec_())
else:
    zapisi = newLog(version)
    zapisi.writeLocation('Not alowed ', version)
    print('Verzija ' + version.replace('_', '.').strip('ver') + ' je zastarela ali pa nimate dostopa do mreže.\nNove verzije so dostopne na '+globalPaths.path.download+'.')

