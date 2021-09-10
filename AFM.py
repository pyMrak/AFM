# -*- coding: utf-8 -*-
"""
#Created on Wed Jan 11 12:39:39 2017

@author: andmra2
"""

debug = True
from libs.logger import newLog
from libs import Permission, login
from libs import GUI_module as GUI
from libs import globalPaths
from PyQt5.QtWidgets import QApplication, QDialog
from sys import exit as sysExit
from sys import argv



version = 'ver2_4'
app = QApplication(argv)
alowed, online = Permission.check(version)
log = None

if __name__ =="__main__":
    if alowed:
        if debug:
            program = GUI.Main(version, online, None)
        else:
            log = login.Login()
            if log.exec_() == QDialog.Accepted:
                #print(login.logMod.username, login.logMod.userType)
                program = GUI.Main(version, online, login.logMod)

    else:
        zapisi = newLog(version, log)
        zapisi.writeLocation('Not alowed ', version)
        GUI.permissionError(app, 'Verzija ' + version.replace('_', '.').strip('ver') +
                            ' je zastarela ali pa nimate dostopa do mreže.\nNove verzije so dostopne na '+
                            globalPaths.path.download+'.')
    sysExit(app.exec_())


