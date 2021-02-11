# -*- coding: utf-8 -*-
"""
Created on Fri Mar 17 09:01:24 2017

@author: andmra2
"""

from libs import functional as start

#for i in range(1,13):
def Analysis(folder="measurements", maxlines=22005, QC='968', R=False, TC=False, graph=5, IG=True, mark=False, MeasDur=220):
    debugAnalysis=start.debug(TC, R, mark, maxlines, MeasDur, graph, IG, QC, folder)
    #start.TC_report(debugAnalysis)
    start.Func_Analysis(debugAnalysis)
#def debug(TC=False, R=False, mark=False, maxlines=6005, MeasDur=60, graph=1, IG=True,QC='414')#, folder = 'measurements'):
Folder=r'\\corp.hidria.com\aet\SI-TO-Izmenjava\Andrej_Mrak\__Nove_Meritve\TC\t-VW 414 10022021\Proba'
Analysis(TC=True, R=False, mark=False, maxlines=6505, MeasDur=65, graph=1, IG=True,QC='968', folder = Folder)
#\\corp.hidria.com\aet\SI-TO-Izmenjava\Andrej_Mrak\__Nove_Meritve\TC\a-Fiat090517