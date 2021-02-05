# -*- coding: utf-8 -*-
"""
Created on Fri Mar 17 09:01:24 2017

@author: andmra2
"""

from libs import functional as start

#for i in range(1,13):
def Analysis(folder="measurements", maxlines=22005, QC='968', R=False, TC=False, graph=5, IG=True, mark=False, MeasDur=220, QCpath=0):
    if QCpath:
        QCPath = 'local'
    else:
        QCPath = 'global'
    debugAnalysis=start.debug(TC, R, mark, maxlines, MeasDur, graph, IG, QC, folder, QCPath)
    start.Func_Analysis(debugAnalysis)
def TCreport(folder="measurements", maxlines=22005, QC='968', R=False, TC=False, graph=5, IG=True, QCpath=0, order_nr='', ProductionDate='', nomVoltage='5V', gp_nr='', author='', TCnr = 1, mark=False, MeasDur=220):
    if QCpath:
        QCPath = 'local'
    else:
        QCPath = 'global'
    debugTCreport=start.debug(TC, R, mark, maxlines, MeasDur, graph, IG, QC, folder, QCPath)
    debugTCreport.setTCdata(order_nr, ProductionDate, nomVoltage, gp_nr, author, TCnr)
    start.TC_report(debugTCreport)
    
if __name__=='__main__':
    Analysis(folder="//corp.hidria.com/aet/SI-TO-Izmenjava/Andrej_Mrak/Proba", maxlines=6505, QC='968', R=False, TC=False, graph=1, IG=True, mark=False, MeasDur=65, QCpath=0)
#def debug(TC=False, R=False, mark=False, maxlines=6005, MeasDur=60, graph=1, IG=True,QC='414')#, folder = 'measurements'):
#folder='//HIS02-STG01/Izmenjava/Andrej_Mrak/__Nove Meritve/VW_brez_zav_R/2_1s-11V_18s_5V'
