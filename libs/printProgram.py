# -*- coding: utf-8 -*-
"""
Created on Thu May  4 15:39:06 2017

@author: andmra2
"""

#import tempfile
from win32api import ShellExecute
from win32print import GetDefaultPrinter
#import os

def printFile(file):
        ShellExecute(
          0,
          "print",
          file,
          #
          # If this is None, the default printer will
          # be used anyway.
          #
          '/d:"%s"' % GetDefaultPrinter (),
          ".",
          0
        )


#os.system("open "+"//corp.hidria.com/AET/SI-TO-Users/andmra2/Python/AnalizaFmeritev/Instrumented glow plug data sheet_1_1.xlsx")
#ftw.save('Instrumented glow plug data sheet_1_1a.xlsx')


def printFiles(files):
    for file in files:
        file = file.replace('/','\\')
        printFile(file)
    
#path = "\\\\corp.hidria.com\\aet\\SI-TO-Izmenjava\\Andrej_Mrak\\__Nove_Meritve\\TC\\j-GM_230_090119"
#path.replace('/', '\\')
#print(path)
#files = os.listdir(path) 
   
#i=0
#for file in files:
#    splitFile = file.split('.')
#    
#    #print(splitFile[1], splitFile[0][:12])
#    if len(splitFile) > 1:
#        print(splitFile)
#        if splitFile[1] == 'xlsx' and splitFile[0][:12] == 'Instrumented':
#            file = path+"\\"+file
#            print(file, '\n')
#            if i >= 0:
#                printFile(file)
#            i += 1
            
            
            

        