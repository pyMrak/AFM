# -*- coding: utf-8 -*-
"""
Created on Wed Jan 11 11:57:12 2017

@author: andmra2
"""
from re import split
from os import listdir
from os.path import dirname, realpath
#from libs import data_manipulation as dm
from libs import data_eval as deval
from libs import globalPaths
from math import floor
from libs.logger import messageLogger

#from sys import exit


def readDefFolder():
    file = open('Settings\defaultFolder.txt', 'r', encoding="utf-8")
    i=0
    for line in file:
        folder = line
        i +=1
        
    if i == 0:
        folder = 'measurements'

    file.close()
    return folder
    
    
def readSettings(nr, username='Debug'):
    file = open(globalPaths.path.settings+username+'.set', 'r', encoding="utf-8")
    out = ''
    for i, line in enumerate(file):
        if i == nr:
            out = line.strip('\n')

    file.close()
    return out


def read_txt(file_name, gdat, path='',delimiter='.',maxlines=6502):
    ml = messageLogger()
    if path=='':
        slash=''
    else:
        slash='\\'
    try:
        file=open(path+slash + file_name+'.txt', 'r', encoding="utf-8")
        #content = file.read()
        Clines = file.readlines()
    except:
        file=open(path+slash + file_name+'.txt', 'r', encoding = 'latin-1')
        Clines = file.readlines()
        #content.encode('latin-1').decode("utf-8")
    #Clines = content.split('\n')    
    lines=[]
    count=0
    maxlines=maxlines-1
    for line in Clines:
        if count>maxlines:
            #count=0
            break
        #line=line.strip('\n')
        if delimiter==',':
            line=line.replace(',','.').strip('\n')
        line=split(r'\t+', line)
        llen=len(line)
        for i in range(llen):
            if i == 0:
                if ':' in line[i]:
                    t = line[i].split(':')
                    line[i] = 0
                    for k, tu in enumerate(t):
                        line[i] += float(tu.replace(',','.'))*60**(2-k)
                    line[i] = round(line[i],2)
                else:
                    try:
                        line[i]=round(float(line[i]),2)
                    except:
                        line[i] = 't[s]'
            else:
                try:
                    line[i]=round(float(line[i]),3)
                except:
                    pass
        while len(line) < 5:
            line.append(0)
        lines.append(line)
        count+=1
    dt = 0.01
    Dt = dt
    line = lines[-1]
    for i in range(maxlines-len(lines)+1):
        if i == 0:
            ml.writeWarning('Datoteka ' + file_name+'.txt dne vsebuje dovolj vrstic. Št. vrstic nastavljeno na '+ str(maxlines)+'.', gdat, isMD=False)
        lines.append([float(line[0]) + Dt]+[0]*(llen-1))
        Dt += dt
    return lines
    

            
    
    
def get_data_directory():
    homedir=dirname(realpath(__file__)).strip('libs')
    return homedir
    
def get_data_names(path):
    data = listdir(path)
    ndata = []
    for meas in data:
        if '.txt' in meas:
            ndata.append(meas)
    return ndata

class QC_prop():
    def __init__(self):
        self.min=0
        self.max=10000
        
class QC_init():
    def __init__(self):
        self.type='?unknown?'
        self.TtR=0
        self.tTtR=QC_prop()
        self.Tmax=QC_prop()
        self.T60=QC_prop()
        self.Imax=QC_prop()
        self.I60=QC_prop()
        self.R=QC_prop()
        
class header():
    def __init__(self, date, order, production_date, nom_v, gp_nr='?unknown?',creator='Andrej Mrak'):
        self.date=date
        self.order_nr=order
        self.production_date=production_date
        self.gp_nr=gp_nr
        self.nominal_v=nom_v
        self.creator=creator
        
def read_TCdata(path,folder,files, gdat):
    ml = messageLogger()
    TC_data=[]
    ml.writeProgressInfo('Berem meritve TC...', gdat)
    for file in files:
        TC_data.append(read_txt(file, gdat ,path + folder,',',27506))
    messageLogger.writeProgressInfo('Meritve TC prebrani.', gdat)     
    


        
    
    
class measurment_data():
    def __init__(self, gdat, TC=0,R=False,mark=False,MaxLines=6510,MeasDur=60,folder='measurements', graph=1, Curr=False, QCpath='local'):
        self.messageLogger = messageLogger()
        self.path=get_data_directory()
        self.sett = [TC, R,mark, MaxLines, MeasDur, folder, graph, Curr, QCpath]
        self.columns = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
        for i in range(26,60):
            self.columns.append(self.columns[floor(i/(26))-1]+self.columns[i%(26)])
        self.reset()
        self.readQCs()
        self.gdat = gdat
        self.graphSett = None
        
    def reset(self):
        self.data=[]
        self.locations=[]
        self.MeasStart= []
        self.table=10
        self.TC=self.sett[0]
        self.R=self.sett[1]
        self.mark=self.sett[2]
        self.maxlines=self.sett[3]
        self.MeasDur=self.sett[4]
        self.folder=self.sett[5]
        self.graph=self.sett[6]
        self.curr=self.sett[7]
        self.QCpath = self.sett[8]
        self.setQC = ''
        self.QC=QC_init()
        
        
        
        
    def read_data(self,folder=0):
        self.messageLogger.writeProgressInfo('Berem meritve...', self)
        if folder == 0:
            folder = self.folder
        elif folder == 'measurements':
            #print('narobe')
            folder = self.path + folder
        for file in self.filenames:
            self.data.append(read_txt(file, self.gdat, folder,',',self.maxlines))
            #print(file)
        deval.checkForDataErrors(self, folder+"/")
        self.messageLogger.writeProgressInfo('Meritve prebrane.', self)
        
    def get_QC(self,QC):
        
        if self.QCpath == 'local':
            fileName = self.path+'QC\QC.txt'
        else:
            fileName = globalPaths.path.QC
        file=open(fileName, 'r', encoding="utf-8").read()
        for QCd in file.split('QC\n'):
            #print('414>' in QCd,QC+'>' in QCd)
            if QC+'>' in QCd or '<'+QC in QCd: # or QC+',' in QCd:
                QCdata=QCd
                self.QC.name=QCd.split('>')[0].strip('<')
                #print(self.QC.name)
                try:
                    self.QC.TtR=int(QCdata.split('Ttr')[1].strip('</').strip('>').split('\n')[1])
                except:
                    self.messageLogger.writeWarning('Zaznan nepopolen QC '+QC+': Manjka delovna temperatura.', self)
                    self.QC.TtR = 750
                    
                temp=QCdata.split('tTtr')[1].strip('</').strip('>').split('\n')
                err = False
                try:
                    self.QC.tTtR.min=float(temp[1].strip('min:'))
                except:
                    err = True
                try:
                    self.QC.tTtR.max=float(temp[2].strip('max:'))
                except:
                    if err:
                        self.messageLogger.writeWarning('Zaznan nepopolen QC '+QC+': Manjkajo tolerance za čas dosega delovne temperature.', self)

                temp=QCdata.split('Tmax')[1].strip('</').strip('>').split('\n')
                err = False
                try:
                    self.QC.Tmax.min=int(temp[1].strip('min:'))
                except:
                    err = True
                try:
                    self.QC.Tmax.max=int(temp[2].strip('max:'))
                except:
                    if err:
                        self.messageLogger.writeWarning('Zaznan nepopolen QC '+QC+':  Manjkajo tolerance za Tmax', self)
                        
                temp=QCdata.split('T60')[1].strip('</').strip('>').split('\n')
                err = False
                try:
                    self.QC.T60.min=int(temp[1].strip('min:'))
                except:
                    err = True
                try:
                    self.QC.T60.max=int(temp[2].strip('max:'))
                except:
                    if err:
                        self.messageLogger.writeWarning('Zaznan nepopolen QC '+QC+':  Manjkajo tolerance za T60s', self)
                        
                temp=QCdata.split('Imax')[1].strip('</').strip('>').split('\n')
                err = False
                try:
                    self.QC.Imax.min=float(temp[1].strip('min:'))
                except:
                    err = True
                try:
                    self.QC.Imax.max=float(temp[2].strip('max:'))
                except:
                    if err:
                        self.messageLogger.writeWarning('Zaznan nepopolen QC '+QC+':  Manjkajo tolerance za Imax', self)
                        
                temp=QCdata.split('I60')[1].strip('</').strip('>').split('\n')
                err = False
                try:
                    self.QC.I60.min=float(temp[1].strip('min:'))
                except:
                    err = True
                try:
                    self.QC.I60.max=float(temp[2].strip('max:'))
                except:
                    if err:
                        self.messageLogger.writeWarning('Zaznan nepopolen QC '+QC+':  Manjkajo tolerance za I60s', self)
                        
                temp=QCdata.split('R')[1].strip('</').strip('>').split('\n')
                err = False
                try:
                    self.QC.R.min=int(temp[1].strip('min:'))
                except:
                    err = True
                try:
                    self.QC.R.max=int(temp[2].strip('max:'))
                except:
                    if err and self.R:
                        self.messageLogger.writeWarning('Zaznan nepopolen QC '+QC+':  Manjkajo tolerance za R.', self)
                        
                break
#        if not myQC:
#            exit("Couldn't find QC named '"+QC+"'")
            
    def readQCs(self):
        if self.QCpath == 'local':
            fileName = self.path+'QC\QC.txt'
        else:
            fileName = globalPaths.path.QC
        file=open(fileName, 'r', encoding="utf-8").read()   
        self.qcs=[]
        for qc in file.split('QC'):
            self.qcs.append(qc.split('>')[0].split('<')[-1])
            
            
    def setGraphSett(self, sett):
        self.graphSett = sett
            
            
            
    def define_TC_header(self,date=0, order_nr='?unknown?', ProductionDate='?unknown?', nomVoltage=0, gp_nr='?unknown?', author='Marko Kenda'):
        if nomVoltage==0:
            V=self.data[0][self.MeasStart[0]+500][1]
            if V<4.2:
                nomVoltage='?unknown?'
            elif V<4.7:
                nomVoltage='4,4V'
            elif V<8:
                nomVoltage='5V'
            elif V<15:
                nomVoltage='11V'
        if "V" not in nomVoltage:
            nomVoltage += 'V'
                
        if date==0:
            from time import strftime
            d=strftime("%x").split('/')
            date=d[1]+'.'+d[0]+'.'+d[2]
        self.TC_header=header(date, order_nr, ProductionDate, nomVoltage, gp_nr, author)
            