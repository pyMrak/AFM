# -*- coding: utf-8 -*-
"""
Created on Thu Mar 16 09:13:10 2017

@author: andmra2
"""
from time import time
from os import system, startfile
import subprocess

from libs import data_manipulation as dm
from libs import data_eval as de
from libs import write_data as wd
from libs import read_data as rd
from libs.logger import messageLogger

def Func_Analysis(gdat):
    ml = messageLogger()
    #print('zacetek')
    start = round(time())
#    if Debug:
#        gdat.read_data(gdat.folder)
#        print('grem v transform')
#        gdat=dm.transform_to_write(gdat)
#        print('grem v write')
#        wd.write_file(gdat)
#        gdat.reset()
#    else:
    #statusBar = gdat.statusBar()
    gdat=dm.set_parameters(gdat)
    #gdat.statusBar = st
    gdat.podatki.read_data(gdat.podatki.folder)
    gdat.podatki=dm.transform_to_write(gdat.podatki)
    lastFile = wd.write_file(gdat.podatki)
    #gdat.podatki.reset()
        #gdat.podatki.reset()
    #podatki.define_TC_header(order_nr='1234',ProductionDate='231a', gp_nr='5011-721-414')
    #wd.create_TC_report(podatki,53)
    
    end = round(time())
    #print(end) 
    ml.append(' Obdelava trajala '+str(end-start)+ 's.', gdat, isMD=False)
    return [lastFile]
    
    
def TC_report(gdat):
    gdat=dm.set_parameters(gdat)
    gdat.podatki.read_data(gdat.podatki.folder)
    gdat.podatki.MeasStart = de.findMeasStart(gdat.podatki.data)
    gdat = dm.set_TC_report(gdat)
    lastFile = wd.create_TC_report(gdat.podatki, gdat.podatki.TCnr)
    gdat.podatki.reset()
    return lastFile
    
    
def openFiles(files):
    for filename in files:
        startfile(filename.replace('/', "\##").replace("##", ''), 'open')
        #subprocess.run(['open', filename], check=True)
        #system('start "" "' + filename.replace('/', "\##").replace("##", '') + '"')
    
    
    
    
    
    
    
class debugSettings():
    
    def __init__(self):
        self.name ='debugSettings'
        self.tfG = 28
        self.atfG = 24
        self.lfG = 14
        self.afG = 12
        self.talG = [0,60]
        self.UIalG = [0,30]
        self.TalG = [700,1200]
        self.lpG = 'bottom'
    
class debug():
    
    def __init__(self, TC=False, R=False, mark=False, maxlines=6505, MeasDur=60, graph=1, IG=True,QC='968', folder = 'measurements', QCpath='global'):
        self.podatki = rd.measurment_data(self)#TC=TC, R=R, mark=mark, maxlines=maxlines, MeasDur=MeasDur, folder=folder, graph=graph, curr=IG )
        #self.podatki.get_QC(QC)
        self.nastavitveA = debugSettings()   
        self.nastavitveG = debugSettings()
        self.nastavitveP = debugSettings()
        self.nastavitveA.TC=TC
        self.nastavitveA.QC=QC
        self.nastavitveG.IG=IG
        self.nastavitveG.nG=graph
        self.nastavitveA.R=R
        self.nastavitveA.fname=folder
        self.nastavitveA.maxlines = maxlines
        self.nastavitveA.TT = False

        self.nastavitveP.QCpath = QCpath
        
    def setTCdata(self, order_nr='', ProductionDate='', nomVoltage='5V', gp_nr='', author='', TCnr = 1):
        self.nastavitveA.stNarocila = order_nr
        self.nastavitveA.datumProizvodnje = ProductionDate
        self.nastavitveA.nomV = nomVoltage
        #print('nom self.nastavitveA.nomV: ', self.nastavitveA.nomV)
        self.nastavitveA.kodaIzdelka = gp_nr
        self.nastavitveA.avtor = author
        self.nastavitveA.oznakaGP = TCnr
        
#        #podatki = rd.measurment_data(TC, R, mark, maxlines, MeasDur, folder, graph, IG)
#        #podatki.setQC = QC
#        if self.podatki.folder == 'measurements':
#            podatki.filenames = dm.rearrange_up(rd.get_data_names(podatki.path+podatki.folder))
#            podatki.length=len(podatki.filenames)
#        else:
#            podatki.filenames = dm.rearrange_up(rd.get_data_names(podatki.folder))
#            podatki.length=len(podatki.filenames)
#        podatki.get_QC(podatki.setQC)
#        Func_Program(podatki, True)
    
    

    
    #return gdat.podatki